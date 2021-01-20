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
  importSigningProfileRequest,
} from "../../squeakclient/requests"


export default function ImportSigningProfileDialog({
  open,
  handleClose,
  ...props
}) {
  var classes = useStyles();
  const history = useHistory();

  var [profileName, setProfileName] = useState('');
  var [privateKey, setPrivateKey] = useState('');

  const resetFields = () => {
    setProfileName('');
  };

  const handleChangeProfileName = (event) => {
    setProfileName(event.target.value);
  };

  const handleChangePrivateKey = (event) => {
    setPrivateKey(event.target.value);
  };

  const handleResponse = (response) => {
    goToProfilePage(response.getProfileId());
  };

  const handleErr = (err) => {
    alert('Error creating contact profile: ' + err.message);
  };

  const goToProfilePage = (profileId) => {
    history.push("/app/profile/" + profileId);
  };

  function handleSubmit(event) {
    event.preventDefault();
    console.log( 'profileName:', profileName);
    console.log( 'privateKey:', privateKey);
    if (!profileName) {
      alert('Profile Name cannot be empty.');
      return;
    }
    if (!privateKey) {
      alert('Private Key cannot be empty.');
      return;
    }
    importSigningProfileRequest(profileName, privateKey, handleResponse, handleErr);
    handleClose();
  }

  function ImportSigningProfileNameInput() {
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

  function ImportSigningProfilePrivateKeyInput() {
    return (
      <TextField
        id="standard-textarea"
        label="Private Key"
        required
        autoFocus
        value={privateKey}
        onChange={handleChangePrivateKey}
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

  function ImportSigningProfilButton() {
    return (
      <Button
       type="submit"
       variant="contained"
       color="primary"
       className={classes.button}
       >
       Import Signing Profile
       </Button>
    )
  }

  return (
    <Dialog open={open} onEnter={resetFields} onClose={handleClose} aria-labelledby="form-dialog-title">
  <DialogTitle id="form-dialog-title">Import Signing Profile</DialogTitle>
  <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
  <DialogContent>
    {ImportSigningProfileNameInput()}
  </DialogContent>
  <DialogContent>
    {ImportSigningProfilePrivateKeyInput()}
  </DialogContent>
  <DialogActions>
    {CancelButton()}
    {ImportSigningProfilButton()}
  </DialogActions>
  </form>
    </Dialog>
  )
}
