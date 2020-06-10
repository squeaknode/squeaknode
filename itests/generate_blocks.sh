#!/bin/bash


while true; do
    alice_address=$(docker exec -it lnd_alice lncli --network=simnet newaddress np2wkh | jq .address -r)
    MINING_ADDRESS=$alice_address docker-compose up -d btcd
    echo "Mining 1 blocks to address: $alice_address ..."
    docker-compose run btcctl generate 400
    sleep 10
done
