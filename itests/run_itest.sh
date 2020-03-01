#!/bin/bash

cd itests
docker-compose down --volumes
docker-compose build
docker-compose up -d

# Initialize the blockchain with miner rewards going to alice.
sleep 10
alice_address=$(docker exec -it lnd_alice lncli --network=simnet newaddress np2wkh | jq .address -r)
MINING_ADDRESS=$alice_address docker-compose up -d btcd
echo "Mining 400 blocks to address: $alice_address ..."
docker-compose run btcctl generate 400
echo "Finished mining blocks."
sleep 10

echo "Running test.sh...."
docker-compose run test ./test.sh
