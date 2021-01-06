import logging
import pprint
from configparser import ConfigParser
from os import environ
from pathlib import Path
from typing import Optional

from typedconfig import Config
from typedconfig import group_key
from typedconfig import key
from typedconfig import section
from typedconfig.source import EnvironmentConfigSource
from typedconfig.source import IniFileConfigSource

logger = logging.getLogger(__name__)


DEFAULT_NETWORK = "testnet"
DEFAULT_PRICE_MSAT = 10000
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_MAX_SQUEAKS_PER_ADDRESS_PER_HOUR = 100
DEFAULT_SERVER_RPC_HOST = "0.0.0.0"
DEFAULT_SERVER_RPC_PORT = 8774
DEFAULT_ADMIN_RPC_HOST = "0.0.0.0"
DEFAULT_ADMIN_RPC_PORT = 8994
DEFAULT_WEBADMIN_HOST = "0.0.0.0"
DEFAULT_WEBADMIN_PORT = 12994
DEFAULT_BITCOIN_RPC_HOST = "localhost"
DEFAULT_BITCOIN_RPC_PORT = 8334
BITCOIN_RPC_PORT = {
    "mainnet": 8332,
    "testnet": 18332,
    "simnet": 18556,
}
DEFAULT_LND_PORT = 9735
DEFAULT_LND_RPC_PORT = 10009
DEFAULT_SQK_DIR = ".sqk"
DEFAULT_SQK_DIR_PATH = str(Path.home() / DEFAULT_SQK_DIR)
DEFAULT_LND_HOST = "localhost"
DEFAULT_SYNC_INTERVAL_S = 10


@section('bitcoin')
class BitcoinConfig(Config):
    rpc_host = key(cast=str, required=False, default=DEFAULT_BITCOIN_RPC_HOST)
    rpc_port = key(cast=int, required=False, default=DEFAULT_BITCOIN_RPC_PORT)
    rpc_user = key(cast=str, required=False, default="")
    rpc_pass = key(cast=str, required=False, default="")
    rpc_use_ssl = key(cast=bool, required=False, default=False)
    rpc_ssl_cert = key(cast=str, required=False, default="")


@section('lnd')
class LndConfig(Config):
    host = key(cast=str, required=False, default=DEFAULT_LND_HOST)
    external_host = key(cast=str, required=False, default=None)
    port = key(cast=int, required=False, default=DEFAULT_LND_PORT)
    rpc_port = key(cast=int, required=False, default=DEFAULT_LND_RPC_PORT)
    tls_cert_path = key(cast=str, required=False, default=None)
    macaroon_path = key(cast=str, required=False, default=None)


@section('server')
class ServerConfig(Config):
    rpc_host = key(cast=str, required=False, default=DEFAULT_SERVER_RPC_HOST)
    rpc_port = key(cast=int, required=False, default=DEFAULT_SERVER_RPC_PORT)


@section('admin')
class AdminConfig(Config):
    rpc_enabled = key(cast=bool, required=False, default=False)
    rpc_host = key(cast=str, required=False, default=DEFAULT_ADMIN_RPC_HOST)
    rpc_port = key(cast=int, required=False, default=DEFAULT_ADMIN_RPC_PORT)


@section('webadmin')
class WebadminConfig(Config):
    enabled = key(cast=bool, required=False, default=False)
    host = key(cast=str, required=False, default=DEFAULT_WEBADMIN_HOST)
    port = key(cast=int, required=False, default=DEFAULT_WEBADMIN_PORT)
    username = key(cast=str, required=False, default="")
    password = key(cast=str, required=False, default="")
    use_ssl = key(cast=bool, required=False, default=False)
    login_disabled = key(cast=bool, required=False, default=False)
    allow_cors = key(cast=bool, required=False, default=False)


# TODO: Use sqk_dir instead of sqk_dir_path
@section('core')
class CoreConfig(Config):
    network = key(cast=str, required=False, default=DEFAULT_NETWORK)
    price_msat = key(cast=int, required=False, default=DEFAULT_PRICE_MSAT)
    max_squeaks_per_address_per_hour = key(
        cast=int, required=False, default=DEFAULT_MAX_SQUEAKS_PER_ADDRESS_PER_HOUR)
    sqk_dir = key(cast=str, required=False, default=DEFAULT_SQK_DIR_PATH)
    log_level = key(cast=str, required=False, default=DEFAULT_LOG_LEVEL)


@section('sync')
class SyncConfig(Config):
    enabled = key(cast=bool, required=False, default=False)
    interval_s = key(cast=int, required=False, default=DEFAULT_SYNC_INTERVAL_S)


@section('db')
class DbConfig(Config):
    connection_string = key(cast=str, required=False, default="")


class SqueaknodeConfig(Config):
    bitcoin = group_key(BitcoinConfig)
    lnd = group_key(LndConfig)
    server = group_key(ServerConfig)
    admin = group_key(AdminConfig)
    webadmin = group_key(WebadminConfig)
    core = group_key(CoreConfig)
    sync = group_key(SyncConfig)
    db = group_key(DbConfig)
    # description = key(cast=str, section_name="general")

    def __init__(self, config_path=None):
        super().__init__()
        self.prefix = "SQUEAKNODE"
        self.config_path = config_path

    def read(self):
        self.add_source(EnvironmentConfigSource(prefix=self.prefix))
        if self.config_path is not None:
            self.add_source(IniFileConfigSource(self.config_path))
        return super().read()


# class SqueaknodeConfig:
#     def __init__(self, config_path):
#         # Get the config object
#         # self.parser = ConfigParser()
#         # if config_path is not None:
#         #     self.parser.read(config_path)
#         # self._configs = dict()

#         config = SqueaknodeConfig()
#         config.add_source(EnvironmentConfigSource(prefix="SQUEAKNODE"))
#         config.add_source(IniFileConfigSource(config_path))
#         config.read()

#         # Bitcoin
#         self._configs["bitcoin_rpc_host"] = self._get_bitcoin_rpc_host()
#         self._configs["bitcoin_rpc_port"] = self._get_bitcoin_rpc_port()
#         self._configs["bitcoin_rpc_user"] = self._get_bitcoin_rpc_user()
#         self._configs["bitcoin_rpc_pass"] = self._get_bitcoin_rpc_pass()
#         self._configs["bitcoin_rpc_use_ssl"] = self._get_bitcoin_rpc_use_ssl()
#         self._configs["bitcoin_rpc_ssl_cert"] = self._get_bitcoin_rpc_ssl_cert()

#         # lnd
#         self._configs["lnd_host"] = self._get_lnd_host()
#         self._configs["lnd_external_host"] = self._get_lnd_external_host()
#         self._configs["lnd_port"] = self._get_lnd_port()
#         self._configs["lnd_rpc_port"] = self._get_lnd_rpc_port()
#         self._configs["lnd_tls_cert_path"] = self._get_lnd_tls_cert_path()
#         self._configs["lnd_macaroon_path"] = self._get_lnd_macaroon_path()
#         # self._configs["lnd_dir"] = self._get_lnd_dir()

#         # server
#         self._configs["server_rpc_host"] = self._get_server_rpc_host()
#         self._configs["server_rpc_port"] = self._get_server_rpc_port()

#         # admin
#         self._configs["admin_rpc_enabled"] = self._get_admin_rpc_enabled()
#         self._configs["admin_rpc_host"] = self._get_admin_rpc_host()
#         self._configs["admin_rpc_port"] = self._get_admin_rpc_port()

#         # webadmin
#         self._configs["webadmin_enabled"] = self._get_webadmin_enabled()
#         self._configs["webadmin_host"] = self._get_webadmin_host()
#         self._configs["webadmin_port"] = self._get_webadmin_port()
#         self._configs["webadmin_username"] = self._get_webadmin_username()
#         self._configs["webadmin_password"] = self._get_webadmin_password()
#         self._configs["webadmin_use_ssl"] = self._get_webadmin_use_ssl()
#         self._configs["webadmin_login_disabled"] = self._get_webadmin_login_disabled()
#         self._configs["webadmin_allow_cors"] = self._get_webadmin_allow_cors()

#         # squeaknode
#         self._configs["squeaknode_network"] = self._get_squeaknode_network()
#         self._configs["squeaknode_price_msat"] = self._get_squeaknode_price_msat()
#         self._configs[
#             "squeaknode_max_squeaks_per_address_per_hour"
#         ] = self._get_squeaknode_max_squeaks_per_address_per_hour()
#         self._configs["squeaknode_sqk_dir"] = self._get_squeaknode_sqk_dir()
#         self._configs["squeaknode_log_level"] = self._get_squeaknode_log_level()

#         # sync
#         self._configs["sync_enabled"] = self._get_sync_enabled()
#         self._configs["sync_interval_s"] = self._get_sync_interval_s()

#         # db
#         self._configs["db_connection_string"] = self._get_db_connection_string()

#         for key, value in self._configs.items():
#             setattr(self, key, value)

#     @property
#     def configs(self):
#         return self._configs

#     def __repr__(self):
#         return pprint.pformat(self._configs)

#     def _get_bitcoin_rpc_host(self):
#         return environ.get("SQUEAKNODE_BITCOIND_HOST") or self.parser.get(
#             "bitcoin", "rpc_host", fallback="localhost"
#         )

#     def _get_bitcoin_rpc_port(self):
#         network = self._get_squeaknode_network()
#         default_rpc_port = BITCOIN_RPC_PORT.get(
#             network, DEFAULT_BITCOIN_RPC_PORT)
#         return int(
#             environ.get("SQUEAKNODE_BITCOIND_PORT") or 0
#         ) or self.parser.getint(
#             "bitcoin", "rpc_port", fallback=default_rpc_port
#         )

#     def _get_bitcoin_rpc_user(self):
#         return environ.get("SQUEAKNODE_BITCOIND_USER") or self.parser.get(
#             "bitcoin", "rpc_user", fallback=""
#         )

#     def _get_bitcoin_rpc_pass(self):
#         return environ.get("SQUEAKNODE_BITCOIND_PASS") or self.parser.get(
#             "bitcoin", "rpc_pass", fallback=""
#         )

#     def _get_bitcoin_rpc_use_ssl(self):
#         return self.parser.getboolean("bitcoin", "rpc_use_ssl", fallback=False)

#     def _get_bitcoin_rpc_ssl_cert(self):
#         return self.parser.get("bitcoin", "rpc_ssl_cert", fallback=None)

#     def _get_lnd_host(self):
#         return environ.get("SQUEAKNODE_LND_HOST") or self.parser.get(
#             "lnd", "host", fallback=DEFAULT_LND_HOST
#         )

#     def _get_lnd_external_host(self):
#         return environ.get("SQUEAKNODE_EXTERNAL_LND_HOST") or self.parser.get(
#             "lnd", "external_host", fallback=None
#         )

#     def _get_lnd_port(self):
#         return int(
#             environ.get("SQUEAKNODE_LND_PORT") or 0
#         ) or self.parser.getint("lnd", "port", fallback=DEFAULT_LND_PORT)

#     def _get_lnd_rpc_port(self):
#         return int(
#             environ.get("SQUEAKNODE_LND_GRPC_PORT") or 0
#         ) or self.parser.getint("lnd", "rpc_port", fallback=DEFAULT_LND_RPC_PORT)

#     def _get_lnd_tls_cert_path(self):
#         env_val = environ.get("SQUEAKNODE_LND_TLS_CERT_PATH")
#         if env_val:
#             return env_val
#         lnd_dir_path = self._get_lnd_dir()
#         tls_cert_path = str(Path(lnd_dir_path) / DEFAULT_LND_TLS_CERT_NAME)
#         return self.parser.get("lnd", "tls_cert_path", fallback=tls_cert_path)

#     def _get_lnd_macaroon_path(self):
#         env_val = environ.get("SQUEAKNODE_LND_MACAROON_PATH")
#         if env_val:
#             return env_val
#         lnd_dir_path = self._get_lnd_dir()
#         network = self._get_squeaknode_network()
#         lnd_network_dir = "data/chain/bitcoin/{}".format(network)
#         macaroon_path = str(
#             Path(lnd_dir_path) / lnd_network_dir / DEFAULT_LND_MACAROON_NAME
#         )
#         return self.parser.get("lnd", "macaroon_path", fallback=macaroon_path)

#     def _get_lnd_dir(self):
#         return self.parser.get("lnd", "lnd_dir", fallback=DEFAULT_LND_DIR_PATH)

#     def _get_server_rpc_host(self):
#         return self.parser.get("server", "rpc_host", fallback=DEFAULT_SERVER_RPC_HOST)

#     def _get_server_rpc_port(self):
#         return self.parser.get("server", "rpc_port", fallback=DEFAULT_SERVER_RPC_PORT)

#     def _get_admin_rpc_enabled(self):
#         return environ.get("SQUEAKNODE_ADMIN_RPC_ENABLED") or self.parser.getboolean(
#             "admin", "rpc_enabled", fallback=False)

#     def _get_admin_rpc_host(self):
#         return self.parser.get("admin", "rpc_host", fallback=ADMIN_RPC_HOST)

#     def _get_admin_rpc_port(self):
#         return self.parser.get("admin", "rpc_port", fallback=ADMIN_RPC_PORT)

#     def _get_webadmin_enabled(self):
#         return environ.get("SQUEAKNODE_WEBADMIN_ENABLED") or self.parser.getboolean(
#             "webadmin", "enabled", fallback=False
#         )

#     def _get_webadmin_host(self):
#         return self.parser.get("webadmin", "host", fallback=DEFAULT_WEBADMIN_HOST)

#     def _get_webadmin_port(self):
#         return self.parser.get("webadmin", "port", fallback=DEFAULT_WEBADMIN_PORT)

#     def _get_webadmin_username(self):
#         return environ.get("SQUEAKNODE_WEBADMIN_USERNAME") or self.parser.get(
#             "webadmin", "username", fallback=""
#         )

#     def _get_webadmin_password(self):
#         return environ.get("SQUEAKNODE_WEBADMIN_PASSWORD") or self.parser.get(
#             "webadmin", "password", fallback=""
#         )

#     def _get_webadmin_use_ssl(self):
#         return environ.get("SQUEAKNODE_WEBADMIN_USE_SSL") or self.parser.getboolean(
#             "webadmin", "use_ssl", fallback=False
#         )

#     def _get_webadmin_login_disabled(self):
#         return environ.get("SQUEAKNODE_WEBADMIN_LOGIN_DISABLED") or self.parser.getboolean(
#             "webadmin", "login_disabled", fallback=False
#         )

#     def _get_webadmin_allow_cors(self):
#         return environ.get("SQUEAKNODE_WEBADMIN_ALLOW_CORS") or self.parser.getboolean(
#             "webadmin", "allow_cors", fallback=False
#         )

#     def _get_squeaknode_network(self):
#         return environ.get("SQUEAKNODE_NETWORK") or self.parser.get(
#             "squeaknode", "network", fallback="testnet"
#         )

#     def _get_squeaknode_price_msat(self):
#         return int(
#             environ.get("SQUEAKNODE_PRICE_MSAT") or 0
#         ) or int(self.parser.get("squeaknode", "price_msat", fallback="10000"))

#     def _get_squeaknode_max_squeaks_per_address_per_hour(self):
#         return int(
#             self.parser.get(
#                 "squeaknode", "max_squeaks_per_address_per_hour", fallback="100"
#             )
#         )

#     def _get_squeaknode_database(self):
#         return self.parser.get("squeaknode", "database", fallback="sqlite")

#     def _get_squeaknode_sqk_dir(self):
#         return environ.get("SQUEAKNODE_SQK_DIR_PATH") or self.parser.get(
#             "squeaknode", "sqk_dir", fallback=DEFAULT_SQK_DIR_PATH
#         )

#     def _get_sync_enabled(self):
#         return environ.get("SQUEAKNODE_SYNC_ENABLED") or self.parser.getboolean(
#             "sync", "enabled", fallback=True)

#     def _get_sync_interval_s(self):
#         return int(
#             environ.get("SQUEAKNODE_SYNC_INTERVAL_S") or 0
#         ) or self.parser.getint("sync", "interval_s", fallback=DEFAULT_SYNC_INTERVAL_S)

#     def _get_squeaknode_log_level(self):
#         return environ.get("LOG_LEVEL") or self.parser.get(
#             "squeaknode", "log_level", fallback="INFO"
#         )

#     def _get_db_connection_string(self):
#         return environ.get("DB_CONNECTION_STRING") or self.parser.get(
#             "db", "connection_string", fallback=None
#         )
