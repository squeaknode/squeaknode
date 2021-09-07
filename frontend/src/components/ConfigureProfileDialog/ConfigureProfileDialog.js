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
  Input,
  TextField,
} from '@material-ui/core';

// styles
import useStyles from './styles';

import {
  setSqueakProfileFollowingRequest,
  setSqueakProfileUseCustomPriceRequest,
  setSqueakProfileCustomPriceRequest,
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

  const setUseCustomPrice = (id, useCustomPrice) => {
    setSqueakProfileUseCustomPriceRequest(id, useCustomPrice, () => {
      reloadProfile();
    });
  };

  const setCustomPriceMsat = (id, customPriceMsat) => {
    setSqueakProfileCustomPriceRequest(id, customPriceMsat, () => {
      reloadProfile();
    });
  };

  const handleSettingsFollowingChange = (event) => {
    console.log(`Following changed for profile id: ${squeakProfile.getProfileId()}`);
    console.log(`Following changed to: ${event.target.checked}`);
    setFollowing(squeakProfile.getProfileId(), event.target.checked);
  };

  const handleSettingsUseCustomPriceChange = (event) => {
    console.log(`UseCustomPrice changed for profile id: ${squeakProfile.getProfileId()}`);
    console.log(`UseCustomPrice changed to: ${event.target.checked}`);
    setUseCustomPrice(squeakProfile.getProfileId(), event.target.checked);
  };

  const handleSettingsCustomPriceMsatChange = (event) => {
    console.log(`Custom Price changed for profile id: ${squeakProfile.getProfileId()}`);
    const newPriceMsat = event.target.value;
    console.log(`Custom Price changed to: ${newPriceMsat}`);
    if (newPriceMsat < 0) {
      return;
    }
    setCustomPriceMsat(squeakProfile.getProfileId(), event.target.value);
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
          <FormControlLabel
            control={<Switch checked={squeakProfile.getUseCustomPrice()} onChange={handleSettingsUseCustomPriceChange} />}
            label="Use Custom Price"
          />
        </FormGroup>
        {squeakProfile.getUseCustomPrice() ?
          <TextField
            required id="standard-required"
            label="Price (msats)"
            type="number"
            defaultValue={squeakProfile.getCustomPriceMsat()}
            onChange={handleSettingsCustomPriceMsatChange} /> :
          <TextField
            disabled
            id="standard-disabled"
            label="Disabled"
            defaultValue={squeakProfile.getCustomPriceMsat()} />
        }
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
