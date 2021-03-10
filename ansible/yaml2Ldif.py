import json
import yaml


workspace = "<WS_ID>"
with open('sample.yaml', 'r') as f:
    y = yaml.load(f, Loader=yaml.FullLoader)

    content = []
    for l in y['rabbitmq_vhosts']:
        content.append({'type': 'service', 'id': l['vhost'], 'data': {}})
        if 'queues' in l:
            for q in l['queues']:
                content.append({'type': 'queue', 'id': q['queuename'], 'data': { 'service': l['vhost']}})
        if 'exchanges' in l: 
            for e in l['exchanges']:
                content.append({'type': 'exchange', 'id': e['exchangename'], 'data': { 'service': l['vhost'], 'queue': e['bind_to'][0]['destination']}})

    ldif = {
        "connectorType": "swagger-connector",
        "connectorId": "swagger-connector",
        "connectorVersion": "1.0",
        "processingMode": "full",
        "lxVersion": "1.0.0",
        "lxWorkspace": workspace,
        "description": "",
        "content": content }

    print (json.dumps(ldif, indent=2))