import React from 'react';
import {
  Typography,
  Grid,
  Dialog,
  DialogTitle,
  DialogContent,
  TextField,
  DialogActions,
  Button,
} from '@material-ui/core';

// styles
import useStyles from './styles';

import Widget from '../Widget';


export default function SqueakDetailsDialog({
  open,
  handleClose,
  hash,
  squeak,
  ...props
}) {
  const classes = useStyles();

  function load(event) {
    // Nothing
  }

  function cancel(event) {
    event.stopPropagation();
    handleClose();
  }

  function ignore(event) {
    event.stopPropagation();
  }

  // useEffect(()=>{
  //   getSqueakDetails(hash)
  // },[hash]);

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

  function SqueakDetailsContent() {
    return (
      <>
        <Widget disableWidgetMenu>
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <div>
                <div key="hash" className={classes.legendItemContainer}>

                  <Typography color="text" colorBrightness="secondary">
                    Hash
                  </Typography>
                  <Typography color="text">
                    {squeak.getSqueakHash()}
                  </Typography>
                </div>

                <div key="address" className={classes.legendItemContainer}>

                  <Typography color="text" colorBrightness="secondary">
                    Address
                  </Typography>
                  <Typography color="text">
                    {squeak.getAuthorAddress()}
                  </Typography>
                </div>

                <div key="rawdata" className={classes.legendItemContainer}>
                  <Typography color="text" colorBrightness="secondary">
                    Raw Data
                  </Typography>
                  <TextField
                    id="standard-textarea"
                    placeholder="Placeholder"
                    value={squeak.getSerializedSqueakHex()}
                    fullWidth="true"
                    variant="outlined"
                    multiline
                  />
                </div>

                <div key="rawdata" className={classes.legendItemContainer}>
                  <Typography color="text" colorBrightness="secondary">
                    Secret key
                  </Typography>
                  <TextField
                    id="standard-textarea"
                    placeholder="Placeholder"
                    value={squeak.getSecretKeyHex()}
                    fullWidth="true"
                    variant="outlined"
                    multiline
                  />
                </div>

              </div>
            </Grid>
          </Grid>
        </Widget>
      </>
    );
  }

  return (
    <Dialog open={open} onRendered={load} onClose={cancel} onClick={ignore} aria-labelledby="form-dialog-title">
      <DialogTitle id="form-dialog-title">View Squeak Details</DialogTitle>
      <form className={classes.root} noValidate autoComplete="off">
        <DialogContent>
          {(squeak)
      && SqueakDetailsContent()}
        </DialogContent>
        <DialogActions>
          {MakeCancelButton()}
        </DialogActions>
      </form>
    </Dialog>
  );
}
