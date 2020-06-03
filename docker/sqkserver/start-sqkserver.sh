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
LND_HOST="lnd"
LND_PORT=10009
BTCD_HOST="btcd"
RPCUSER=$(set_default "$RPCUSER" "devuser")
RPCPASS=$(set_default "$RPCPASS" "devpass")
DEBUG=$(set_default "$DEBUG" "debug")
NETWORK=$(set_default "$NETWORK" "simnet")
CHAIN=$(set_default "$CHAIN" "bitcoin")
BACKEND="btcd"
SQK_HOST="localhost"
SQK_PORT="56789"

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


# Generate the config file.
chmod +x config.ini.sh
./config.ini.sh $NETWORK $LND_HOST $LND_PORT $BTCD_HOST $BTCD_RPC_PORT $RPCUSER $RPCPASS $SQK_HOST $SQK_PORT > config.ini
echo "config.ini:"
cat config.ini

# # Initialize the client database.
# runsqueaknodeclient \
#     "--config"="config.ini" \
#     "--log-level"="$DEBUG" \
#     init-db

echo "$DEBUG:"
echo $DEBUG

echo "Starting to run the python server here...."

exec runsqueaknodeserver \
     "--config"="config.ini" \
     "--log-level"="$DEBUG" \
     run-server

# exec ls
