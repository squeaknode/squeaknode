import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  FormControl,
  FormLabel,
  FormGroup,
  FormControlLabel,
  Switch,
} from '@material-ui/core';

// styles
import useStyles from './styles';

import {
  setSqueakProfileFollowingRequest,
} from '../../squeakclient/requests';

export default function ConfigureProfileDialog({
  open,
  handleClose,
  squeakProfile,
  reloadProfile,
  ...props
}) {
  const classes = useStyles();

  const setFollowing = (id, following) => {
    setSqueakProfileFollowingRequest(id, following, () => {
      reloadProfile();
    });
  };

  const handleSettingsFollowingChange = (event) => {
    console.log(`Following changed for profile id: ${squeakProfile.getProfileId()}`);
    console.log(`Following changed to: ${event.target.checked}`);
    setFollowing(squeakProfile.getProfileId(), event.target.checked);
  };

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

  function ProfileSettingsForm() {
    return (
      <FormControl component="fieldset">
        <FormLabel component="legend">Profile settings</FormLabel>
        <FormGroup>
          <FormControlLabel
            control={<Switch checked={squeakProfile.getFollowing()} onChange={handleSettingsFollowingChange} />}
            label="Following"
          />
        </FormGroup>
      </FormControl>
    );
  }

  return (
    <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
      <DialogTitle id="form-dialog-title">Configure Profile</DialogTitle>
      <form className={classes.root} noValidate autoComplete="off">
        <DialogContent>
          {squeakProfile
      && ProfileSettingsForm()}
        </DialogContent>
        <DialogActions>
          {MakeCancelButton()}
        </DialogActions>
      </form>
    </Dialog>
  );
}
