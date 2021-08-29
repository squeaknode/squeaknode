import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import {
  Grid,
  Button,
  Fab,
} from '@material-ui/core';
import { useTheme } from '@material-ui/styles';

import EditIcon from '@material-ui/icons/Edit';
import ReplayIcon from '@material-ui/icons/Replay';

import Paper from '@material-ui/core/Paper';

// styles
import useStyles from './styles';

// components
import MakeSqueakDialog from '../../components/MakeSqueakDialog';
import SqueakList from '../../components/SqueakList';

import {
  getTimelineSqueakDisplaysRequest,
  getNetworkRequest,
} from '../../squeakclient/requests';

const SQUEAKS_PER_PAGE = 10;

export default function TimelinePage() {
  const classes = useStyles();
  const theme = useTheme();
  const [squeaks, setSqueaks] = useState([]);
  const [open, setOpen] = React.useState(false);
  const [network, setNetwork] = useState('');

  const history = useHistory();

  const getSqueaks = () => {
    getTimelineSqueakDisplaysRequest(SQUEAKS_PER_PAGE, null, null, null, setSqueaks);
  };
  const getNetwork = () => {
    getNetworkRequest(setNetwork);
  };

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  useEffect(() => {
    getSqueaks(setSqueaks);
  }, []);
  useEffect(() => {
    getNetwork();
  }, []);

  function NoSqueaksContent() {
    return (
      <div>
        Unable to load squeaks.
      </div>
    );
  }

  function MakeSqueakDialogContent() {
    return (
      <>
        <MakeSqueakDialog
          open={open}
          handleClose={handleClose}
        />
      </>
    );
  }

  function SqueaksContent() {
    return (
      <>
        <SqueakList
          squeaks={squeaks}
          network={network}
          setSqueaksFn={setSqueaks}
        />
        {(squeaks.length > 0) && ViewMoreSqueaksButton()}
      </>
    );
  }

  function ViewMoreSqueaksButton() {
    return (
      <>
        <Grid item xs={12}>
          <div className={classes.root}>
            <Button
              variant="contained"
              onClick={() => {
                const latestSqueak = squeaks.slice(-1).pop();
                const latestSqueakHeight = (latestSqueak ? latestSqueak.getBlockHeight() : null);
                const latestSqueakTime = (latestSqueak ? latestSqueak.getSqueakTime() : null);
                const latestSqueakHash = (latestSqueak ? latestSqueak.getSqueakHash() : null);
                console.log(latestSqueakHeight);
                console.log(latestSqueakTime);
                console.log(latestSqueakHash);
                getTimelineSqueakDisplaysRequest(SQUEAKS_PER_PAGE, latestSqueakHeight, latestSqueakTime, latestSqueakHash, (resp) => {
                // TODO: nothing maybe
                  console.log(resp);
                  setSqueaks(squeaks.concat(resp));
                });
              }}
            >
              <ReplayIcon />
              View more squeaks
            </Button>
          </div>
        </Grid>
      </>
    );
  }

  function GridContent() {
    return (
      <Grid container spacing={0}>
        <Grid item xs={12} sm={9}>
          <Paper className={classes.paper}>
            {(squeaks)
              ? SqueaksContent()
              : NoSqueaksContent()}
          </Paper>
        </Grid>
        <Grid item xs={12} sm={3}>
          <Paper className={classes.paper} />
        </Grid>
      </Grid>
    );
  }

  return (
    <>
      {GridContent()}
      <Fab color="secondary" aria-label="edit" className={classes.fab} onClick={handleClickOpen}>
        <EditIcon />
      </Fab>

      {MakeSqueakDialogContent()}
    </>
  );
}
