import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
} from '@material-ui/core';

// styles
import useStyles from './styles';

import {
  deleteTwitterAccountRequest,
} from '../../squeakclient/requests';

export default function DeleteTwitterAccountDialog({
  open,
  handleClose,
  twitterAccount,
  reloadAccountsFn,
  ...props
}) {
  const classes = useStyles();

  const deleteTwitterAccount = (twitterAccountId) => {
    deleteTwitterAccountRequest(twitterAccountId, (response) => {
      reloadAccountsFn();
    });
  };

  function handleSubmit(event) {
    event.preventDefault();
    console.log('twitter account:', twitterAccount);
    const twitterAccountId = twitterAccount.getTwitterAccountId();
    console.log('twitterAccountId:', twitterAccountId);
    deleteTwitterAccount(twitterAccountId);
    handleClose();
  }

  function MakeCancelButton() {
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

  function DeleteTwitterAccountButton() {
    return (
      <Button
        type="submit"
        variant="contained"
        color="primary"
        className={classes.button}
      >
        Delete Twitter Account
      </Button>
    );
  }

  return (
    <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
      <DialogTitle id="form-dialog-title">Delete Twitter Account Mapping</DialogTitle>
      <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
        <DialogContent>
          Are you sure you want to delete this twitter account mapping?
        </DialogContent>
        <DialogActions>
          {MakeCancelButton()}
          {DeleteTwitterAccountButton()}
        </DialogActions>
      </form>
    </Dialog>
  );
}
