import React, { useState, useEffect, useCallback } from 'react';
import {
  Grid,
  Button,
  CircularProgress,
} from '@material-ui/core';

import Paper from '@material-ui/core/Paper';

import ReplayIcon from '@material-ui/icons/Replay';

// styles
import useStyles from './styles';

// components
import SqueakList from '../../components/SqueakList';

import {
  getLikedSqueakDisplaysRequest,
  getNetworkRequest,
} from '../../squeakclient/requests';

const SQUEAKS_PER_PAGE = 10;

export default function LikedPage() {
  const classes = useStyles();
  const [squeaks, setSqueaks] = useState([]);
  const [network, setNetwork] = useState('');
  const [waitingForLikedSqueaks, setWaitingForLikedSqueaks] = useState(false);

  const getSqueaks = useCallback((limit, lastEntry) => {
    setWaitingForLikedSqueaks(true);
    getLikedSqueakDisplaysRequest(limit, lastEntry, handleLoadedTimeline);
  },
  []);
  const getNetwork = () => {
    getNetworkRequest(setNetwork);
  };

  const handleLoadedTimeline = (loadedSqueaks) => {
    setWaitingForLikedSqueaks(false);
    setSqueaks((prevSqueaks) => {
      if (!prevSqueaks) {
        return loadedSqueaks;
      }
      return prevSqueaks.concat(loadedSqueaks);
    });
  };

  useEffect(() => {
    getSqueaks(SQUEAKS_PER_PAGE, null);
  }, [getSqueaks]);
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

  function SqueaksContent() {
    return (
      <>
        <SqueakList
          squeaks={squeaks}
          network={network}
          setSqueaksFn={setSqueaks}
        />
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
          {ViewMoreSqueaksButton()}
        </Grid>
        <Grid item xs={12} sm={3}>
          <Paper className={classes.paper} />
        </Grid>
      </Grid>
    );
  }

  function ViewMoreSqueaksButton() {
    return (
      <>
        <Grid item xs={12}>
          <div className={classes.wrapper}>
            {!waitingForLikedSqueaks
            && (
            <Button
              variant="contained"
              color="primary"
              disabled={waitingForLikedSqueaks}
              onClick={() => {
                const latestSqueak = squeaks.slice(-1).pop();
                getSqueaks(SQUEAKS_PER_PAGE, latestSqueak);
              }}
            >
              <ReplayIcon />
              View more squeaks
            </Button>
            )}
            {waitingForLikedSqueaks && <CircularProgress size={48} className={classes.buttonProgress} />}
          </div>
        </Grid>
      </>
    );
  }

  return (
    <>
      {GridContent()}
    </>
  );
}
