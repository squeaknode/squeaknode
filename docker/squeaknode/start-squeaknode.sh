#!/usr/bin/env bash

# exit from script if error was raised.
set -e

# Wait for the lnd cert file to exist before starting
while ! test -f "/root/.lnd/tls.cert"; do
    sleep 10
    echo "Still waiting for lnd cert file to exist..."
done

# Start using the run server command
exec runsqueaknode \
     --config config.ini \
     --log-level INFO \
     run-server
