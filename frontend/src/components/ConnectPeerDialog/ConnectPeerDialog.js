import React, { useState } from 'react';
import {
  Button,
  Dialog,
  DialogActions,
  DialogTitle,
  DialogContent,
  FormControlLabel,
  Switch,
  TextField,
  CircularProgress,
} from '@material-ui/core';

import {
  connectSqueakPeerRequest,
} from '../../squeakclient/requests';

// styles
import useStyles from './styles';

const portDefaultValue = '0';

export default function ConnectPeerDialog({
  open,
  handleClose,
  handlePeerConnected,
  ...props
}) {
  const classes = useStyles();

  const [peerName, setPeerName] = useState('');
  const [host, setHost] = useState('');
  const [port, setPort] = useState('');
  const [customPortChecked, setCustomPortChecked] = useState(false);
  const [useTorChecked, setUseTorChecked] = useState(false);
  const [loading, setLoading] = useState(false);

  const resetFields = () => {
    setPeerName('');
    setHost('');
    setPort(portDefaultValue);
    setCustomPortChecked(false);
  };

  const handleChangeHost = (event) => {
    setHost(event.target.value);
  };

  const handleChangeCustomPortChecked = (event) => {
    setPort(
      event.target.checked ? '' : portDefaultValue,
    );
    setCustomPortChecked(event.target.checked);
  };

  const handleChangePort = (event) => {
    setPort(event.target.value);
  };

  const handleChangeUseTorChecked = (event) => {
    setUseTorChecked(event.target.checked);
  };

  const connectPeer = (peerName, host, port) => {
    setLoading(true);
    connectSqueakPeerRequest(host, port, useTorChecked, (response) => {
      // goToPeerPage(history, response.getPeerId());
      // handlePeerConnected();
      handlePeerConnectedResponse();
    },
    handlePeerConnectedErr);
  };

  const handlePeerConnectedResponse = (response) => {
    handlePeerConnected();
    setLoading(false);
    handleClose();
  };

  const handlePeerConnectedErr = (err) => {
    alert(`Connect Peer failure: ${err}`);
    setLoading(false);
    handleClose();
  };

  function handleSubmit(event) {
    event.preventDefault();
    console.log('host:', host);
    console.log('port:', port);
    if (!host) {
      alert('Host cannot be empty.');
      return;
    }
    if (!port) {
      alert('Port cannot be empty.');
      return;
    }
    connectPeer(peerName, host, port);
    // handleClose();
  }

  function ConnectHostInput() {
    return (
      <TextField
        required
        variant="outlined"
        label="Host"
        autoFocus
        value={host}
        onChange={handleChangeHost}
        inputProps={{ maxLength: 128 }}
        margin="normal"
      />
    );
  }

  function ConnectPortInput() {
    return (
      <TextField
        required={customPortChecked}
        variant="outlined"
        label="Port"
        value={customPortChecked ? port : ''}
        onChange={handleChangePort}
        inputProps={{ maxLength: 8 }}
        disabled={!customPortChecked}
        margin="normal"
      />
    );
  }

  function CustomPortSwitch() {
    return (
      <FormControlLabel
        className={classes.formControlLabel}
        control={(
          <Switch
            checked={customPortChecked}
            onChange={handleChangeCustomPortChecked}
            name="use-custom-port"
            size="small"
          />
        )}
        label="Use custom port"
      />
    );
  }

  function UseTorSwitch() {
    return (
      <FormControlLabel
        className={classes.formControlLabel}
        control={(
          <Switch
            checked={useTorChecked}
            onChange={handleChangeUseTorChecked}
            name="use-tor"
            size="small"
          />
        )}
        label="Use Tor"
      />
    );
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
    );
  }

  function ConnectPeerButton() {
    return (
      <div className={classes.wrapper}>
        <Button
          type="submit"
          variant="contained"
          color="primary"
          disabled={loading}
        >
          Connect Peer
        </Button>
        {loading && <CircularProgress size={24} className={classes.buttonProgress} />}
      </div>
    );
  }

  return (
    <Dialog
      open={open}
      onEnter={resetFields}
      onClose={handleClose}
      aria-labelledby="form-dialog-title"
      maxWidth="sm"
    >
      <DialogTitle id="form-dialog-title">
        Connect Peer
      </DialogTitle>
      <form
        className={classes.form}
        onSubmit={handleSubmit}
        noValidate
        autoComplete="off"
      >
        <DialogContent>
          {ConnectHostInput()}
          {ConnectPortInput()}
        </DialogContent>
        <DialogActions>
          {CustomPortSwitch()}
        </DialogActions>
        <DialogActions>
          {UseTorSwitch()}
        </DialogActions>
        <DialogActions>
          {CancelButton()}
          {ConnectPeerButton()}
        </DialogActions>
      </form>
    </Dialog>
  );
}
