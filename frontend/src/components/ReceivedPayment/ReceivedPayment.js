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
  goToSqueakPage,
  goToPeerAddressPage,
} from '../../navigation/navigation';

export default function ReceivedPayment({
  receivedPayment,
  ...props
}) {

  const history = useHistory();

  const onSqueakClick = (event) => {
    event.preventDefault();
    const hash = receivedPayment.getSqueakHash();
    console.log(`Handling squeak click for hash: ${hash}`);
    goToSqueakPage(history, hash);
  };

  const onPeerClick = (event) => {
    event.preventDefault();
    goToPeerAddressPage(
      history,
      receivedPayment.getPeerAddress().getHost(),
      receivedPayment.getPeerAddress().getPort(),
    );
  };

  function PeerDisplay() {
    const peerAddress = receivedPayment.getPeerAddress();
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

  console.log('receivedPayment:');
  console.log(receivedPayment);
  return (
    <Box
      p={1}
      m={0}
      style={{ backgroundColor: 'lightgray' }}
    >
      <Grid
        container
        direction="row"
        justify="flex-start"
        alignItems="flex-start"
      >
        <Grid item>
          <Box fontWeight="fontWeightBold">
            {receivedPayment.getPriceMsat()}
            {' '}
            msats
          </Box>
        </Grid>
      </Grid>
      <Grid
        container
        direction="row"
        justify="flex-start"
        alignItems="flex-start"
      >
        <Grid item>
          {moment(receivedPayment.getTimeS() * 1000).format('DD MMM YYYY hh:mm a')}
        </Grid>
      </Grid>
      <Grid
        container
        direction="row"
        justify="flex-start"
        alignItems="flex-start"
      >
        <Grid item>
          Squeak hash:
          <Link
            href="#"
            onClick={onSqueakClick}
          >
            <span> </span>
            {receivedPayment.getSqueakHash()}
          </Link>
        </Grid>
      </Grid>
      <Grid
        container
        direction="row"
        justify="flex-start"
        alignItems="flex-start"
      >
        <Grid item>
          {PeerDisplay()}
        </Grid>
      </Grid>
    </Box>
  );
}
