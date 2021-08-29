import React from 'react';
import {
  Dialog,
  DialogTitle,
} from '@material-ui/core';
import { useHistory } from 'react-router-dom';

// styles
import useStyles from './styles';

export default function LndUnavailableDialog({
  open,
  handleClose,
  ...props
}) {
  const classes = useStyles();
  const history = useHistory();

  return (
    <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
      <DialogTitle id="form-dialog-title">Lnd Unavailable</DialogTitle>
      Unable to connect to lnd node.
      Make sure that lnd node is avaialable, and then reload page.
    </Dialog>
  );
}
