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
  InputLabel,
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
  renameSqueakProfileRequest,
} from "../../squeakclient/requests"
import {
  reloadRoute,
} from "../../navigation/navigation"


export default function RenameProfileDialog({
  open,
  handleClose,
  profile,
  reloadProfile,
  ...props
}) {
  var classes = useStyles();
  const history = useHistory();

  var [profileName, setProfileName] = useState('');

  const resetFields = () => {
    setProfileName('');
  };

  const handleChangeProfileName = (event) => {
    setProfileName(event.target.value);
  };

  const handleResponse = (response) => {
    reloadProfile();
  };

  const handleErr = (err) => {
    alert('Error renaming signing profile: ' + err);
  };

  const renameSqueakProfile = (profileId, profileName) => {
    renameSqueakProfileRequest(profileId, profileName, handleResponse, handleErr);
  };

  function handleSubmit(event) {
    event.preventDefault();
    var profileId = profile.getProfileId();
    console.log( 'profileId:', profileId);
    console.log( 'profileName:', profileName);
    if (!profileName) {
      alert('Profile Name cannot be empty.');
      return;
    }
    renameSqueakProfile(profileId, profileName);
    handleClose();
  }

  function RenameProfileNameInput() {
    return (
      <TextField
        id="standard-textarea"
        label="Profile Name"
        required
        autoFocus
        value={profileName}
        onChange={handleChangeProfileName}
        fullWidth
        inputProps={{ maxLength: 64 }}
      />
    )
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
    )
  }

  function RenameProfilButton() {
    return (
      <Button
       type="submit"
       variant="contained"
       color="primary"
       className={classes.button}
       >
       Rename Profile
       </Button>
    )
  }

  return (
    <Dialog open={open} onEnter={resetFields} onClose={handleClose} aria-labelledby="form-dialog-title">
  <DialogTitle id="form-dialog-title">Rename Profile</DialogTitle>
  <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
  <DialogContent>
    {RenameProfileNameInput()}
  </DialogContent>
  <DialogActions>
    {CancelButton()}
    {RenameProfilButton()}
  </DialogActions>
  </form>
    </Dialog>
  )
}
