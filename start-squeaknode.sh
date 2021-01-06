#!/usr/bin/env bash

# exit from script if error was raised.
set -e

# # Wait for the lnd cert file to exist before starting
# while ! test -f "/root/.lnd/tls.cert"; do
#     sleep 10
#     echo "Still waiting for lnd cert file to exist..."
# done

sleep 10

# Start using the run server command
if [ -f config.ini ]; then
    exec runsqueaknode \
	 --config config.ini \
	 --log-level INFO \
	 run-server
else
    exec runsqueaknode \
	 --log-level INFO \
	 run-server
fi
