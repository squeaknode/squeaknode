import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  FormControl,
  FormLabel,
  FormGroup,
  FormControlLabel,
  Switch,
} from '@material-ui/core';

// styles
import useStyles from './styles';

import {
  setPeerAutoconnectRequest,
  setPeerShareForFreeRequest,
} from '../../squeakclient/requests';

export default function ConfigurePeerDialog({
  open,
  handleClose,
  savedPeer,
  reloadPeer,
  ...props
}) {
  const classes = useStyles();

  const setAutoconnect = (id, autoconnect) => {
    setPeerAutoconnectRequest(id, autoconnect, () => {
      reloadPeer();
    });
  };

  const setShareForFree = (id, shareForFree) => {
    setPeerShareForFreeRequest(id, shareForFree, () => {
      reloadPeer();
    });
  };

  const handleSettingsAutoconnectChange = (event) => {
    console.log(`Autoconnect changed for peer id: ${savedPeer.getPeerId()}`);
    console.log(`Autoconnect changed to: ${event.target.checked}`);
    setAutoconnect(savedPeer.getPeerId(), event.target.checked);
  };

  const handleSettingsShareForFreeChange = (event) => {
    console.log(`ShareForFree changed for peer id: ${savedPeer.getPeerId()}`);
    console.log(`ShareForFree changed to: ${event.target.checked}`);
    setShareForFree(savedPeer.getPeerId(), event.target.checked);
  };

  function MakeCancelButton() {
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

  function PeerSettingsForm() {
    return (
      <FormControl component="fieldset">
        <FormLabel component="legend">Peer settings</FormLabel>
        <FormGroup>
          <FormControlLabel
            control={<Switch checked={savedPeer.getAutoconnect()} onChange={handleSettingsAutoconnectChange} />}
            label="Autoconnect"
          />
        </FormGroup>
        <FormGroup>
          <FormControlLabel
            control={<Switch checked={savedPeer.getShareForFree()} onChange={handleSettingsShareForFreeChange} />}
            label="Share for free"
          />
        </FormGroup>
      </FormControl>
    );
  }

  return (
    <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
      <DialogTitle id="form-dialog-title">Configure Peer</DialogTitle>
      <form className={classes.root} noValidate autoComplete="off">
        <DialogContent>
          {savedPeer
      && PeerSettingsForm()}
        </DialogContent>
        <DialogActions>
          {MakeCancelButton()}
        </DialogActions>
      </form>
    </Dialog>
  );
}
