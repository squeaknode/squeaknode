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
  clearSqueakProfileImageRequest,
} from '../../squeakclient/requests';

export default function ClearProfileImageDialog({
  open,
  handleClose,
  squeakProfile,
  reloadProfile,
  ...props
}) {
  const classes = useStyles();
  const history = useHistory();

  const handleResponse = (response) => {
    reloadProfile();
  };

  const handleErr = (err) => {
    alert(`Error clearing profile image: ${err}`);
  };

  const clearProfileImage = () => {
    clearSqueakProfileImageRequest(
      squeakProfile.getProfileId(),
      handleResponse,
      handleErr,
    );
  };

  function handleSubmit(event) {
    event.preventDefault();
    clearProfileImage();
    handleClose();
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

  function ClearProfileImageButton() {
    return (
      <Button
        type="submit"
        variant="contained"
        color="primary"
        className={classes.button}
      >
        Clear Profile Image
      </Button>
    );
  }

  return (
    <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
      <DialogTitle id="form-dialog-title">Clear Profile Image</DialogTitle>
      <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
        <DialogContent>
          Are you sure you want to clear the image for this profile?
        </DialogContent>
        <DialogActions>
          {CancelButton()}
          {ClearProfileImageButton()}
        </DialogActions>
      </form>
    </Dialog>
  );
}
