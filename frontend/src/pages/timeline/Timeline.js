import React, { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import {
  Grid,
  Button,
  Fab,
  CircularProgress,
  Backdrop,
  CardHeader,
  Card,
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
  const [waitingForTimeline, setWaitingForTimeline] = React.useState(false);

  const history = useHistory();

  const getSqueaks = (limit, blockHeight, squeakTime, squeakHash) => {
    setWaitingForTimeline(true);
    getTimelineSqueakDisplaysRequest(limit, blockHeight, squeakTime, squeakHash, handleLoadedTimeline, alertFailedRequest);
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

  const alertFailedRequest = () => {
    alert('Failed to load timeline.');
  };

  const handleLoadedTimeline = (loadedSqueaks) => {
    setWaitingForTimeline(false);
    setSqueaks(squeaks.concat(loadedSqueaks));
  };

  useEffect(() => {
    getSqueaks(SQUEAKS_PER_PAGE, null, null, null);
  }, []);
  useEffect(() => {
    getNetwork();
  }, []);

  function NoSqueaksContent() {
    return (
      <Card
        className={classes.root}
      >
        <CardHeader
          subheader="No squeaks found in timeline. Try following your friends or add your own squeaks."
        />
      </Card>
    );
  }

  function LoadingContent() {
    return (
      <Backdrop className={classes.backdrop} open={waitingForTimeline}>
        <CircularProgress color="inherit" />
      </Backdrop>
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
                getSqueaks(SQUEAKS_PER_PAGE, latestSqueakHeight, latestSqueakTime, latestSqueakHash);
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
            {(squeaks.length > 0)
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
      {LoadingContent()}
    </>
  );
}
