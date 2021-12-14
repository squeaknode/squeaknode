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
  deletePeerRequest,
} from '../../squeakclient/requests';


export default function DeletePeerDialog({
  open,
  handleClose,
  peer,
  reloadPeer,
  ...props
}) {
  const classes = useStyles();

  const deletePeer = (peerId) => {
    deletePeerRequest(peerId, (response) => {
      reloadPeer();
    });
  };

  function handleSubmit(event) {
    event.preventDefault();
    console.log('peer:', peer);
    const peerId = peer.getPeerId();
    console.log('peerId:', peerId);
    deletePeer(peerId);
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

  function DeletePeerButton() {
    return (
      <Button
        type="submit"
        variant="contained"
        color="primary"
        className={classes.button}
      >
        Delete peer
      </Button>
    );
  }

  return (
    <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
      <DialogTitle id="form-dialog-title">Delete peer</DialogTitle>
      <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
        <DialogContent>
          Are you sure you want to delete this peer?
        </DialogContent>
        <DialogActions>
          {MakeCancelButton()}
          {DeletePeerButton()}
        </DialogActions>
      </form>
    </Dialog>
  );
}
