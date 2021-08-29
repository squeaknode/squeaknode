import React from 'react';
import {
  Typography,
  Grid,
  Box,
} from '@material-ui/core';
import { useHistory } from 'react-router-dom';

// styles
import moment from 'moment';
import useStyles from './styles';

export default function BuyOfferItem({
  offer,
  handleOfferClick,
  ...props
}) {
  const classes = useStyles();

  const history = useHistory();

  const onOfferClick = (event) => {
    event.preventDefault();
    console.log('Handling offer click...');
    if (handleOfferClick) {
      handleOfferClick();
    }
  };

  function OfferContent() {
    return (
      <Typography
        size="md"
      >
        {offer.getPriceMsat()}
        {' '}
        msats (
        {offer.getPriceMsat() / 1000}
        {' '}
        sats)
      </Typography>
    );
  }

  function ProfileInfoContent(peer) {
    return (
      <Box>
        <Typography
          size="md"
        >
          {peer.getPeerName()}
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

  return (
    <Box
      p={1}
      m={0}
      style={{ backgroundColor: 'white' }}
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
    </Box>
  );
}
