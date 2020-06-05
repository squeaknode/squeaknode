#define parameters which are passed in.
NETWORK=$1
LND_RPC_HOST=$2
LND_RPC_PORT=$3
SQK_RPC_HOST=$4
SQK_RPC_PORT=$5

#define the template.
cat  << EOF

[DEFAULT]
network=$NETWORK

[lnd]
rpc_host=$LND_RPC_HOST
rpc_port=$LND_RPC_PORT

[electrum]
rpc_host=
rpc_port=
rpc_user=
rpc_pass=

[server]
rpc_host=$SQK_RPC_HOST
rpc_port=$SQK_RPC_PORT

[postgresql]
host=db
database=squeakserver
user=postgres
password=postgres

EOF
