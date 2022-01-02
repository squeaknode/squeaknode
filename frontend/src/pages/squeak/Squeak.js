import React, {
  useState, useEffect, useMemo, useCallback,
} from 'react';
import { useParams } from 'react-router-dom';
import {
  Grid,
  Button,
  Box,
  CircularProgress,
} from '@material-ui/core';

import Timeline from '@material-ui/lab/Timeline';

import GetAppIcon from '@material-ui/icons/GetApp';
import ReplayIcon from '@material-ui/icons/Replay';

// styles
import useStyles from './styles';

// components
import SqueakDetailItem from '../../components/SqueakDetailItem';
import SqueakThread from '../../components/SqueakThread';
import SqueakReplies from '../../components/SqueakReplies';
import DownloadInProgressDialog from '../../components/DownloadInProgressDialog';

import {
  getAncestorSqueakDisplaysRequest,
  getReplySqueakDisplaysRequest,
  getNetworkRequest,
  downloadSqueakRequest,
  downloadRepliesRequest,
  // subscribeReplySqueakDisplaysRequest,
  // subscribeAncestorSqueakDisplaysRequest,
} from '../../squeakclient/requests';

const SQUEAKS_PER_PAGE = 10;

export default function SqueakPage() {
  const classes = useStyles();
  const { hash } = useParams();
  const [ancestorSqueaks, setAncestorSqueaks] = useState(null);
  const [replySqueaks, setReplySqueaks] = useState(null);
  const [network, setNetwork] = useState('');
  const [waitingForReplySqueaks, setWaitingForReplySqueaks] = useState(false);
  const [waitingForDownloadAncestors, setWaitingForDownloadAncestors] = useState(false);
  const [waitingForDownloadReplies, setWaitingForDownloadReplies] = useState(false);

  const initialLoadComplete = useMemo(() => (ancestorSqueaks), [ancestorSqueaks]);

  const getAncestorSqueaks = useCallback((hash) => {
    getAncestorSqueakDisplaysRequest(hash, handleLoadedAncestorSqueaks);
  },
  []);
  // const subscribeAncestorSqueaks = (hash) => subscribeAncestorSqueakDisplaysRequest(hash, setAncestorSqueaks);
  const getReplySqueaks = useCallback((hash, limit, lastEntry) => {
    setWaitingForReplySqueaks(true);
    getReplySqueakDisplaysRequest(hash, limit, lastEntry, handleLoadedReplySqueaks);
  },
  []);
  // const subscribeReplySqueaks = (hash) => subscribeReplySqueakDisplaysRequest(hash, (resp) => {
  //   setReplySqueaks((prevReplySqueaks) => prevReplySqueaks.concat(resp));
  // });
  const getNetwork = () => {
    getNetworkRequest(setNetwork);
  };

  const getCurrentSqueak = () => {
    getAncestorSqueaks(hash);
  };

  const handleLoadedAncestorSqueaks = (loadedAncestorSqueaks) => {
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

  const handleCloseAncestorsDownloadInProgressDialog = () => {
    setWaitingForDownloadAncestors(false);
  };

  const handleCloseRepliesDownloadInProgressDialog = () => {
    setWaitingForDownloadReplies(false);
  };

  const handleDownloadAncestors = () => {
    console.log('Handling download ancestors click...');
    setWaitingForDownloadAncestors(true);
    downloadSqueakRequest(hash, (response) => {
      setWaitingForDownloadAncestors(false);
      const downloadResult = response.getDownloadResult();
      const numPeers = downloadResult.getNumberPeers();
      const numDownloaded = downloadResult.getNumberDownloaded();
      if (numPeers === 0) {
        alert("Unable to download because zero connected peers.");
      } else {
        alert(`Downloaded ${numDownloaded} squeaks from ${numPeers} connected peers.`);
      }
      if (downloadResult.getNumberDownloaded() === 0) {
        return;
      }
      setAncestorSqueaks(null); // Temporary fix until component unmounts correcyly
      getAncestorSqueaks(hash);
    });
  };

  const handleDownloadReplies = () => {
    console.log('Handling download replies click...');
    setWaitingForDownloadReplies(true);
    downloadRepliesRequest(hash, (response) => {
      setWaitingForDownloadReplies(false);
      const downloadResult = response.getDownloadResult();
      const numPeers = downloadResult.getNumberPeers();
      const numDownloaded = downloadResult.getNumberDownloaded();
      if (numPeers === 0) {
        alert("Unable to download because zero connected peers.");
      } else {
        alert(`Downloaded ${numDownloaded} squeaks from ${numPeers} connected peers.`);
      }
      if (downloadResult.getNumberDownloaded() === 0) {
        return;
      }
      setReplySqueaks(null); // Temporary fix until component unmounts correcyly
      getReplySqueaks(hash, SQUEAKS_PER_PAGE, null);
    });
  };

  const onDownloadRepliesClick = (event) => {
    event.preventDefault();
    handleDownloadReplies();
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
    setAncestorSqueaks(null); // Temporary fix until component unmounts correcyly
    getAncestorSqueaks(hash);
  }, [getAncestorSqueaks, hash]);
  // useEffect(() => {
  //   const stream = subscribeAncestorSqueaks(hash);
  //   return () => stream.cancel();
  // }, [hash]);
  useEffect(() => {
    setReplySqueaks(null); // Temporary fix until component unmounts correctly
    getReplySqueaks(hash, SQUEAKS_PER_PAGE, null);
  }, [getReplySqueaks, hash]);
  // useEffect(() => {
  //   const stream = subscribeReplySqueaks(hash);
  //   return () => stream.cancel();
  // }, [hash]);
  useEffect(() => {
    getNetwork();
  }, []);

  const currentSqueak = useMemo(() => calculateCurrentSqueak(ancestorSqueaks), [ancestorSqueaks]);

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
        handleDownloadAncestorsClick={handleDownloadAncestors}
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
        {replySqueaks && RepliesContent()}
        {ViewMoreSqueaksButton()}
      </>
    );
  }

  function GridContent() {
    return (
      <Grid container spacing={0}>
        <Grid item xs={12} sm={9}>
          {SqueakContent()}
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

  function AncestorsDownloadInProgressDialogContent() {
    return (
      <>
        <DownloadInProgressDialog
          open={waitingForDownloadAncestors}
          handleClose={handleCloseAncestorsDownloadInProgressDialog}
        />
      </>
    );
  }

  function RepliesDownloadInProgressDialogContent() {
    return (
      <>
        <DownloadInProgressDialog
          open={waitingForDownloadReplies}
          handleClose={handleCloseRepliesDownloadInProgressDialog}
        />
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
            {waitingForReplySqueaks && WaitingIndicator() }
          </div>
        </Grid>
      </>
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
      {AncestorsDownloadInProgressDialogContent()}
      {RepliesDownloadInProgressDialogContent()}
    </>
  );
}
