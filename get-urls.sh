#!/bin/bash
BASE_URL="$1"

if [[ -z "$BASE_URL" ]] || [[ "$BASE_URL" = "-h" ]]; then
    echo "Usage: $0 <base_url>"
    exit 1
fi

if [[ "${BASE_URL}" != */ ]]; then
    BASE_URL="${BASE_URL}/"
fi

wget -qO- "$BASE_URL" \
    | grep -oP '(?<=href=")[^"]*' \
    | grep -v '^\.\./' \
    | sed 's|^|'"$BASE_URL"'|' \
    | jq -R . \
    | jq -s .
