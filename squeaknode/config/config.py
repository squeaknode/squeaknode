import logging
from configparser import ConfigParser
from os import environ

import pprint

logger = logging.getLogger(__name__)


SERVER_RPC_HOST = "0.0.0.0"
SERVER_RPC_PORT = 8774
ADMIN_RPC_HOST = "0.0.0.0"
ADMIN_RPC_PORT = 8994
WEBADMIN_HOST = "0.0.0.0"
WEBADMIN_PORT = 12994
DEFAULT_BITCOIN_RPC_PORT = 8334
BITCOIN_RPC_PORT = {
    'mainnet': 8334,
    'testnet': 18334,
    'simnet': 18556,
}
DEFAULT_LND_PORT = 9735
DEFAULT_LND_RPC_PORT = 10009
POSTGRES_HOST = "localhost"
POSTGRES_DATABASE = "squeaknode"


class Config:

    def __init__(self, config_path):
        # Get the config object
        self.parser = ConfigParser()
        self.parser.read(config_path)
        self._configs = dict()

        # bitcoin
        self._configs['bitcoin_rpc_host'] = self._get_bitcoin_rpc_host()
        self._configs['bitcoin_rpc_port'] = self._get_bitcoin_rpc_port()
        self._configs['bitcoin_rpc_user'] = self._get_bitcoin_rpc_user()
        self._configs['bitcoin_rpc_pass'] = self._get_bitcoin_rpc_pass()

        #lnd
        self._configs['lnd_host'] = self._get_lnd_host()
        self._configs['lnd_external_host'] = self._get_lnd_external_host()
        self._configs['lnd_port'] = self._get_lnd_port()
        self._configs['lnd_rpc_port'] = self._get_lnd_rpc_port()
        self._configs['lnd_tls_cert_path'] = self._get_lnd_tls_cert_path()
        self._configs['lnd_macaroon_path'] = self._get_lnd_macaroon_path()

        # server
        self._configs['server_rpc_host'] = self._get_server_rpc_host()
        self._configs['server_rpc_port'] = self._get_server_rpc_port()

        # admin
        self._configs['admin_rpc_host'] = self._get_admin_rpc_host()
        self._configs['admin_rpc_port'] = self._get_admin_rpc_port()

        # webadmin
        self._configs['webadmin_enabled'] = self._get_webadmin_enabled()
        self._configs['webadmin_host'] = self._get_webadmin_host()
        self._configs['webadmin_port'] = self._get_webadmin_port()
        self._configs['webadmin_username'] = self._get_webadmin_username()
        self._configs['webadmin_password'] = self._get_webadmin_password()
        self._configs['webadmin_use_ssl'] = self._get_webadmin_use_ssl()
        self._configs['webadmin_login_disabled'] = self._get_webadmin_login_disabled()
        self._configs['webadmin_allow_cors'] = self._get_webadmin_allow_cors()

        # squeaknode
        self._configs['squeaknode_network'] = self._get_squeaknode_network()
        self._configs['squeaknode_price'] = self._get_squeaknode_price()
        self._configs['squeaknode_max_squeaks_per_address_per_hour'] = self._get_squeaknode_max_squeaks_per_address_per_hour()
        self._configs['squeaknode_database'] = self._get_squeaknode_database()
        self._configs['squeaknode_sqk_dir'] = self._get_squeaknode_sqk_dir()
        self._configs['squeaknode_enable_sync'] = self._get_squeaknode_enable_sync()

        # postgresql
        self._configs['postgresql_user'] = self._get_postgresql_user()
        self._configs['postgresql_password'] = self._get_postgresql_password()
        self._configs['postgresql_host'] = self._get_postgresql_host()
        self._configs['postgresql_database'] = self._get_postgresql_database()

        for key, value in self._configs.items():
            setattr(self, key, value)

    @property
    def configs(self):
        return self._configs

    def __repr__(self):
        return pprint.pformat(self._configs)

    def _get_bitcoin_rpc_host(self):
        return self.parser.get("bitcoin", "rpc_host", fallback="localhost")

    def _get_bitcoin_rpc_port(self):
        network = self._get_squeaknode_network()
        default_rpc_port = BITCOIN_RPC_PORT.get(network, DEFAULT_BITCOIN_RPC_PORT)
        return self.parser.getint("bitcoin", "rpc_port", fallback=default_rpc_port)

    def _get_bitcoin_rpc_user(self):
        return self.parser.get("bitcoin", "rpc_user")

    def _get_bitcoin_rpc_pass(self):
        return self.parser.get("bitcoin", "rpc_pass")

    def _get_lnd_host(self):
        return self.parser.get("lnd", "host")

    def _get_lnd_external_host(self):
        return environ.get('EXTERNAL_LND_HOST') \
            or self.parser.get("lnd", "external_host", fallback=None)

    def _get_lnd_port(self):
        return self.parser.getint("lnd", "port", fallback=DEFAULT_LND_PORT)

    def _get_lnd_rpc_port(self):
        return self.parser.getint("lnd", "rpc_port", fallback=DEFAULT_LND_RPC_PORT)

    def _get_lnd_tls_cert_path(self):
        return self.parser.get("lnd", "tls_cert_path")

    def _get_lnd_macaroon_path(self):
        return self.parser.get("lnd", "macaroon_path")

    def _get_server_rpc_host(self):
        return self.parser.get("server", "rpc_host", fallback=SERVER_RPC_HOST)

    def _get_server_rpc_port(self):
        return self.parser.get("server", "rpc_port", fallback=SERVER_RPC_PORT)

    def _get_admin_rpc_host(self):
        return self.parser.get("admin", "rpc_host", fallback=ADMIN_RPC_HOST)

    def _get_admin_rpc_port(self):
        return self.parser.get("admin", "rpc_port", fallback=ADMIN_RPC_PORT)

    def _get_webadmin_enabled(self):
        return self.parser.getboolean("webadmin", "enabled", fallback=False)

    def _get_webadmin_host(self):
        return self.parser.get("webadmin", "host", fallback=WEBADMIN_HOST)

    def _get_webadmin_port(self):
        return self.parser.get("webadmin", "port", fallback=WEBADMIN_PORT)

    def _get_webadmin_username(self):
        return self.parser.get("webadmin", "username", fallback="")

    def _get_webadmin_password(self):
        return self.parser.get("webadmin", "password", fallback="")

    def _get_webadmin_use_ssl(self):
        return environ.get('WEBADMIN_USE_SSL') \
            or self.parser.getboolean("webadmin", "use_ssl", fallback=False)

    def _get_webadmin_login_disabled(self):
        return environ.get('WEBADMIN_LOGIN_DISABLED') \
            or self.parser.getboolean("webadmin", "login_disabled", fallback=False)

    def _get_webadmin_allow_cors(self):
        return environ.get('WEBADMIN_ALLOW_CORS') \
            or self.parser.getboolean("webadmin", "allow_cors", fallback=False)

    def _get_squeaknode_network(self):
        return self.parser.get("squeaknode", "network", fallback="testnet")

    def _get_squeaknode_price(self):
        return int(self.parser.get("squeaknode", "price", fallback="10"))

    def _get_squeaknode_max_squeaks_per_address_per_hour(self):
        return int(self.parser.get("squeaknode", "max_squeaks_per_address_per_hour", fallback="100"))

    def _get_squeaknode_database(self):
        return self.parser.get("squeaknode", "database", fallback="sqlite")

    def _get_squeaknode_sqk_dir(self):
        return self.parser.get("squeaknode", "sqk_dir", fallback=None)

    def _get_squeaknode_enable_sync(self):
        return self.parser.getboolean("squeaknode", "enable_sync", fallback=False)

    def _get_postgresql_user(self):
        return self.parser.get("postgresql", "user", fallback="")

    def _get_postgresql_password(self):
        return self.parser.get("postgresql", "password", fallback="")

    def _get_postgresql_host(self):
        return self.parser.get("postgresql", "host", fallback=POSTGRES_HOST)

    def _get_postgresql_database(self):
        return self.parser.get("postgresql", "database", fallback=POSTGRES_DATABASE)
