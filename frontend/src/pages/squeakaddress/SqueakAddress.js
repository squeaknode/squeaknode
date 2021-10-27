import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useHistory } from 'react-router-dom';
import {
  Grid,
  Button,
  Box,
  CircularProgress,
} from '@material-ui/core';

// styles

// components

import Paper from '@material-ui/core/Paper';

import GetAppIcon from '@material-ui/icons/GetApp';
import ReplayIcon from '@material-ui/icons/Replay';

import CreateContactProfileDialog from '../../components/CreateContactProfileDialog';
import DownloadInProgressDialog from '../../components/DownloadInProgressDialog';
import SqueakList from '../../components/SqueakList';
import useStyles from './styles';

import {
  getSqueakProfileByAddressRequest,
  getAddressSqueakDisplaysRequest,
  getNetworkRequest,
  // subscribeAddressSqueakDisplaysRequest,
  downloadAddressSqueaksRequest,
} from '../../squeakclient/requests';
import {
  goToProfilePage,
} from '../../navigation/navigation';

const SQUEAKS_PER_PAGE = 10;

export default function SqueakAddressPage() {
  const classes = useStyles();
  const history = useHistory();
  const { address } = useParams();
  const [squeakProfile, setSqueakProfile] = useState(null);
  const [squeaks, setSqueaks] = useState([]);
  const [createContactProfileDialogOpen, setCreateContactProfileDialogOpen] = useState(false);
  const [network, setNetwork] = useState('');
  const [waitingForSqueaks, setWaitingForSqueaks] = useState(false);
  const [waitingForDownload, setWaitingForDownload] = useState(false);

  const getSqueakProfile = (address) => {
    getSqueakProfileByAddressRequest(address, setSqueakProfile);
  };
  const getSqueaks = useCallback((address, limit, lastEntry) => {
    setWaitingForSqueaks(true);
    getAddressSqueakDisplaysRequest(address, limit, lastEntry, handleLoadedAddressSqueaks);
  },
  []);
  // const subscribeSqueaks = (address) => subscribeAddressSqueakDisplaysRequest(address, (resp) => {
  //   setSqueaks((prevSqueaks) => [resp].concat(prevSqueaks));
  // });
  const getNetwork = () => {
    getNetworkRequest(setNetwork);
  };

  const handleLoadedAddressSqueaks = (loadedAddressSqueaks) => {
    setWaitingForSqueaks(false);
    setSqueaks((prevSqueaks) => {
      if (!prevSqueaks) {
        return loadedAddressSqueaks;
      }
      return prevSqueaks.concat(loadedAddressSqueaks);
    });
  };

  const handleClickOpenCreateContactProfileDialog = () => {
    setCreateContactProfileDialogOpen(true);
  };

  const handleCloseCreateContactProfileDialog = () => {
    setCreateContactProfileDialogOpen(false);
  };

  const handleCloseDownloadInProgressDialog = () => {
    setWaitingForDownload(false);
  };

  const onDownloadSqueaksClick = (event) => {
    event.preventDefault();
    console.log('Handling download address squeaks click...');
    setWaitingForDownload(true);
    downloadAddressSqueaksRequest(address, (response) => {
      setWaitingForDownload(false);
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
      setSqueaks([]);
      getSqueaks(address, SQUEAKS_PER_PAGE, null);
    });
  };

  useEffect(() => {
    getSqueakProfile(address);
  }, [address]);
  useEffect(() => {
    getSqueaks(address, SQUEAKS_PER_PAGE, null);
  }, [getSqueaks, address]);
  // useEffect(() => {
  //   const stream = subscribeSqueaks(address);
  //   return () => stream.cancel();
  // }, [address]);
  useEffect(() => {
    getNetwork();
  }, []);

  function NoProfileContent() {
    return (
      <div>
        No profile for address.
        <Button
          variant="contained"
          onClick={() => {
            handleClickOpenCreateContactProfileDialog();
          }}
        >
          Create Profile
        </Button>
      </div>
    );
  }

  function ProfileContent() {
    return (
      <div className={classes.root}>
        Profile:
        <Button
          variant="contained"
          onClick={() => {
            goToProfilePage(history, squeakProfile.getProfileId());
          }}
        >
          {squeakProfile.getProfileName()}
        </Button>
      </div>
    );
  }

  function NoSqueaksContent() {
    return (
      <div>
        Unable to load squeaks.
      </div>
    );
  }

  function SqueaksContent() {
    return (
      <SqueakList
        squeaks={squeaks}
        network={network}
        setSqueaksFn={setSqueaks}
      />
    );
  }

  function CreateContactProfileDialogContent() {
    return (
      <>
        <CreateContactProfileDialog
          open={createContactProfileDialogOpen}
          handleClose={handleCloseCreateContactProfileDialog}
          initialAddress={address}
        />
      </>
    );
  }

  function DownloadInProgressDialogContent() {
    return (
      <>
        <DownloadInProgressDialog
          open={waitingForDownload}
          handleClose={handleCloseDownloadInProgressDialog}
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

  function DownloadSqueaksButtonContent() {
    return (
      <>
        <Box p={1}>
          <Button
            variant="contained"
            onClick={onDownloadSqueaksClick}
          >
            <GetAppIcon />
            Download squeaks
          </Button>
        </Box>
      </>
    );
  }

  function SqueakProfileContent() {
    return (
      <>
        {squeakProfile
          ? ProfileContent()
          : NoProfileContent()}
        {CreateContactProfileDialogContent()}
      </>

    );
  }

  function AddressSqueaksContent() {
    return (
      <>
        {DownloadSqueaksButtonContent()}
        {GridContent()}
        {waitingForSqueaks && <CircularProgress size={24} className={classes.buttonProgress} />}
      </>

    );
  }

  function ViewMoreSqueaksButton() {
    return (
      <>
        <Grid item xs={12}>
          <div className={classes.wrapper}>
            {!waitingForSqueaks
            && (
            <Button
              variant="contained"
              color="primary"
              disabled={waitingForSqueaks}
              onClick={() => {
                const latestSqueak = squeaks.slice(-1).pop();
                getSqueaks(address, SQUEAKS_PER_PAGE, latestSqueak);
              }}
            >
              <ReplayIcon />
              View more squeaks
            </Button>
            )}
            {waitingForSqueaks && <CircularProgress size={48} className={classes.buttonProgress} />}
          </div>
        </Grid>
      </>
    );
  }

  return (
    <>
      {SqueakProfileContent()}
      {AddressSqueaksContent()}
      {DownloadInProgressDialogContent()}
    </>
  );
}
