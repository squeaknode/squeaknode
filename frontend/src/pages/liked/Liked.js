import React, { useState, useEffect, useCallback, useMemo } from 'react';
import {
  Grid,
  Button,
  CircularProgress,
  CardHeader,
  Card,
} from '@material-ui/core';

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
  const [squeaks, setSqueaks] = useState(null);
  const [network, setNetwork] = useState('');
  const [waitingForLikedSqueaks, setWaitingForLikedSqueaks] = useState(false);

  const initialLoadComplete = useMemo(() => (squeaks), [squeaks]);

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
      <Card
        className={classes.root}
      >
        <CardHeader
          subheader="No squeaks have been liked. Try clicking the like button on some squeaks in your timeline."
        />
      </Card>
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
          {(squeaks.length > 0)
            ? SqueaksContent()
            : NoSqueaksContent()}
        {ViewMoreSqueaksButton()}
        </Grid>
      </Grid>
    );
  }

  function ViewMoreSqueaksButton() {
    return (
      <>
        <Grid item xs={12}>
          <div className={classes.wrapper}>
            {(!waitingForLikedSqueaks)
              ? ReadyButton()
              : WaitingIndicator()}
          </div>
        </Grid>
      </>
    );
  }

  function ReadyButton() {
    return (
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
    );
  }

  function WaitingIndicator() {
    return (
      <CircularProgress size={48} className={classes.buttonProgress} />
    );
  }

  return (
    <>
      {(initialLoadComplete)
        ? GridContent()
        : WaitingIndicator()}
    </>
  );
}
