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
  getBuyOffersRequest,
  syncSqueakRequest,
} from "../../squeakclient/requests"
import {BUY_VIEW, navigateTo, OFFER_VIEW, PROFILE_VIEW} from "../../navigation/routes";


export default function BuyPage() {
  var classes = useStyles();
  const history = useHistory();
  const { hash } = useParams();
  const [offers, setOffers] = useState([]);

  const getOffers = (hash) => {
      getBuyOffersRequest(hash, setOffers);
  };

  const reloadRoute = () => {
    history.go(0);
  };

  const onDownloadClick = (event) => {
    event.preventDefault();
    console.log("Handling download click...");
    // goToBuyPage(squeak.getSqueakHash());
    console.log("syncSqueakRequest with hash: " + hash);
    syncSqueakRequest(hash, (response) => {
      console.log("response:");
      console.log(response);
      reloadRoute();
    });
  }

  useEffect(()=>{
    getOffers(hash)
  },[hash]);

  function OffersContent() {
    return (
      <>
        <Typography variant="h3">
          Offers
        </Typography>
        <Button
          variant="contained"
          onClick={onDownloadClick}
          >Load offers
        </Button>
        <div>
          {offers.map(offer =>
            <Box
              p={1}
              key={offer.getOfferId()}
              >
            <BuyOfferItem
              key={offer.getOfferId()}
              handleOfferClick={() => navigateTo(history, OFFER_VIEW, [offer.getOfferId()])}
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
