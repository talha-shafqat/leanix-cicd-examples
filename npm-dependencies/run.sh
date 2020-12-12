export MS_ID=${MI_DEV_MICROSERVICE_ID:-123} 
export HOST=${MI_DEV_HOST:-demo-eu.leanix.net}
export TOKEN=${MI_DEV_TOKEN:-<YOUR TOKEN>}

echo $HOST
echo $TOKEN

export URL="https://${HOST}/services/cicd-connector/v1/dependencies"

curl -X POST \
      "$URL?source=npm&externalId=$MS_ID" \
      -H 'content-type: multipart/form-data' \
      -F "api_token=${TOKEN}" \
      -F "host=${HOST}" \
      -F 'file=@dependencies.json'
