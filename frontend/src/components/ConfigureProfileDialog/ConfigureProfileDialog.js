import React, {useState, useEffect} from 'react';
import {
  Paper,
  IconButton,
  Menu,
  MenuItem,
  Typography,
  Grid,
  Box,
  Link,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  TextField,
  DialogActions,
  Button,
  FormControl,
  FormLabel,
  FormGroup,
  InputLabel,
  FormControlLabel,
  FormHelperText,
  Switch,
  Select,
} from "@material-ui/core";
import { MoreVert as MoreIcon } from "@material-ui/icons";
import {useHistory} from "react-router-dom";
import classnames from "classnames";

// styles
import useStyles from "./styles";

import Widget from "../../components/Widget";
import SqueakThreadItem from "../../components/SqueakThreadItem";

import {
  setSqueakProfileFollowingRequest,
} from "../../squeakclient/requests"


export default function ConfigureProfileDialog({
  open,
  handleClose,
  squeakProfile,
  reloadProfile,
  ...props
}) {
  var classes = useStyles();
  const history = useHistory();

  const setFollowing = (id, following) => {
    setSqueakProfileFollowingRequest(id, following, () => {
      reloadProfile();
    })
  };

  const handleSettingsFollowingChange = (event) => {
    console.log("Following changed for profile id: " + squeakProfile.getProfileId());
    console.log("Following changed to: " + event.target.checked);
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
    )
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
    )
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
  )
}
