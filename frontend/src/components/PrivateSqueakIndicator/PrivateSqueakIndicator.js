import React from 'react';
import {
  Grid,
  Link,
} from '@material-ui/core';
import { useHistory } from 'react-router-dom';

import ForwardIcon from '@mui/icons-material/Forward';

import {
  goToPubkeyPage,
} from '../../navigation/navigation';

export default function PrivateSqueakIndicator({
  squeak,
  ...props
}) {
  const history = useHistory();

  const onRecipientAddressClick = (event) => {
    event.preventDefault();
    event.stopPropagation();
    console.log('Handling recipient click...');
    if (!squeak || !squeak.getIsPrivate()) {
      return;
    }
    goToPubkeyPage(history, squeak.getRecipientPubkey());
  };

  function getRecipientAddressDisplay() {
    if (!squeak) {
      return 'Recipient unknown';
    }
    return squeak.getIsRecipientKnown()
      ? squeak.getRecipient().getProfileName()
      : squeak.getRecipientPubkey();
  }

  return (
    <Grid
      container
      direction="row"
      justify="flex-start"
      alignItems="flex-start"
    >
      <Grid item>
        <ForwardIcon/>
        <Link
          href="#"
          onClick={onRecipientAddressClick}
        >
          {getRecipientAddressDisplay()}
        </Link>
      </Grid>
    </Grid>
  );
}
