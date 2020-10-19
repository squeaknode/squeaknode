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
  createContactProfile,
} from "../../squeakclient/requests"


export default function CreateContactProfileDialog({
  open,
  handleClose,
  initialAddress='',
  ...props
}) {
  var classes = useStyles();
  const history = useHistory();

  var [profileName, setProfileName] = useState('');
  var [address, setAddress] = useState(initialAddress);

  const resetFields = () => {
    setProfileName('');
    setAddress(initialAddress);
  };

  const handleChangeProfileName = (event) => {
    setProfileName(event.target.value);
  };

  const handleChangeAddress = (event) => {
    setAddress(event.target.value);
  };

  const create = (profileName, squeakAddress) => {
    createContactProfile(profileName, squeakAddress, (response) => {
      goToProfilePage(response.getProfileId());
    })
  };

  const goToProfilePage = (profileId) => {
    history.push("/app/profile/" + profileId);
  };

  function handleSubmit(event) {
    event.preventDefault();
    console.log( 'profileName:', profileName);
    console.log( 'address:', address);
    if (!profileName) {
      alert('Profile Name cannot be empty.');
      return;
    }
    if (!address) {
      alert('Address Name cannot be empty.');
      return;
    }
    create(profileName, address);
    handleClose();
  }

  function CreateContactProfileNameInput() {
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

  function CreateContactAddressInput() {
    return (
      <TextField required
          id="standard-textarea"
          label="Address"
          required
          value={address}
          onChange={handleChangeAddress}
          inputProps={{ maxLength: 35 }}
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

  function CreateContactProfilButton() {
    return (
      <Button
       type="submit"
       variant="contained"
       color="primary"
       className={classes.button}
       >
       Create Contact Profile
       </Button>
    )
  }

  return (
    <Dialog open={open} onEnter={resetFields} onClose={handleClose} aria-labelledby="form-dialog-title">
  <DialogTitle id="form-dialog-title">Create Contact Profile</DialogTitle>
  <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
  <DialogContent>
    {CreateContactProfileNameInput()}
    {CreateContactAddressInput()}
  </DialogContent>
  <DialogActions>
    {CancelButton()}
    {CreateContactProfilButton()}
  </DialogActions>
  </form>
    </Dialog>
  )
}
