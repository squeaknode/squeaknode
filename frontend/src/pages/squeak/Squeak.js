import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { useParams, useHistory } from 'react-router-dom';
import {
  Grid,
  Button,
  Box,
  CircularProgress,
} from '@material-ui/core';

import Timeline from '@material-ui/lab/Timeline';
import TimelineDot from '@material-ui/lab/TimelineDot';
import Paper from '@material-ui/core/Paper';

import FaceIcon from '@material-ui/icons/Face';
import GetAppIcon from '@material-ui/icons/GetApp';
import ReplayIcon from '@material-ui/icons/Replay';

// styles
import useStyles from './styles';

// components
import SqueakDetailItem from '../../components/SqueakDetailItem';
import SqueakThread from '../../components/SqueakThread';
import SqueakReplies from '../../components/SqueakReplies';

import {
  getAncestorSqueakDisplaysRequest,
  getReplySqueakDisplaysRequest,
  getNetworkRequest,
  downloadRepliesRequest,
  subscribeReplySqueakDisplaysRequest,
  subscribeAncestorSqueakDisplaysRequest,
} from '../../squeakclient/requests';
import {
  goToSqueakAddressPage,
} from '../../navigation/navigation';

const SQUEAKS_PER_PAGE = 10;

export default function SqueakPage() {
  const classes = useStyles();
  const history = useHistory();
  const { hash } = useParams();
  const [ancestorSqueaks, setAncestorSqueaks] = useState(null);
  const [replySqueaks, setReplySqueaks] = useState([]);
  const [network, setNetwork] = useState('');
  const [waitingForSqueak, setWaitingForSqueak] = useState(false);
  const [waitingForReplySqueaks, setWaitingForReplySqueaks] = useState(false);

  const getAncestorSqueaks = useCallback((hash) => {
    setWaitingForSqueak(true);
    getAncestorSqueakDisplaysRequest(hash, handleLoadedAncestorSqueaks);
  },
  []);
  const subscribeAncestorSqueaks = (hash) => subscribeAncestorSqueakDisplaysRequest(hash, setAncestorSqueaks);
  const getReplySqueaks = useCallback((hash, limit, lastEntry) => {
    setWaitingForReplySqueaks(true);
    getReplySqueakDisplaysRequest(hash, limit, lastEntry, handleLoadedReplySqueaks);
  },
  []);
  const subscribeReplySqueaks = (hash) => subscribeReplySqueakDisplaysRequest(hash, (resp) => {
    setReplySqueaks((prevReplySqueaks) => prevReplySqueaks.concat(resp));
  });
  const getNetwork = () => {
    getNetworkRequest(setNetwork);
  };

  const getCurrentSqueak = () => {
    getAncestorSqueaks(hash);
  };

  const handleLoadedAncestorSqueaks = (loadedAncestorSqueaks) => {
    setWaitingForSqueak(false);
    setAncestorSqueaks(loadedAncestorSqueaks);
  };

  const handleLoadedReplySqueaks = (loadedReplySqueaks) => {
    setWaitingForReplySqueaks(false);
    setReplySqueaks((prevSqueaks) => {
      if (!prevSqueaks) {
        return loadedReplySqueaks;
      }
      return prevSqueaks.concat(loadedReplySqueaks);
    });
  };

  const onDownloadRepliesClick = (event) => {
    event.preventDefault();
    console.log('Handling download replies click...');
    downloadRepliesRequest(hash, (response) => {
      // Do nothing.
    });
  };

  const calculateCurrentSqueak = (ancestorSqueaks) => {
    if (ancestorSqueaks == null) {
      return null;
    } if (ancestorSqueaks.length === 0) {
      return null;
    }
    return ancestorSqueaks.slice(-1)[0];
  };

  useEffect(() => {
    getAncestorSqueaks(hash);
  }, [getAncestorSqueaks, hash]);
  useEffect(() => {
    const stream = subscribeAncestorSqueaks(hash);
    return () => stream.cancel();
  }, [hash]);
  useEffect(() => {
    getReplySqueaks(hash, SQUEAKS_PER_PAGE, null);
  }, [getReplySqueaks, hash]);
  useEffect(() => {
    const stream = subscribeReplySqueaks(hash);
    return () => stream.cancel();
  }, [hash]);
  useEffect(() => {
    getNetwork();
  }, []);

  const currentSqueak = useMemo(() => calculateCurrentSqueak(ancestorSqueaks), [ancestorSqueaks]);

  function NoSqueakContent() {
    return (
      <div>
        Unable to load squeak.
      </div>
    );
  }

  function TimelineUserAvatar(squeak) {
    const handleAvatarClick = () => {
      console.log('Avatar clicked...');
      if (squeak) {
        goToSqueakAddressPage(history, squeak.getAuthorAddress());
      }
    };
    return (
      <TimelineDot
        onClick={handleAvatarClick}
        style={{ cursor: 'pointer' }}
      >
        <FaceIcon />
      </TimelineDot>
    );
  }

  function AncestorsContent() {
    return (
      <SqueakThread
        squeaks={ancestorSqueaks}
        network={network}
        setSqueaksFn={setAncestorSqueaks}
      />
    );
  }

  function CurrentSqueakContent() {
    return (
      <SqueakDetailItem
        hash={hash}
        squeak={currentSqueak}
        reloadSqueak={getCurrentSqueak}
        network={network}
      />
    );
  }

  function RepliesContent() {
    return (
      <SqueakReplies
        squeaks={replySqueaks}
        network={network}
        setSqueaksFn={setReplySqueaks}
      />
    );
  }

  function SqueakContent() {
    return (
      <>
        <Timeline align="left">
          {AncestorsContent()}
        </Timeline>
        {CurrentSqueakContent()}
        {DownloadRepliesButtonContent()}
        {RepliesContent()}
        {ViewMoreSqueaksButton()}
      </>
    );
  }

  function GridContent() {
    return (
      <Grid container spacing={0}>
        <Grid item xs={12} sm={9}>
          <Paper className={classes.paper}>
            {ancestorSqueaks && SqueakContent()}
          </Paper>
          {waitingForSqueak && <CircularProgress size={48} className={classes.buttonProgress} />}
        </Grid>
        <Grid item xs={12} sm={3}>
          <Paper className={classes.paper} />
        </Grid>
      </Grid>
    );
  }

  function DownloadRepliesButtonContent() {
    return (
      <>
        <Box p={1}>
          <Button
            variant="contained"
            onClick={onDownloadRepliesClick}
          >
            <GetAppIcon />
            Download replies
          </Button>
        </Box>
      </>
    );
  }

  function ViewMoreSqueaksButton() {
    return (
      <>
        <Grid item xs={12}>
          <div className={classes.wrapper}>
            {!waitingForReplySqueaks
            && (
            <Button
              variant="contained"
              color="primary"
              disabled={waitingForReplySqueaks}
              onClick={() => {
                const latestSqueak = replySqueaks.slice(-1).pop();
                getReplySqueaks(hash, SQUEAKS_PER_PAGE, latestSqueak);
              }}
            >
              <ReplayIcon />
              View more replies
            </Button>
            )}
            {waitingForReplySqueaks && <CircularProgress size={48} className={classes.buttonProgress} />}
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
