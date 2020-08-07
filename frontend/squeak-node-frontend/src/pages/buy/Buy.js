import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {useHistory} from "react-router-dom";
import {
  Grid,
  Button,
  Divider,
  Box,
  Typography,
} from "@material-ui/core";

// styles
import useStyles from "./styles";

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
import SqueakDetailItem from "../../components/SqueakDetailItem";
import BuyOfferItem from "../../components/BuyOfferItem";
import MakeSqueakDialog from "../../components/MakeSqueakDialog";
import DeleteSqueakDialog from "../../components/DeleteSqueakDialog";

import {
  GetSqueakDisplayRequest,
  GetAncestorSqueakDisplaysRequest,
  LoadBuyOffersRequest,
  GetBuyOffersRequest,
} from "../../proto/squeak_admin_pb"
import { SqueakAdminClient } from "../../proto/squeak_admin_grpc_web_pb"

var client = new SqueakAdminClient('http://' + window.location.hostname + ':8080')

export default function BuyPage() {
  var classes = useStyles();
  const history = useHistory();
  const { hash } = useParams();
  const [offers, setOffers] = useState([]);

  const loadOffers = (hash) => {
      var loadBuyOffersRequest = new LoadBuyOffersRequest()
      loadBuyOffersRequest.setSqueakHash(hash);
      console.log(loadBuyOffersRequest);

      client.loadBuyOffers(loadBuyOffersRequest, {}, (err, response) => {
        if (err) {
          console.log(err.message);
          alert('Error loading offers: ' + err.message);
          return;
        }
        console.log(response);
      });
  };
  const getOffers = (hash) => {
      var getBuyOffersRequest = new GetBuyOffersRequest()
      getBuyOffersRequest.setSqueakHash(hash);
      console.log(getBuyOffersRequest);

      client.getBuyOffers(getBuyOffersRequest, {}, (err, response) => {
        if (err) {
          console.log(err.message);
          alert('Error getting offers: ' + err.message);
          return;
        }
        console.log(response);
        console.log(response.getOffersList());
        setOffers(response.getOffersList())
      });
  };

  const goToOfferPage = (offerId) => {
    console.log("Go to offer page for id: " + offerId);
    // history.push("/app/offer/" + offerId);
  };


  useEffect(()=>{
    loadOffers(hash)
  },[hash]);
  useEffect(()=>{
    getOffers(hash)
  },[hash]);

  function OffersContent() {
    return (
      <>
        <Typography variant="h3">
          Offers
        </Typography>
        <div>
          {offers.map(offer =>
            <Box
              p={1}
              key={offer.getOfferId()}
              >
            <BuyOfferItem
              key={offer.getOfferId()}
              handleOfferClick={() => goToOfferPage(offer.getOfferId())}
              offer={offer}>
            </BuyOfferItem>
            </Box>
          )}
        </div>
      </>
    )
  }

  return (
    <>
      <PageTitle title="Buy squeak" />
      {OffersContent()}
    </>
  );
}
