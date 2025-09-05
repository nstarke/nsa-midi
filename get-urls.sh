#!/bin/bash
wget -qO- "$1" | grep -oP '(?<=href=")[^"]*' > "$2"
