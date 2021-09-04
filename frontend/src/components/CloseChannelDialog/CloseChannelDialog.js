import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  TextField,
  DialogActions,
  Button,
} from '@material-ui/core';

// styles
import useStyles from './styles';

import {
  lndCloseChannelRequest,
} from '../../squeakclient/requests';

export default function CloseChannelDialog({
  open,
  txId,
  outputIndex,
  handleClose,
  ...props
}) {
  const classes = useStyles();

  const resetFields = () => {
    // TODO
  };

  const handleResponse = (response) => {
    // TODO: handle streaming response.
    // TODO: go to channel page instead of showing alert.
  };

  const handleErr = (err) => {
    alert(`Error closing channel: ${err}`);
  };

  const closeChannel = (txId, outputIndex) => {
    lndCloseChannelRequest(txId, outputIndex, handleResponse, handleErr);
  };

  function handleSubmit(event) {
    event.preventDefault();
    console.log('txId:', txId);
    console.log('outputIndex:', outputIndex);
    closeChannel(txId, outputIndex);
    handleClose();
  }

  function TxIdInput() {
    return (
      <TextField
        id="txid-textarea"
        label="TxId"
        required
        autoFocus
        value={txId}
        fullWidth
        inputProps={{
          readOnly: true,
        }}
      />
    );
  }

  function OutputIndexInput() {
    return (
      <TextField
        id="outputindex-textarea"
        label="Output Index"
        required
        autoFocus
        value={outputIndex}
        fullWidth
        inputProps={{
          readOnly: true,
        }}
      />
    );
  }

  function CancelButton() {
    return (
      <Button
        onClick={handleClose}
        variant="contained"
        color="secondary"
      >
        Cancel
      </Button>
    );
  }

  function CloseChannelButton() {
    return (
      <Button
        type="submit"
        variant="contained"
        color="primary"
        className={classes.button}
      >
        Close Channel
      </Button>
    );
  }

  return (
    <Dialog open={open} onEnter={resetFields} onClose={handleClose} aria-labelledby="form-dialog-title">
      <DialogTitle id="form-dialog-title">Close Channel</DialogTitle>
      <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
        <DialogContent>
          {TxIdInput()}
        </DialogContent>
        <DialogContent>
          {OutputIndexInput()}
        </DialogContent>
        <DialogActions>
          {CancelButton()}
          {CloseChannelButton()}
        </DialogActions>
      </form>
    </Dialog>
  );
}
