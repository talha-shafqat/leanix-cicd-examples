export MS_ID=${MI_DEV_MICROSERVICE_ID:-123} 
export HOST=${MI_DEV_HOST:-demo-eu.leanix.net}
export TOKEN=${MI_DEV_TOKEN:-<YOUR TOKEN>}

export SYNC_URL="https://${HOST}/services/integration-api/v1/synchronizationRuns"

BEARER=$(curl -X POST --url https://${HOST}/services/mtm/v1/oauth2/token -u apitoken:${TOKEN} --data grant_type=client_credentials | jq -r '.access_token') 
SYNC_RUN=$(curl -X POST --header 'Content-Type: application/json' --header "Authorization: Bearer $BEARER" -d "`cat sample.json`" $SYNC_URL | jq -r '.id') 
RES=$(curl --write-out '%{http_code}' -X POST --header 'Content-Type: application/json' --header "Authorization: Bearer $BEARER" $SYNC_URL/$SYNC_RUN/start)

if test "$RES" == "200"; then
   echo "Sync run successfully started"
fi