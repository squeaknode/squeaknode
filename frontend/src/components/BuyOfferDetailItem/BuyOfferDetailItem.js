import React, { useState } from "react";
import {
  Paper,
  Button,
  IconButton,
  Menu,
  MenuItem,
  Typography,
  Grid,
  Box,
  Link,
} from "@material-ui/core";
import { MoreVert as MoreIcon } from "@material-ui/icons";
import {useHistory} from "react-router-dom";
import classnames from "classnames";

import LockIcon from '@material-ui/icons/Lock';

// styles
import useStyles from "./styles";

import Widget from "../../components/Widget";

import moment from 'moment';

import {
  goToPeerPage,
  goToPeerAddressPage,
  goToLightningNodePage,
} from "../../navigation/navigation"

export default function BuyOfferDetailItem({
  offer,
  ...props
}) {
  var classes = useStyles();
  const history = useHistory();
  const [payOfferDialogOpen, setPayOfferDialogOpen] = useState(false);

  const preventDefault = (event) => event.preventDefault();

  const onPeerClick = (event) => {
    event.preventDefault();
    goToPeerAddressPage(
      history,
      offer.getPeerAddress().getHost(),
      offer.getPeerAddress().getPort(),
    );
  }

  const onLightningNodeClick = (event) => {
    event.preventDefault();
    goToLightningNodePage(
      history,
      offer.getNodePubkey(),
      offer.getNodeHost(),
      offer.getNodePort(),
    )
  }

  const handleClickPayOffer = () => {
    console.log("Handle click pay offer.");
    setPayOfferDialogOpen(true);
  };

  const handleClosePayOfferDialog = () => {
    setPayOfferDialogOpen(false);
  };

  function OfferContent() {
    return (
      <Typography
        size="md"
        >Price: {offer.getPriceMsat() / 1000} sats
      </Typography>
    )
  }

  function PeerInfoContent() {
    console.log(offer);
    const peerAddress =  offer.getPeerAddress();
    const host = peerAddress.getHost();
    const peerAddressText =  peerAddress.getHost() + ":" + peerAddress.getPort();
    return (
      <Box>
        <Typography
          size="md"
          >Peer: <Link href="#" onClick={onPeerClick}>
            {peerAddressText}
          </Link>
        </Typography>
      </Box>
    )
  }

  function ExpiresInfoContent(offer) {
    var invoiceTime = offer.getInvoiceTimestamp();
    var invoiceExpiry = offer.getInvoiceExpiry();
    var expireTime = invoiceTime + invoiceExpiry;
    return (
      <Box>
        <Typography
          size="md"
          >
            Expires: {moment(expireTime*1000).fromNow()}
          </Typography>
      </Box>
    )
  }

  function LightningPeerInfoContent(offer) {
    const lightningAddress =  offer.getNodeHost() + ":" + offer.getNodePort();
    const lightningPubkey = offer.getNodePubkey();
    return (
      <Box>
        <Typography
          size="md"
          >Lightning Node: <Link href="#" onClick={onLightningNodeClick}>
            {lightningPubkey + "@" + lightningAddress}
          </Link>
        </Typography>
      </Box>
    )
  }

  return (
    <>
    <Box
      p={1}
      m={0}
      style={{backgroundColor: 'white'}}
      >
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
          >
          <Grid item>
            {OfferContent()}
          </Grid>
          </Grid>
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
          >
          <Grid item>
            {PeerInfoContent()}
          </Grid>
          </Grid>
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
          >
          <Grid item>
            {LightningPeerInfoContent(offer)}
          </Grid>
          </Grid>
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
          >
          <Grid item>
            {ExpiresInfoContent(offer)}
          </Grid>
          </Grid>
    </Box>
    </>
  )
}
