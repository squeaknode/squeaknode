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
  GetBuyOfferRequest,
} from "../../proto/squeak_admin_pb"
import { client } from "../../squeakclient/squeakclient"


export default function OfferPage() {
  var classes = useStyles();
  const history = useHistory();
  const { id } = useParams();
  const [offer, setOffer] = useState(null);

  const getOffer = (offerId) => {
      console.log("Getting offer with offerId: " + offerId);
      var getBuyOfferRequest = new GetBuyOfferRequest()
      getBuyOfferRequest.setOfferId(offerId);
      console.log(getBuyOfferRequest);

      client.getBuyOffer(getBuyOfferRequest, {}, (err, response) => {
        if (err) {
          console.log(err.message);
          alert('Error getting offer: ' + err.message);
          return;
        }
        console.log(response);
        console.log(response.getOffer());
        setOffer(response.getOffer())
      });
  };

  useEffect(()=>{
    getOffer(id)
  },[id]);

  function OfferContent() {
    return (
      <>
        <div>
            <Box
              p={1}
              key={offer.getOfferId()}
              >
            <BuyOfferItem
              key={offer.getOfferId()}
              offer={offer}>
            </BuyOfferItem>
            </Box>
        </div>
      </>
    )
  }

  function NoOfferContent() {
    return (
      <p>
        No offer loaded
      </p>
    )
  }

  return (
    <>
      <PageTitle title="Offer" />
      {offer
        ? OfferContent()
        : NoOfferContent()
      }
    </>
  );
}
