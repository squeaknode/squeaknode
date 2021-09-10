import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  TextField,
} from '@material-ui/core';

// styles
import useStyles from './styles';

import {
  getExternalAddressRequest,
} from '../../squeakclient/requests';

export default function ShowExternalAddressDialog({
  open,
  handleClose,
  ...props
}) {
  const classes = useStyles();

  const [externalAddress, setExternalAddress] = useState(null);

  const resetFields = () => {
    setExternalAddress(null);
  };

  const getExternalAddress = () => {
    getExternalAddressRequest(setExternalAddress);
  };

  function load(event) {
    getExternalAddress();
  }

  function cancel(event) {
    event.stopPropagation();
    handleClose();
  }

  function ignore(event) {
    event.stopPropagation();
  }

  function DisplayExternalAddress() {
    return (
      <TextField
        id="standard-textarea"
        label="external-address"
        required
        autoFocus
        value={externalAddress && `${externalAddress.getHost()}:${externalAddress.getPort()}`}
        fullWidth
        inputProps={{
          readOnly: true,
        }}
      />
    );
  }

  return (
    <Dialog open={open} onRendered={load} onClose={cancel} onClick={ignore} aria-labelledby="form-dialog-title">
      <DialogTitle id="form-dialog-title">Show External Address</DialogTitle>
      <form className={classes.root} noValidate autoComplete="off">
        <DialogContent>
          {DisplayExternalAddress()}
        </DialogContent>
      </form>
    </Dialog>
  );
}
