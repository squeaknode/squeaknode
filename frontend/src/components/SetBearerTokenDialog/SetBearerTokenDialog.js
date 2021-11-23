import React, { useState } from 'react';
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
  setTwitterBearerTokenRequest,
} from '../../squeakclient/requests';


export default function SetBearerTokenDialog({
  open,
  handleClose,
  reloadBearerTokenFn,
  ...props
}) {
  const classes = useStyles();

  const [bearerToken, setBearerToken] = useState('');

  const resetFields = () => {
    setBearerToken('');
  };

  const handleChangeBearerToken = (event) => {
    setBearerToken(event.target.value);
  };

  const handleResponse = (response) => {
    // goToProfilePage(history, response.getProfileId());
    // TODO
    reloadBearerTokenFn();
  };

  const handleErr = (err) => {
    alert(`Error setting bearer token: ${err}`);
  };

  const setBearerTokenRequest = (bearerToken) => {
    setTwitterBearerTokenRequest(bearerToken, handleResponse, handleErr);
  };

  function handleSubmit(event) {
    event.preventDefault();
    console.log('bearerToken:', bearerToken);
    if (!bearerToken) {
      alert('Bearer Token cannot be empty.');
      return;
    }
    setBearerTokenRequest(bearerToken);
    handleClose();
  }

  function SetBearerTokenInput() {
    return (
      <TextField
        id="standard-textarea"
        label="Bearer Token"
        variant="outlined"
        margin="normal"
        required
        autoFocus
        value={bearerToken}
        onChange={handleChangeBearerToken}
        fullWidth
        inputProps={{ maxLength: 256 }}
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

  function SetBearerTokenButton() {
    return (
      <Button
        type="submit"
        variant="contained"
        color="primary"
        className={classes.button}
      >
        Set Bearer Token
      </Button>
    );
  }

  return (
    <Dialog open={open} onEnter={resetFields} onClose={handleClose} aria-labelledby="form-dialog-title">
      <DialogTitle id="form-dialog-title">Set Bearer Token</DialogTitle>
      <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
        <DialogContent>
          {SetBearerTokenInput()}
        </DialogContent>
        <DialogActions>
          {CancelButton()}
          {SetBearerTokenButton()}
        </DialogActions>
      </form>
    </Dialog>
  );
}
