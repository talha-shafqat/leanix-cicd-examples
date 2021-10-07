import json


workspace = "<WS ID>"
microserviceId = "<MICROSERVICE ID>"
with open('openapi_3.0_example.json', 'r') as f:

    j = json.load(f)
    apis = {}
    title = j['info']['title']

    content = []
    for path, path_definition  in j['paths'].items():
        for k, v in path_definition.items():
            if (v['tags'][0] not in apis):
                apis[v['tags'][0]]={
                    'type': 'API',
                    'id': v['tags'][0],
                    'data': {
                        'name': title + ' - ' + v['tags'][0],
                        'microserviceId': microserviceId,
                        'description': ""
                        }}
            if ('operations' not in apis[v['tags'][0]]['data']):
                apis[v['tags'][0]]['data']['operations'] = []

            apis[v['tags'][0]]['data']['operations'].append({
               'url': path,
               'description': v['summary'],
               'name': str(k).upper() + ' - ' + path
           })

    content = [v for v in apis.values()]
    for dataObject, data  in j['components']['schemas'].items():
        elementToAdd = {'type': 'Data Object', 'id': dataObject}
        elementToAdd['description'] = data['description'] if ('description' in data) else ""
        content.append(elementToAdd)

    ldif = {
        "connectorType": "swagger-connector",
        "connectorId": "swagger-connector",
        "connectorVersion": "1.0",
        "processingMode": "full",
        "lxVersion": "1.0.0",
        "lxWorkspace": workspace,
        "description": "",
        "content": content}
    print (json.dumps(ldif, indent=2))