import React from 'react';
import {
  Typography,
  Grid,
  Box,
  Link,
} from '@material-ui/core';
import { useHistory } from 'react-router-dom';

// styles
import moment from 'moment';

import {
  goToPeerAddressPage,
  goToLightningNodePage,
} from '../../navigation/navigation';

export default function BuyOfferDetailItem({
  offer,
  ...props
}) {
  const history = useHistory();

  const onPeerClick = (event) => {
    event.preventDefault();
    goToPeerAddressPage(
      history,
      offer.getPeerAddress().getNetwork(),
      offer.getPeerAddress().getHost(),
      offer.getPeerAddress().getPort(),
    );
  };

  const onLightningNodeClick = (event) => {
    event.preventDefault();
    goToLightningNodePage(
      history,
      offer.getNodePubkey(),
      offer.getNodeHost(),
      offer.getNodePort(),
    );
  };

  function OfferContent() {
    return (
      <Typography
        variant="h4"
      >
        Price:
        {' '}
        {offer.getPriceMsat() / 1000}
        {' '}
        sats
      </Typography>
    );
  }

  function PeerInfoContent() {
    console.log(offer);
    const peerAddress = offer.getPeerAddress();
    const peerAddressText = `${peerAddress.getHost()}:${peerAddress.getPort()}`;
    return (
      <Box>
        <Typography
          size="md"
        >
          Peer:
          {' '}
          <Link href="#" onClick={onPeerClick}>
            {peerAddressText}
          </Link>
        </Typography>
      </Box>
    );
  }

  function ExpiresInfoContent(offer) {
    const invoiceTime = offer.getInvoiceTimestamp();
    const invoiceExpiry = offer.getInvoiceExpiry();
    const expireTime = invoiceTime + invoiceExpiry;
    return (
      <Box>
        <Typography
          size="md"
        >
          Expires:
          {' '}
          {moment(expireTime * 1000).fromNow()}
        </Typography>
      </Box>
    );
  }

  function LightningPeerInfoContent(offer) {
    const lightningAddress = `${offer.getNodeHost()}:${offer.getNodePort()}`;
    const lightningPubkey = offer.getNodePubkey();
    return (
      <Box>
        <Typography
          size="md"
        >
          Lightning Node:
          {' '}
          <Link href="#" onClick={onLightningNodeClick}>
            {`${lightningPubkey}@${lightningAddress}`}
          </Link>
        </Typography>
      </Box>
    );
  }

  return (
    <>
      <Box
        p={1}
        m={0}
        style={{ backgroundColor: 'white' }}
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
  );
}
