# MIT License
#
# Copyright (c) 2020 Jonathan Zernik
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import mock
import pytest

from squeaknode.config.config import SqueaknodeConfig
from squeaknode.node.squeak_node import SqueakNode


@pytest.fixture()
def mock_lightning_client():
    yield mock.patch('squeaknode.node.squeak_node.LNDLightningClient', autospec=True)


def get_config(config_dict):
    config = SqueaknodeConfig(
        dict_config=config_dict,
    )
    config.read()
    return config


mainnet_config = {
    'node': {
        'network': 'mainnet'
    },
}


webadmin_enabled_config = {
    'node': {
        'network': 'mainnet'
    },
    'webadmin': {
        'enabled': 'true'
    },
}


@pytest.fixture(scope="module", params=[mainnet_config, webadmin_enabled_config])
def squeak_node(request):
    print('--------request.param---------')
    print(request.param)
    with mock.patch('squeaknode.node.squeak_node.LNDLightningClient', autospec=True), \
            mock.patch('squeaknode.node.squeak_node.get_connection_string', autospec=True), \
            mock.patch('squeaknode.node.squeak_node.get_engine', autospec=True), \
            mock.patch('squeaknode.node.squeak_node.SqueakDb', autospec=True):
        config = get_config(request.param)
        yield SqueakNode(config)


def test_start_stop(squeak_node):
    print('--------squeak_node.config---------')
    print(squeak_node.config)
    squeak_node.start_running()
    squeak_node.stop_running()
