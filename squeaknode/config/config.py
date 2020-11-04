import logging
from configparser import ConfigParser
from os import environ


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

        for key, value in self._configs.items():
            setattr(self, key, value)

    @property
    def configs(self):
        return self._configs

    def __repr__(self):
        return repr(self._configs)

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
