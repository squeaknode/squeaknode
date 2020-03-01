#!/usr/bin/env bash

# exit from script if error was raised.
set -e

# error function is used within a bash function in order to send the error
# message directly to the stderr output and exit.
error() {
    echo "$1" > /dev/stderr
    exit 0
}

# return is used within bash function in order to return the value.
return() {
    echo "$1"
}

# set_default function gives the ability to move the setting of default
# env variable from docker file to the script thereby giving the ability to the
# user override it durin container start.
set_default() {
    # docker initialized env variables with blank string and we can't just
    # use -z flag as usually.
    BLANK_STRING='""'

    VARIABLE="$1"
    DEFAULT="$2"

    if [[ -z "$VARIABLE" || "$VARIABLE" == "$BLANK_STRING" ]]; then

        if [ -z "$DEFAULT" ]; then
            error "You should specify default variable"
        else
            VARIABLE="$DEFAULT"
        fi
    fi

   return "$VARIABLE"
}

# Set default variables if needed.
RPCUSER=$(set_default "$RPCUSER" "devuser")
RPCPASS=$(set_default "$RPCPASS" "devpass")
DEBUG=$(set_default "$DEBUG" "debug")
NETWORK=$(set_default "$NETWORK" "simnet")
CHAIN=$(set_default "$CHAIN" "bitcoin")
BACKEND="btcd"

# This is a hack that is needed because python-bitcoinlib does not
# currently support simnet network.
BTCD_RPC_PORT="18332"
if [[ "$NETWORK" == "mainnet" ]]; then
    BTCD_RPC_PORT="8334"
elif [[ "$NETWORK" == "testnet" ]]; then
    BTCD_RPC_PORT="18334"
elif [[ "$NETWORK" == "regtest" ]]; then
    BTCD_RPC_PORT="18445"
elif [[ "$NETWORK" == "simnet" ]]; then
    BTCD_RPC_PORT="18556"
fi


# Add btcd's RPC TLS certificate to system Certificate Authority list.	exec runsqueak \
cp /rpc/rpc.cert /usr/share/ca-certificates/btcd.crt
echo btcd.crt >> /etc/ca-certificates.conf
update-ca-certificates

# To make python requests use the system ca-certificates bundle, it
# needs to be told to use it over its own embedded bundle
export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

exec runsqueaknodeclient \
     "--network"="$NETWORK" \
     "--rpcuser"="$RPCUSER" \
     "--rpcpass"="$RPCPASS" \
     "--$BACKEND.rpchost"="blockchain" \
     "--$BACKEND.rpcport"="$BTCD_RPC_PORT" \
     "--$BACKEND.rpcuser"="$RPCUSER" \
     "--$BACKEND.rpcpass"="$RPCPASS" \
     "--lnd.rpchost"="lnd" \
     --log-level="$DEBUG" \
