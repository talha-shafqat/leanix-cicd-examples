import json
import yaml


workspace = "<WS_ID>"
microserviceId = "<MICROSERVICE ID>"
with open('sample.yaml', 'r') as f:
    y = yaml.load(f, Loader=yaml.FullLoader)

    base_url = 'https://' + y['host'] + y['basePath']
    title = y['info']['title']

    apis = {}
    for tag in y['tags']:
        apis[tag['name']] = {
            'type': 'API', 
            'id': base_url + ' ' + tag['name'], 
            'data': {'name': title + ' - ' + tag['name'], 'microserviceId': microserviceId, 'description': tag['description'], 'operations':[]}}

    for path in y['paths']:
        cmd = list(y['paths'][path].keys())[0].upper()
        operation = list(y['paths'][path].values())[0]

        apis[operation['tags'][0]]['data']['operations'].append({
            'url': base_url + path,
            'description': operation['summary'],
            'name': str(cmd) + ' - ' + base_url + path
        })
    
    ldif = {
        "connectorType": "swagger-connector",
        "connectorId": "swagger-connector",
        "connectorVersion": "1.0",
        "processingMode": "full",
        "lxVersion": "1.0.0",
        "lxWorkspace": workspace,
        "description": "",
        "content": [v for v in apis.values()]}
    print (json.dumps(ldif, indent=2))