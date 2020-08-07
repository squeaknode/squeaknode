import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {useHistory} from "react-router-dom";
import {
  Grid,
  Button,
  Divider,
  Box,
} from "@material-ui/core";

// styles
import useStyles from "./styles";

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
import SqueakDetailItem from "../../components/SqueakDetailItem";
import SqueakThreadItem from "../../components/SqueakThreadItem";
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

  const goToSqueakPage = (hash) => {
    history.push("/app/squeak/" + hash);
  };


  useEffect(()=>{
    loadOffers(hash)
  },[hash]);
  useEffect(()=>{
    getOffers(hash)
  },[hash]);


  return (
    <>
      <PageTitle title="Buy squeak" />
      Hello
    </>
  );
}
