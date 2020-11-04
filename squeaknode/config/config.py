import logging
from configparser import ConfigParser
from os import environ

import pprint

logger = logging.getLogger(__name__)


class Config:

    def __init__(self, config_path):
        # Get the config object
        self.parser = ConfigParser()
        self.parser.read(config_path)
        self._configs = dict()

        self._configs['foobar'] = 123

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

        for key, value in self._configs.items():
            setattr(self, key, value)

    @property
    def configs(self):
        return self._configs

    def __repr__(self):
        return pprint.pformat(self._configs)

    def _get_bitcoin_rpc_host(self):
        return self.parser["bitcoin"]["rpc_host"]

    def _get_bitcoin_rpc_port(self):
        return self.parser["bitcoin"]["rpc_port"]

    def _get_bitcoin_rpc_user(self):
        return self.parser["bitcoin"]["rpc_user"]

    def _get_bitcoin_rpc_pass(self):
        return self.parser["bitcoin"]["rpc_pass"]

    def _get_lnd_host(self):
        return self.parser["lnd"]["host"]

    def _get_lnd_external_host(self):
        return environ.get('EXTERNAL_LND_HOST') \
            or self.parser.get("lnd", "external_host", fallback=None)

    def _get_lnd_port(self):
        return int(self.parser["lnd"]["port"])

    def _get_lnd_rpc_port(self):
        return self.parser["lnd"]["rpc_port"]

    def _get_lnd_tls_cert_path(self):
        return self.parser["lnd"]["tls_cert_path"]

    def _get_lnd_macaroon_path(self):
        return self.parser["lnd"]["macaroon_path"]

    def _get_server_rpc_host(self):
        return self.parser["server"]["rpc_host"]

    def _get_server_rpc_port(self):
        return self.parser["server"]["rpc_port"]

    def _get_admin_rpc_host(self):
        return self.parser["admin"]["rpc_host"]

    def _get_admin_rpc_port(self):
        return self.parser["admin"]["rpc_port"]

    def _get_webadmin_enabled(self):
        return self.parser.getboolean("webadmin", "enabled", fallback=False),

    def _get_webadmin_host(self):
        return self.parser.get("webadmin", "host", fallback="0.0.0.0")

    def _get_webadmin_port(self):
        return self.parser.get("webadmin", "port", fallback=12994)

    def _get_webadmin_username(self):
        return self.parser.get("webadmin", "username", fallback="")

    def _get_webadmin_password(self):
        return self.parser.get("webadmin", "password", fallback="")

    def _get_webadmin_use_ssl(self):
        return environ.get('WEBADMIN_USE_SSL') \
            or self.parser.getboolean("webadmin", "use_ssl", fallback=False),

    def _get_webadmin_login_disabled(self):
        return environ.get('WEBADMIN_LOGIN_DISABLED') \
            or self.parser.getboolean("webadmin", "login_disabled", fallback=False),

    def _get_webadmin_allow_cors(self):
        return environ.get('WEBADMIN_ALLOW_CORS') \
            or self.parser.getboolean("webadmin", "allow_cors", fallback=False),
