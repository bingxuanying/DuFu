#!/bin/bash

SOURCEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DUFUMAINDIR="$( dirname "${SOURCEDIR}" )"
MAINFILEDIR="${DUFUMAINDIR}/clients/main/publisher/Publisher.py"

echo "${MAINFILEDIR}"

# Check if server file exists
if [ ! -f "${MAINFILEDIR}" ]; then
    echo "[ERROR] Publisher.py file doesn't exist" >&2
    exit 1
fi

case $1 in
    broker)
        echo -n "Starting Publisher with active broker ..."
        python3 "${MAINFILEDIR}" --show -b
        ;;
    *)
        echo -n "Starting Publisher with broker off ..."
        python3 "${MAINFILEDIR}" --show
        ;;
esac

exit 0