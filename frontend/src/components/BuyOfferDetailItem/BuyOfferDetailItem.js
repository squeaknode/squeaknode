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
import {LIGHTNING_NODE_PORT_VIEW, navigateTo} from "../../navigation/routes";

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
        >{offer.getPriceMsat()} msats ({offer.getPriceMsat() / 1000} sats)
      </Typography>
    )
  }

  function ProfileInfoContent(peer) {
    return (
      <Box>
        <Typography
          size="md"
          >{peer.getPeerName()}
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
            Expires: {moment(expireTime*1000).fromNow()} ({expireTime})
          </Typography>
      </Box>
    )
  }

  function PeerNodeInfoContent(offer) {
    return (
      <Box>
        <Typography
          size="md"
          >Node Host: {offer.getNodeHost()}
        </Typography>
        <Typography
          size="md"
          >Node Port: {offer.getNodePort()}
        </Typography>
        <Typography
          size="md"
          >Node Pubkey:
          <Link href="#" onClick={() => {
            console.info("I'm a button.");
            navigateTo(
              history,
              LIGHTNING_NODE_PORT_VIEW,
              [offer.getNodePubkey(), offer.getNodeHost(), offer.getNodePort()]
            );
          }}>
            {offer.getNodePubkey()}
          </Link>
        </Typography>

        <Typography size="md">
        {PayOfferButton()}
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
            {ProfileInfoContent(offer.getPeer())}
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
    </Box>
      {PayOfferDialogContent()}
    </>
  )
}
