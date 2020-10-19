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
import BuyOfferDetailItem from "../../components/BuyOfferDetailItem";
import MakeSqueakDialog from "../../components/MakeSqueakDialog";
import DeleteSqueakDialog from "../../components/DeleteSqueakDialog";

import {
  getBuyOffer,
} from "../../squeakclient/requests"


export default function OfferPage() {
  var classes = useStyles();
  const history = useHistory();
  const { id } = useParams();
  const [offer, setOffer] = useState(null);

  const getOffer = (offerId) => {
      getBuyOffer(offerId, setOffer);
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
            <BuyOfferDetailItem
              key={offer.getOfferId()}
              offer={offer}>
            </BuyOfferDetailItem>
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
