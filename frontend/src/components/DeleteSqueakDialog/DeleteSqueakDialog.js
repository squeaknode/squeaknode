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
  deleteSqueakRequest,
} from '../../squeakclient/requests';
import {
  reloadRoute,
} from '../../navigation/navigation';

export default function DeleteSqueakDialog({
  open,
  handleClose,
  squeakToDelete,
  ...props
}) {
  const classes = useStyles();
  const history = useHistory();

  const deleteSqueak = (squeakHash) => {
    deleteSqueakRequest(squeakHash, (response) => {
      reloadRoute(history);
    });
  };

  function handleSubmit(event) {
    event.preventDefault();
    event.stopPropagation();
    console.log('squeakToDelete:', squeakToDelete);
    const squeakHash = squeakToDelete.getSqueakHash();
    console.log('squeakHash:', squeakHash);
    deleteSqueak(squeakHash);
    handleClose();
  }

  function cancel(event) {
    event.stopPropagation();
    handleClose();
  }

  function ignore(event) {
    event.stopPropagation();
  }

  function MakeCancelButton() {
    return (
      <Button
        onClick={cancel}
        variant="contained"
        color="secondary"
      >
        Cancel
      </Button>
    );
  }

  function DeleteSqueakButton() {
    return (
      <Button
        type="submit"
        variant="contained"
        color="primary"
        className={classes.button}
      >
        Delete Squeak
      </Button>
    );
  }

  return (
    <Dialog open={open} onClose={cancel} onBackdropClick={cancel} onClick={ignore} aria-labelledby="form-dialog-title">
      <DialogTitle id="form-dialog-title">Delete Squeak</DialogTitle>
      <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
        <DialogContent>
          Are you sure you want to delete this squeak?
        </DialogContent>
        <DialogActions>
          {MakeCancelButton()}
          {DeleteSqueakButton()}
        </DialogActions>
      </form>
    </Dialog>
  );
}
