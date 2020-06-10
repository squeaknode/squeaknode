#!/bin/bash

trap "exit" INT TERM
trap "kill 0" EXIT

function mine_blocks {
    while true; do
	printf "Mining 1 block to address: $MINING_ADDRESS ..."
	docker-compose run btcctl generate 1
	sleep 10
    done
}


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

echo "Continue mining blocks, 1 every 10 seconds."
mine_blocks &
echo "Background mining task is in background..."

echo "Running test.sh...."
docker-compose run test ./test.sh

echo "Shutting down itest..."
# docker-compose down --rmi all --volumes
docker-compose down
