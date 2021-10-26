import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  CircularProgress,
} from '@material-ui/core';

// styles
import useStyles from './styles';

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
