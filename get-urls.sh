#!/bin/bash
wget -qO- "$1" \
    | grep -oP '(?<=href=")[^"]*' \
    | grep -v '^\.\./' \
    | sed 's|^|'"$1"'|' \
    | jq -R . \
    | jq -s .
