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
  var [port, setPort] = useState('');

  const handleChangeSubscriptionName = (event) => {
    setsubscriptionName(event.target.value);
  };

  const handleChangeHost = (event) => {
    setHost(event.target.value);
  };

  const handleChangePort = (event) => {
    setPort(event.target.value);
  };

  const createSubscription = (subscriptionName, host, port) => {
    console.log("called createSubscription");

    var createSubscriptionRequest = new CreateSubscriptionRequest()
    createSubscriptionRequest.setSubscriptionName(subscriptionName);
    createSubscriptionRequest.setHost(host);
    createSubscriptionRequest.setPort(port);
    console.log(createSubscriptionRequest);

    client.createSubscription(createSubscriptionRequest, {}, (err, response) => {
      if (err) {
        console.log(err.message);
        alert('Error creating subscription: ' + err.message);
        return;
      }
      console.log(response);
      console.log(response.getSubscriptionId());
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
    console.log( 'port:', port);
    if (!host) {
      alert('Host cannot be empty.');
      return;
    }
    if (!port) {
      alert('Port cannot be empty.');
      return;
    }
    createSubscription(subscriptionName, host, port);
    handleClose();
  }

  function CreateSubscriptionNameInput() {
    return (
      <TextField
        id="standard-textarea"
        label="Subscription Name"
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

  function CreatePortInput() {
    return (
      <TextField required
          id="standard-textarea"
          label="Port"
          required
          value={port}
          onChange={handleChangePort}
          inputProps={{ maxLength: 8 }}
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
  <DialogTitle id="form-dialog-title">Create Subscription</DialogTitle>
  <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
  <DialogContent>
    <div>
      {CreateSubscriptionNameInput()}
    </div>
    <div>
      {CreateHostInput()}
    </div>
    <div>
      {CreatePortInput()}
    </div>
  </DialogContent>
  <DialogActions>
    {CancelButton()}
    {CreateSubscriptionButton()}
  </DialogActions>
  </form>
    </Dialog>
  )
}
