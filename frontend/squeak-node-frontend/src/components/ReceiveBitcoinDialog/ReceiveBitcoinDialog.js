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
  CreateSigningProfileRequest,
} from "../../proto/squeak_admin_pb"
import { client } from "../../squeakclient/squeakclient"


export default function ReceiveBitcoinDialog({
  open,
  handleClose,
  ...props
}) {
  var classes = useStyles();
  const history = useHistory();

  var [address, setAddress] = useState('');

  const resetFields = () => {
    setAddress('');
  };

  const handleChangeAddress = (event) => {
    setAddress(event.target.value);
  };

  const createSigningProfile = (address) => {
    console.log("called createSigningProfile");

    var createSigningProfileRequest = new CreateSigningProfileRequest()
    createSigningProfileRequest.setProfileName(address);
    console.log(createSigningProfileRequest);

    client.createSigningProfile(createSigningProfileRequest, {}, (err, response) => {
      if (err) {
        console.log(err.message);
        alert('Error creating signing profile: ' + err.message);
        return;
      }
      console.log(response);
      console.log(response.getProfileId());
      goToProfilePage(response.getProfileId());
    });
  };

  const goToProfilePage = (profileId) => {
    history.push("/app/profile/" + profileId);
  };

  function handleSubmit(event) {
    event.preventDefault();
    console.log( 'address:', address);
    if (!address) {
      alert('address cannot be empty.');
      return;
    }
    createSigningProfile(address);
    handleClose();
  }

  function CreateSigningProfileNameInput() {
    return (
      <TextField
        id="standard-textarea"
        label="Address"
        required
        autoFocus
        value={address}
        onChange={handleChangeAddress}
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
  <DialogTitle id="form-dialog-title">Receive Bitcoin</DialogTitle>
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
