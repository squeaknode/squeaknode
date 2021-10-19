# configuration


#### configs


config | type | valid values | has default | default value | environment variable | description
--- | --- | --- | --- | --- | --- | ---
node.network | string | ['mainnet', 'testnet', 'regtest', 'simnet'] | yes | "testnet" | SQUEAKNODE_NODE_NETWORK | Which network to use.
node.price_msat | int | [0,...] | yes | 10000 | SQUEAKNODE_NODE_PRICE_MSAT | The price to sell squeaks to other peers in millisatoshis.
node.max_squeaks | int | [0,...] | yes | 10000 | SQUEAKNODE_NODE_MAX_SQUEAKS | The absolute maximum number of squeaks allowed in the database.
node.max_squeaks_per_address_in_block_range | int | [0,...] | yes | 1000 | SQUEAKNODE_NODE_MAX_SQUEAKS_PER_ADDRESS_IN_BLOCK_RANGE | The maximum number of squeaks for an individual address in the recent block range.
node.sqk_dir_path | string | | yes | "<USER_HOME>/.sqk" | SQUEAKNODE_NODE_SQK_DIR_PATH | The directory to store application data (only if using sqlite as database backend).
node.log_level | string | | yes | "INFO" | SQUEAKNODE_NODE_LOG_LEVEL | The log level to use.
node.sent_offer_retention_s | int | [0,...] | yes | 86400 | SQUEAKNODE_NODE_SENT_OFFER_RETENTION_S | The amount of time in seconds to keep a sent offer after creation before deleting it.
node.received_offer_retention_s | int | [0,...] | yes | 86400 | SQUEAKNODE_NODE_RECEIVED_OFFER_RETENTION_S | The amount of time in seconds to keep a received offer after download before deleting it.
node.subscribe_invoices_retry_s | int | [0,...] | yes | 10 | SQUEAKNODE_NODE_SUBSCRIBE_INVOICES_RETRY_S | The amount of time in seconds to wait after a subscription failure to retry subscribing settled invoices.
node.squeak_retention_s | int | [0,...] | yes | 604800 | SQUEAKNODE_NODE_SQUEAK_RETENTION_S | The amount of time in seconds to keep a squeak after download before deleting it.
node.squeak_deletion_interval_s | int | [0,...] | yes | 10 | SQUEAKNODE_NODE_SQUEAK_DELETION_INTERVAL_S | The amount of time in seconds to wait in between deleting old squeaks.
node.offer_deletion_interval_s | int | [0,...] | yes | 10 | SQUEAKNODE_NODE_OFFER_DELETION_INTERVAL_S | The amount of time in seconds to wait in between deleting old offers.
node.interest_block_interval | int | [0,...] | yes | 2016 | SQUEAKNODE_NODE_INTEREST_BLOCK_INTERVAL | The number of blocks (starting from the most recent and descending) that this node will attempt to find squeaks with matching block height.
node.external_address | string | | yes | "" | SQUEAKNODE_NODE_EXTERNAL_ADDRESS | The address that other nodes should use to open a connection to this node.
bitcoin.rpc_host | string | | yes | "localhost" | SQUEAKNODE_BITCOIN_RPC_HOST | The host of the bitcoin node to connect.
bitcoin.rpc_port | int | | yes | 18334 | SQUEAKNODE_BITCOIN_RPC_HOST | The port of the bitcoin node to connect.
bitcoin.rpc_user | string | | yes | "" | SQUEAKNODE_BITCOIN_RPC_USER | The username to use for authentication on the bitcoin node.
bitcoin.rpc_pass | string | | yes | "" | SQUEAKNODE_BITCOIN_RPC_PASS | The password to use for authentication on the bitcoin node.
bitcoin.rpc_use_ssl | boolean | [true, false] | yes | false | SQUEAKNODE_BITCOIN_USE_SSL | Use SSL for the connection to the bitcoin node.
bitcoin.rpc_ssl_cert | str |  | yes | "" | SQUEAKNODE_BITCOIN_SSL_CERT | The path to the SSL cert to use for connection to the bitcoin node.
bitcoin.zeromq_hashblock_port | int | | yes | 28334 | SQUEAKNODE_BITCOIN_ZEROMQ_HASHBLOCK_PORT | The port to use to subscribe with zeromq to new block hashes on the bitcoin node.
lnd.host | string | | yes | "localhost" | SQUEAKNODE_LND_HOST | The host of the LND node to connect.
lnd.external_host | string | | yes | "" | SQUEAKNODE_LND_EXTERNAL_HOST | The host of the LND node to share with other peers.
lnd.port | int | | yes | | SQUEAKNODE_LND_PORT | The port of the LND node to use for LND peer connections.
lnd.rpc_port | int | | yes | | SQUEAKNODE_LND_RPC_PORT | The port of the LND node to use for RPC connections.
lnd.tls_cert_path | string | | yes | "" | SQUEAKNODE_LND_TLS_CERT_PATH | The path to the TLS certificate to use for LND connection.
lnd.macaroon_path | string | | yes | "" | SQUEAKNODE_LND_MACAROON_PATH | The path to the macaroon to use for LND connection.
