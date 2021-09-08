import json
import yaml


workspace = "<WS_ID>"
microserviceId = "<MICROSERVICE ID>"
with open('sample.json', 'r') as f:

    j = json.load(f)

    base_url = j['basePath']
    

    data= []
    for definition in (j['definitions']):
        data.append({'type': 'definition', 'id': definition, 'data': {}})

    operations = []
    for path, path_definition in j['paths'].items():
        for k, v in path_definition.items():
            operations.append({
                'url': base_url + path,
                'description': v['description'],
                'name': k + ' - ' + base_url + path
            })

    data.append({'type': 'api', 'id': j['info'], 'data': {'operations': operations}})
    
    ldif = {
        "connectorType": "swagger-connector",
        "connectorId": "swagger-connector",
        "connectorVersion": "1.0",
        "processingMode": "full",
        "lxVersion": "1.0.0",
        "lxWorkspace": workspace,
        "description": "",
        "content": data}
    print (json.dumps(ldif, indent=2))