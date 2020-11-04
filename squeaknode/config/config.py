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
        self._configs['bitcoin_rpc_host'] = self._get_bitcoin_rpc_host()
        self._configs['bitcoin_rpc_port'] = self._get_bitcoin_rpc_port()
        self._configs['bitcoin_rpc_user'] = self._get_bitcoin_rpc_user()
        self._configs['bitcoin_rpc_pass'] = self._get_bitcoin_rpc_pass()

        for key, value in self._configs.items():
            setattr(self, key, value)

    @property
    def configs(self):
        return self._configs

    def _get_bitcoin_rpc_host(self):
        return self.parser["bitcoin"]["rpc_host"]

    def _get_bitcoin_rpc_port(self):
        return self.parser["bitcoin"]["rpc_port"]

    def _get_bitcoin_rpc_user(self):
        return self.parser["bitcoin"]["rpc_user"]

    def _get_bitcoin_rpc_pass(self):
        return self.parser["bitcoin"]["rpc_pass"]
