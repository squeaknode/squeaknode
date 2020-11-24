#!/usr/bin/env bash

# exit from script if error was raised.
set -e

# # Add btcd's RPC TLS certificate to system Certificate Authority list.	exec runsqueak \
# cp /rpc/rpc.cert /usr/share/ca-certificates/btcd.crt
# echo btcd.crt >> /etc/ca-certificates.conf
# update-ca-certificates

# # To make python requests use the system ca-certificates bundle, it
# # needs to be told to use it over its own embedded bundle
# export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

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
