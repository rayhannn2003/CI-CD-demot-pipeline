#!/usr/bin/env bash
set -euo pipefail

# Simple health check script that polls the /health endpoint until it returns HTTP 200
# Usage: ./healthcheck.sh [URL]

# Use Docker bridge gateway IP to reach app from Jenkins container
URL=${1:-http://172.17.0.1:3000/health}
MAX_RETRIES=10
SLEEP=3

for i in $(seq 1 "$MAX_RETRIES"); do
	HTTP=$(curl -s -o /dev/null -w "%{http_code}" "$URL" || echo "000")
	if [ "$HTTP" = "200" ]; then
		echo "Health check passed ($HTTP) at $URL"
		exit 0
	fi
	echo "Attempt $i/$MAX_RETRIES - got $HTTP, retrying in $SLEEP..."
	sleep $SLEEP
done

echo "Health check failed after $MAX_RETRIES attempts"
exit 1
