#define parameters which are passed in.
NETWORK=$1
LND_RPC_HOST=$2
LND_RPC_PORT=$3
BTCD_RPC_HOST=$4
BTCD_RPC_PORT=$5
BTCD_RPC_USER=$6
BTCD_RPC_PASS=$7
SQK_RPC_HOST=$2
SQK_RPC_PORT=$3
PRIVATE_KEY=$8

#define the template.
cat  << EOF

[DEFAULT]
network=$NETWORK

[lnd]
rpc_host=$LND_RPC_HOST
rpc_port=$LND_RPC_PORT

[btcd]
rpc_host=$BTCD_RPC_HOST
rpc_port=$BTCD_RPC_PORT
rpc_user=$BTCD_RPC_USER
rpc_pass=$BTCD_RPC_PASS

[client]
rpc_host=$SQK_RPC_HOST
rpc_port=$SQK_RPC_PORT
private_key=$PRIVATE_KEY

EOF
