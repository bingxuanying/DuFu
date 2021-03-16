#!/bin/bash

SOURCEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DUFUMAINDIR="$( dirname "${SOURCEDIR}" )"
MAINFILEDIR="${DUFUMAINDIR}/core/main/BrokerServer.py"

# Check if server file exists
if [ ! -f "${MAINFILEDIR}" ]; then
    echo "[ERROR] BrokerServer.py file doesn't exist" >&2
    exit 1
fi

python3 "${MAINFILEDIR}" --show

exit 0