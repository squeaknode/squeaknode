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
import SqueakList from '../../components/SqueakList';
import useStyles from './styles';

import {
  getSearchSqueakDisplaysRequest,
  getNetworkRequest,
  // subscribeAddressSqueakDisplaysRequest,
} from '../../squeakclient/requests';
import {
  goToProfilePage,
} from '../../navigation/navigation';

const SQUEAKS_PER_PAGE = 10;

export default function SearchPage() {
  const classes = useStyles();
  const history = useHistory();
  const { searchText } = useParams();
  const [squeaks, setSqueaks] = useState([]);
  const [createContactProfileDialogOpen, setCreateContactProfileDialogOpen] = useState(false);
  const [network, setNetwork] = useState('');
  const [waitingForSqueaks, setWaitingForSqueaks] = useState(false);

  const getSqueaks = useCallback((searchText, limit, lastEntry) => {
    setWaitingForSqueaks(true);
    getSearchSqueakDisplaysRequest(searchText, limit, lastEntry, handleLoadedAddressSqueaks);
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

  useEffect(() => {
    getSqueaks(searchText, SQUEAKS_PER_PAGE, null);
  }, [getSqueaks, searchText]);
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

  function AddressSqueaksContent() {
    return (
      <>
        <p>Search bar here...</p>
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
                getSqueaks(searchText, SQUEAKS_PER_PAGE, latestSqueak);
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
      <p>Search bar here...</p>
      {AddressSqueaksContent()}
    </>
  );
}
