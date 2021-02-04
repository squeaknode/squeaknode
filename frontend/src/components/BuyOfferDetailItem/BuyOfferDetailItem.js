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
    const peerHash = getPeerHash();
    if (peerHash == null) {
      return;
    }
    console.log("Handling peer click for peerHash: " + peerHash);
    goToPeerPage(history, peerHash);
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

  const getPeerHash = () => {
    if (!offer.getHasPeer()) {
      return null;
    }
    const peer = offer.getPeer();
    return peer.getPeerHash();
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


  function PeerDisplay() {
    if (offer.getHasPeer()) {
      return HasPeerDisplay(offer.getPeer());
    } else {
      return HasNoPeerDisplay();
    }
  }

  function HasPeerDisplay(peer) {
    const peerHash = peer.getPeerHash();
    const peerName = peer.getPeerName();
    const peerDisplayName = peerName ? peerName : peerHash;
    return (
      <Link href="#"
        onClick={onPeerClick}
        >{peerDisplayName}
      </Link>
    )
  }

  function HasNoPeerDisplay() {
    return (
      <>
        Unknown Peer
      </>
    )
  }


  function ProfileInfoContent() {
    return (
      <Box>
        <Typography
          size="md"
          >Peer: {PeerDisplay()}
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

  function PeerNodeInfoContent(offer) {
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
            {ProfileInfoContent()}
          </Grid>
          </Grid>
          <Grid
            container
            direction="row"
            justify="flex-start"
            alignItems="flex-start"
          >
          <Grid item>
            {PeerNodeInfoContent(offer)}
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
