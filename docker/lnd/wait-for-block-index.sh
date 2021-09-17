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
    echo "Starting lnd with pid: $last_pid" >&2
    echo "Sleeping for 20 seconds..."
    sleep 20
    if ps -p $last_pid; then
	echo "Found running process for pid: $last_pid" >&2
	READY=1
	wait $last_pid
    else
	echo "Sleeping for 5 seconds..."
	sleep 5
    fi
done
