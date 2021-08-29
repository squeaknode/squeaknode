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
  deleteProfileRequest,
} from '../../squeakclient/requests';

export default function DeleteProfileDialog({
  open,
  handleClose,
  profile,
  reloadProfile,
  ...props
}) {
  const classes = useStyles();
  const history = useHistory();

  const deleteProfile = (profileId) => {
    deleteProfileRequest(profileId, (response) => {
      reloadProfile();
    });
  };

  function handleSubmit(event) {
    event.preventDefault();
    console.log('profile:', profile);
    const profileId = profile.getProfileId();
    console.log('profileId:', profileId);
    deleteProfile(profileId);
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

  function DeleteProfileButton() {
    return (
      <Button
        type="submit"
        variant="contained"
        color="primary"
        className={classes.button}
      >
        Delete Profile
      </Button>
    );
  }

  return (
    <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
      <DialogTitle id="form-dialog-title">Delete Profile</DialogTitle>
      <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
        <DialogContent>
          Are you sure you want to delete this profile?
        </DialogContent>
        <DialogActions>
          {MakeCancelButton()}
          {DeleteProfileButton()}
        </DialogActions>
      </form>
    </Dialog>
  );
}
