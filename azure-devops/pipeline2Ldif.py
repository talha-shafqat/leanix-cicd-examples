import json
import requests
import time
import base64
import os
from requests.auth import HTTPBasicAuth

# ENV VARS
ADO_AUTH = os.getenv('ADO_AUTH')
ADO_ORGANIZATION = os.getenv('ADO_ORGANIZATION')
ADO_PROJECT = os.getenv('ADO_PROJECT')
LEANIX_DOMAIN = os.getenv('LEANIX_DOMAIN')
LEANIX_API_TOKEN = os.getenv('LEANIX_API_TOKEN')
WORKSPACE_ID = "" # setup to pass along ID in other function


def pipeline2ldif():

    # The name of the Azure DevOps Organization
    ado_organization = ADO_ORGANIZATION
    # The name of the Azure DevOps Project (can be the name or the ID)
    add_project = ADO_PROJECT

    # This is the token provided by Azure Dev Ops
    auth = HTTPBasicAuth(
        '', ADO_AUTH)

    request_url = 'https://dev.azure.com/' + ado_organization + '/' + add_project + \
        '/_apis/pipelines?api-version=6.0-preview.1'  # Reques to get a full list of available pipelines
    # related to this Project

    res = requests.get(request_url, auth=auth)
    pipeline_list = res.json()

    pipeline_configs = []
    for pipeline_item in pipeline_list['value']:
        # print(json.dumps(pipeline_list, indent=2))
        response = requests.get(
            pipeline_item['_links']['self']['href'], auth=auth)

        # List of runs
        runs_list = []

        # Get last 1000 runs from each pipeline
        add_pipe_line_id = str(pipeline_item['id'])

        # Get individual run from pipeline
        runs_url = 'https://dev.azure.com/' + ado_organization + '/' + add_project + \
            '/_apis/pipelines/' + add_pipe_line_id + '/runs?api-version=6.0-preview.1'
        runs_response = requests.get(runs_url, auth=auth)
        runs_json = runs_response.json()

        # Add individual run to metrics
        for runs_item in runs_json['value']:
            if runs_item['state'] == 'completed':
                runs_list.append({
                    "type": "Run",
                    "id": "run_" + runs_item['name'],
                    "data": {
                        'state': runs_item['state'],
                        'result': runs_item['result'],
                        'date': runs_item['finishedDate'],
                        "deployment": runs_item['pipeline']['name']
                    }
                })

        response_json = json.loads(response.content)

        # Add Config fact sheet with history of runs
        pipeline_configs.append({
            "type": "Configuration",
            "id": response_json['name'],
            "data": {
                'url': response_json['_links']['web']['href'],
                'name': response_json['configuration']['repository']['fullName'],
                'runs': runs_list
            }
        })
        # To add further fact sheets in the future
        # pipeline_configs.append({
        #     "type": "Fact Sheet Type - mandatory field",
        #     "id": <<Delineate your required ID here - mandatory field>>,
        #     "data": {
        #         'exampleList': [
        #           {<<Add list item 1 here>>},
        #           {<<Add list item 2 here>>},
        #         ],
        #         'name': <<This shows that you can have any item in data section>>
        #     }
        # })

    # Add up findings from each API to create LDIF

    ldif = {
        "connectorType": "leanix",
        "connectorId": "leanix-azureDevOps-connector",
        "connectorVersion": "1.0.0",
        "processingDirection": "inbound",
        "processingMode": "full",
        "lxVersion": "1.0.0",
        "lxWorkspace": "workspaceId",
        "description": "Azure DevOps Connector",
        "content": pipeline_configs}
    # print(json.dumps(ldif, indent=2))
    return(ldif)

def access_configs():
    access_data = {
      "domain": LEANIX_DOMAIN,
      "apitoken": LEANIX_API_TOKEN
    }

    return access_data

def auth_url():
    domain = access_configs()['domain']
    return f"https://{domain}/services/mtm/v1/oauth2/token"

def request_url():
    domain = access_configs()['domain']
    return f"https://{domain}/services/integration-api/v1/"

def api_token():
    return access_configs()['apitoken']

def getAccessTokenJson(access_token):
  payload_part = access_token.split('.')[1]
  # fix missing padding for this base64 encoded string.
  # If number of bytes is not dividable by 4, append '=' until it is.
  missing_padding = len(payload_part) % 4
  if missing_padding != 0:
    payload_part += '='* (4 - missing_padding)
  payload = json.loads(base64.b64decode(payload_part))
  return payload

def authenticate():
    response = requests.post(auth_url(), auth=('apitoken', api_token()),
                             data={'grant_type': 'client_credentials'})

    response.raise_for_status()
    access_token = response.json()['access_token']
    global WORKSPACE_ID
    WORKSPACE_ID = getAccessTokenJson(access_token)['principal']['permission']['workspaceId']

    return {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}

def call_post(endpoint, header, data=False):
    response = requests.post(
        url=request_url() + endpoint, headers=header, data=data)
    response.raise_for_status()
    return response

def call_get(endpoint, header):
    response = requests.get(url=request_url() + endpoint, headers=header)
    response.raise_for_status()
    return response

def create_run(run_config, header):
    result = call_post(endpoint="synchronizationRuns",
                       data=json.dumps(run_config), header=header)
    return json.loads(result.text)['id']

def start_run(run_id, header):
    start_run_endpoint = 'synchronizationRuns/%s/start' % (run_id)
    result = call_post(endpoint=start_run_endpoint, header=header)
    return result.status_code

def check_run_status(run_id, header, status_response=False):
    print('checking status')
    status_endpoint = 'synchronizationRuns/%s/status' % (run_id)
    status_response = call_get(status_endpoint, header)
    status_response = json.loads(status_response.text)['status']
    print(status_response)
    if status_response != 'FINISHED':
        time.sleep(5)
        return check_run_status(run_id, status_response=status_response, header=header)
    else:
        return True

def fetch_results(run_id, header):
    results_endpoint = 'synchronizationRuns/%s/results' % (run_id)
    results_response = call_get(results_endpoint, header)
    return json.loads(results_response.text)

def handle_run(ldif_data, processing_direction, header):

    run_id = create_run(ldif_data, header)
    if start_run(run_id, header) == 200:
        if check_run_status(run_id, header) and processing_direction == 'outbound':
            return fetch_results(run_id, header)


def run_integration_api():

    header = authenticate()

    ldif_data = pipeline2ldif()
    ldif_data["lxWorkspace"] = WORKSPACE_ID

    connector_id = ldif_data['connectorId']
    connector_version = ldif_data['connectorVersion']
    processing_direction = ldif_data['processingDirection']

    if processing_direction == 'outbound':
        run_results = handle_run(
            ldif_data=ldif_data, processing_direction='outbound', header=header)
        with open('_'.join([connector_id + connector_version]) + '.json', 'w') as outfile:
            json.dump(run_results, outfile, ensure_ascii=False, indent=4)
    else:
        handle_run(ldif_data, processing_direction='inbound', header=header)


# Initiate script
run_integration_api()