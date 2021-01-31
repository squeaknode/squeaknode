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

// components
import BuyOfferDialog from "../../components/BuyOfferDialog";

// styles
import useStyles from "./styles";

import Widget from "../../components/Widget";

import moment from 'moment';

export default function BuyOfferDetailItem({
  offer,
  handleOfferClick,
  ...props
}) {
  var classes = useStyles();
  const history = useHistory();
  const [payOfferDialogOpen, setPayOfferDialogOpen] = useState(false);


  const preventDefault = (event) => event.preventDefault();

  const onOfferClick = (event) => {
    event.preventDefault();
    console.log("Handling offer click...");
    if (handleOfferClick) {
      handleOfferClick();
    }
  }

  const onPeerClick = (event) => {
    event.preventDefault();
    const peerId = getPeerId();
    if (peerId == null) {
      return;
    }
    console.log("Handling peer click for peerId: " + peerId);
    goToPeerPage(peerId);
  }

  const getPeerId = () => {
    if (!offer.getHasPeer()) {
      return null;
    }
    const peer = offer.getPeer();
    return peer.getPeerId();
  }

  const goToPeerPage = (peerId) => {
    history.push("/app/peer/" + peerId);
  };

  const goToLightningNodePage = (pubkey, host, port) => {
      console.log("Go to lightning node for pubkey: " + pubkey);
      if (pubkey && host && port) {
        history.push("/app/lightningnode/" + pubkey + "/" + host + "/" + port);
      } else if (pubkey && host) {
        history.push("/app/lightningnode/" + pubkey + "/" + host);
      } else {
        history.push("/app/lightningnode/" + pubkey);
      }
  };

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
    const peerId = peer.getPeerId();
    const peerName = peer.getPeerName();
    const peerDisplayName = peerName ? peerName : peerId;
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
          >Lightning Node: <Link href="#" onClick={() => {
            goToLightningNodePage(
              offer.getNodePubkey(),
              offer.getNodeHost(),
              offer.getNodePort(),
            )
          }}>
            {lightningPubkey + "@" + lightningAddress}
          </Link>
        </Typography>
      </Box>
    )
  }

  function PayOfferButton() {
    return (
      <>
          <Button
            variant="contained"
            onClick={() => {
              handleClickPayOffer();
            }}>Pay Offer
          </Button>
      </>
    )
  }

  function PayOfferDialogContent() {
    return (
      <>
        <BuyOfferDialog
          open={payOfferDialogOpen}
          offer={offer}
          handleClose={handleClosePayOfferDialog}
          ></BuyOfferDialog>
      </>
    )
  }

  return (
    <>
    <Box
      p={1}
      m={0}
      style={{backgroundColor: 'white'}}
      onClick={onOfferClick}
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
      {PayOfferDialogContent()}
    </>
  )
}
