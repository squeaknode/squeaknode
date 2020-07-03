squeakserver
======

Server for squeak protocol


Test
----

Run unit tests::

    $ make test


Run integration tests::

    $ make itest


Run with docker
---

Edit [docker/config.ini](docker/config.ini) to use your external IP address for `external_host`

Start the squeak server::

    $ cd docker
    $ docker-compose up


Run without docker
---

Create a `config.ini` file and fill in the relevant values::

  [DEFAULT]
  network=testnet

  [lnd]
  host=<YOUR_LND_HOST>
  external_host=<YOUR_LND_HOST>
  port=9735
  rpc_port=10009
  tls_cert_path=/root/.lnd/tls.cert
  macaroon_path=/root/.lnd/data/chain/bitcoin/testnet/admin.macaroon

  [server]
  rpc_host=0.0.0.0
  rpc_port=8774
  price=<YOUR_SELLING_PRICE_IN_SATOSHIS>

  [postgresql]
  host=<YOUR_POSTGRES_HOST>
  database=squeakserver
  user=postgres
  password=postgres


Run the following script on the postgres server to initialize the database::

    $ createdb.sql


Install the server requirements::

    $ pip3 install -r requirements.txt
    $ install-rpc.sh
    $ python3 setup.py install


Start the squeak server::

    $ runsqueakserver --config config.ini run-server
