#!/usr/bin/env bash

# exit from script if error was raised.
set -e

CMD="$1"

READY=0

while [ $READY != 1 ]
do
    echo "Trying to run cmd: $CMD" >&2
    eval $CMD &
    last_pid=$!
    sleep 30
    if kill $last_pid > /dev/null 2>&1; then
	echo "Found running process for pid: $last_pid" >&2
	READY=1
    fi
done
