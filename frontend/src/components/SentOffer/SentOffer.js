import React from 'react';
import {
  Grid,
  Box,
  Link,
} from '@material-ui/core';
import { useHistory } from 'react-router-dom';

// styles
import moment from 'moment';
import useStyles from './styles';

import {
  goToSqueakPage,
} from '../../navigation/navigation';

export default function SentOffer({
  receivedPayment,
  ...props
}) {
  const classes = useStyles();

  const history = useHistory();

  const paymentTimeMs = receivedPayment.setPaymentTimeMs();

  const onSqueakClick = (event) => {
    event.preventDefault();
    const hash = receivedPayment.getSqueakHash();
    console.log(`Handling squeak click for hash: ${hash}`);
    goToSqueakPage(history, hash);
  };

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
          {paymentTimeMs
            ? moment(receivedPayment.setPaymentTimeMs()).format('DD MMM YYYY hh:mm a') : 'Not paid'}
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
    </Box>
  );
}
