export MS_ID=${MI_DEV_MICROSERVICE_ID:-123} 
export HOST=${MI_DEV_HOST:-app.leanix.net}
export TOKEN=${MI_DEV_TOKEN:-<YOUR API TOKEN>}

export URL="https://$HOST/services/cicd-connector/v1/dependencies"

curl -X POST \
    "$URL?source=gradle&externalId=$MS_ID"\
    -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
    -F 'api_token='$TOKEN \
    -F 'host='$HOST \
    -F 'file=@gradle-dependencies.txt'