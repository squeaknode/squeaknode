import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
} from '@material-ui/core';
import { useHistory } from 'react-router-dom';

// styles
import useStyles from './styles';

import {
  deletePeerRequest,
} from '../../squeakclient/requests';
import {
  reloadRoute,
} from '../../navigation/navigation';

export default function DeletePeerDialog({
  open,
  handleClose,
  peer,
  ...props
}) {
  const classes = useStyles();
  const history = useHistory();

  const deletePeer = (peerId) => {
    deletePeerRequest(peerId, (response) => {
      reloadRoute(history);
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
