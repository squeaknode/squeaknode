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
  lndNewAddress,
} from "../../squeakclient/requests"



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

  const getNewAddress = () => {
    // console.log("called newAddress");
    //
    // var newAddressRequest = new NewAddressRequest()
    // console.log(newAddressRequest);
    //
    // client.lndNewAddress(newAddressRequest, {}, (err, response) => {
    //   if (err) {
    //     console.log(err.message);
    //     alert('Error getting new address: ' + err.message);
    //     return;
    //   }
    //   console.log(response);
    //   console.log(response.getAddress());
    //   // goToProfilePage(response.getProfileId());
    //
    //   setAddress(response.getAddress());
    // });
    lndNewAddress((response) => {
      setAddress(response.getAddress());
    });
  };

  function handleSubmit(event) {
    event.preventDefault();
    getNewAddress(address);
    // handleClose();
  }

  function ReceiveBitcoinAddess() {
    return (
      <TextField
        id="standard-textarea"
        label="Address"
        required
        autoFocus
        value={address}
        onChange={handleChangeAddress}
        fullWidth
        inputProps={{
           readOnly: true,
        }}
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

  function RenewAddressButton() {
    return (
      <Button
       type="submit"
       variant="contained"
       color="primary"
       className={classes.button}
       >
       Get New Address
       </Button>
    )
  }

  return (
    <Dialog open={open} onEnter={resetFields} onClose={handleClose} aria-labelledby="form-dialog-title">
  <DialogTitle id="form-dialog-title">Receive Bitcoin</DialogTitle>
  <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
  <DialogContent>
    {ReceiveBitcoinAddess()}
  </DialogContent>
  <DialogActions>
    {CancelButton()}
    {RenewAddressButton()}
  </DialogActions>
  </form>
    </Dialog>
  )
}
