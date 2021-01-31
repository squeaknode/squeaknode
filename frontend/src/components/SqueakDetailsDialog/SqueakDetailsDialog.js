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

import {
  getSqueakDetailsRequest,
} from "../../squeakclient/requests"


export default function SqueakDetailsDialog({
  open,
  handleClose,
  hash,
  squeak,
  ...props
}) {
  var classes = useStyles();
  const history = useHistory();

  const [squeakDetails, setSqueakDetails] = useState(null);

  const getSqueakDetails = (hash) => {
      getSqueakDetailsRequest(hash, setSqueakDetails);
  };

  useEffect(()=>{
    getSqueakDetails(hash)
  },[hash]);

  function MakeCancelButton() {
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
                      &nbsp;{squeak.getSqueakHash()}
                  </Typography>
                </div>

                <div key="address" className={classes.legendItemContainer}>

                  <Typography color="text" colorBrightness="secondary">
                    Address
                  </Typography>
                  <Typography color="text">
                      &nbsp;{squeak.getAuthorAddress()}
                  </Typography>
                </div>

                <div key="rawdata" className={classes.legendItemContainer}>
                  <Typography color="text" colorBrightness="secondary">
                    Raw Data
                  </Typography>
                  <TextField
                    id="standard-textarea"
                    placeholder="Placeholder"
                    value={squeakDetails.getSerializedSqueakHex()}
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
    )
  }

  return (
    <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
  <DialogTitle id="form-dialog-title">View Squeak Details</DialogTitle>
  <form className={classes.root} noValidate autoComplete="off">
  <DialogContent>
    {(squeak && squeakDetails) &&
      SqueakDetailsContent()
    }
  </DialogContent>
  <DialogActions>
    {MakeCancelButton()}
  </DialogActions>
  </form>
    </Dialog>
  )
}
