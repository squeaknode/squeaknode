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
  OpenChannelRequest,
} from "../../proto/lnd_pb"
import { client } from "../../squeakclient/squeakclient"


export default function OpenChannelDialog({
  open,
  pubkey,
  handleClose,
  ...props
}) {
  var classes = useStyles();
  const history = useHistory();

  var [amount, setAmount] = useState("");

  const resetFields = () => {
    setAmount("");
  };

  const handleChangeAmount = (event) => {
    setAmount(event.target.value);
  };

  const openChannel = (pubkey, amount) => {
    console.log("called openChannel");

    var openChannelRequest = new OpenChannelRequest()
    openChannelRequest.setNodePubkeyString(pubkey);
    openChannelRequest.setLocalFundingAmount(amount);
    console.log(openChannelRequest);

    client.lndOpenChannelSync(openChannelRequest, {}, (err, response) => {
      if (err) {
        console.log(err.message);
        alert('Error opening channel: ' + err.message);
        return;
      }
      console.log(response);
      console.log(response.getFundingTxidStr());
      console.log(response.getOutputIndex());
      // goToProfilePage(response.getProfileId());
    });
  };

  // const goToProfilePage = (profileId) => {
  //   history.push("/app/profile/" + profileId);
  // };

  function handleSubmit(event) {
    event.preventDefault();
    console.log( 'pubkey:', pubkey);
    console.log( 'amount:', amount);
    if (!amount) {
      alert('Amount cannot be empty.');
      return;
    }
    openChannel(pubkey, amount);
    handleClose();
  }

  function PubKeyInput() {
    return (
      <TextField
        id="pubkey-textarea"
        label="Node Pub Key"
        required
        autoFocus
        value={pubkey}
        fullWidth
        inputProps={{
           readOnly: true,
        }}
      />
    )
  }

  function LocalFundingAmountInput() {
    return (
      <TextField
        id="amount-textarea"
        label="Local Funding Amount"
        required
        autoFocus
        value={amount}
        onChange={handleChangeAmount}
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

  function OpenChannelButton() {
    return (
      <Button
       type="submit"
       variant="contained"
       color="primary"
       className={classes.button}
       >
       Open Channel
       </Button>
    )
  }

  return (
    <Dialog open={open} onEnter={resetFields} onClose={handleClose} aria-labelledby="form-dialog-title">
  <DialogTitle id="form-dialog-title">Open Channel</DialogTitle>
  <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
  <DialogContent>
    {PubKeyInput()}
  </DialogContent>
  <DialogContent>
    {LocalFundingAmountInput()}
  </DialogContent>
  <DialogActions>
    {CancelButton()}
    {OpenChannelButton()}
  </DialogActions>
  </form>
    </Dialog>
  )
}
