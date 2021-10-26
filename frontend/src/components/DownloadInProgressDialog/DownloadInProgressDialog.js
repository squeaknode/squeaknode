import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  TextField,
  DialogActions,
  Button,
  CircularProgress,
} from '@material-ui/core';

// styles
import useStyles from './styles';

import {
  lndNewAddressRequest,
} from '../../squeakclient/requests';

export default function DownloadInProgressDialog({
  open,
  handleClose,
  ...props
}) {
  const classes = useStyles();

  return (
    <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
      <DialogTitle id="form-dialog-title">Download in progress</DialogTitle>
      <form className={classes.root} noValidate autoComplete="off">
        <DialogContent>
          Downloading...
        </DialogContent>
        <DialogContent>
          <CircularProgress size={48} className={classes.buttonProgress} />
        </DialogContent>
      </form>
    </Dialog>
  );
}
