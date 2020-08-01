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
  CreateContactProfileRequest,
  CreateSubscriptionRequest,
} from "../../proto/squeak_admin_pb"
import {SqueakAdminClient} from "../../proto/squeak_admin_grpc_web_pb"

var client = new SqueakAdminClient('http://' + window.location.hostname + ':8080')

export default function CreateSubscriptionDialog({
  open,
  handleClose,
  ...props
}) {
  var classes = useStyles();
  const history = useHistory();

  var [subscriptionName, setsubscriptionName] = useState('');
  var [host, setHost] = useState('');

  const handleChangeSubscriptionName = (event) => {
    setsubscriptionName(event.target.value);
  };

  const handleChangeHost = (event) => {
    setHost(event.target.value);
  };

  const createSubscription = (serverName, host, port) => {
    console.log("called createContactProfile");

    var addServerRequest = new CreateSubscriptionRequest()
    addServerRequest.setServerName(serverName);
    addServerRequest.setHost(host);
    // TODO: use real port here
    // addServerRequest.setHost(0);
    console.log(addServerRequest);

    client.addServer(addServerRequest, {}, (err, response) => {
      if (err) {
        console.log(err.message);
        alert('Error creating subscription: ' + err.message);
        return;
      }
      console.log(response);
      console.log(response.getServerId());
      // goToProfilePage(response.getProfileId());
    });
  };

  const goToProfilePage = (profileId) => {
    history.push("/app/profile/" + profileId);
  };

  function handleSubmit(event) {
    event.preventDefault();
    console.log( 'subscriptionName:', subscriptionName);
    console.log( 'host:', host);
    if (!host) {
      alert('Host cannot be empty.');
      return;
    }
    createSubscription(subscriptionName, host);
    handleClose();
  }

  function CreateSubscriptionNameInput() {
    return (
      <TextField
        id="standard-textarea"
        label="Subscription Name"
        required
        autoFocus
        value={subscriptionName}
        onChange={handleChangeSubscriptionName}
        fullWidth
        inputProps={{ maxLength: 64 }}
      />
    )
  }

  function CreateHostInput() {
    return (
      <TextField required
          id="standard-textarea"
          label="Host"
          required
          value={host}
          onChange={handleChangeHost}
          inputProps={{ maxLength: 128 }}
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

  function CreateSubscriptionButton() {
    return (
      <Button
       type="submit"
       variant="contained"
       color="primary"
       className={classes.button}
       >
       Create Subscription
       </Button>
    )
  }

  return (
    <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
  <DialogTitle id="form-dialog-title">Create Contact Profile</DialogTitle>
  <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
  <DialogContent>
    {CreateSubscriptionNameInput()}
    {CreateHostInput()}
  </DialogContent>
  <DialogActions>
    {CancelButton()}
    {CreateSubscriptionButton()}
  </DialogActions>
  </form>
    </Dialog>
  )
}
