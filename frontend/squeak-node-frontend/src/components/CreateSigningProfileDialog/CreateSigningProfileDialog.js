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
  createSigningProfile,
} from "../../squeakclient/requests"


export default function CreateSigningProfileDialog({
  open,
  handleClose,
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

  const create = (profileName) => {
    createSigningProfile(profileName, (response) => {
      goToProfilePage(response.getProfileId());
    })
  };

  const goToProfilePage = (profileId) => {
    history.push("/app/profile/" + profileId);
  };

  function handleSubmit(event) {
    event.preventDefault();
    console.log( 'profileName:', profileName);
    if (!profileName) {
      alert('Profile Name cannot be empty.');
      return;
    }
    create(profileName);
    handleClose();
  }

  function CreateSigningProfileNameInput() {
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

  function CreateSigningProfilButton() {
    return (
      <Button
       type="submit"
       variant="contained"
       color="primary"
       className={classes.button}
       >
       Create Signing Profile
       </Button>
    )
  }

  return (
    <Dialog open={open} onEnter={resetFields} onClose={handleClose} aria-labelledby="form-dialog-title">
  <DialogTitle id="form-dialog-title">Create Signing Profile</DialogTitle>
  <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
  <DialogContent>
    {CreateSigningProfileNameInput()}
  </DialogContent>
  <DialogActions>
    {CancelButton()}
    {CreateSigningProfilButton()}
  </DialogActions>
  </form>
    </Dialog>
  )
}
