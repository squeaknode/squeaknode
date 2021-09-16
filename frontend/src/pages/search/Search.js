import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useHistory } from 'react-router-dom';
import {
  Grid,
  Button,
  Box,
  CircularProgress,
  TextField,
} from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';



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
  goToSearchPage,
} from '../../navigation/navigation';

// // styles
// const useStyles = makeStyles((theme) => ({
//   root: {
//     '& .MuiTextField-root': {
//       margin: theme.spacing(1),
//       width: '25ch',
//     },
//   },
// }));

const SQUEAKS_PER_PAGE = 10;

export default function SearchPage() {
  const classes = useStyles();
  const history = useHistory();
  const { searchText } = useParams();
  const [squeaks, setSqueaks] = useState([]);
  const [createContactProfileDialogOpen, setCreateContactProfileDialogOpen] = useState(false);
  const [network, setNetwork] = useState('');
  const [waitingForSqueaks, setWaitingForSqueaks] = useState(false);
  const [inputText, setInputText] = useState(searchText);

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

  const handleChangeSearchInput = (event) => {
    setInputText(event.target.value);
  };

  const handleClickSearch = () => {
    goToSearchPage(history, inputText);
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


    function SearchBar() {
      return (
        <form className={classes.root} noValidate autoComplete="off">
              <div>
                <TextField id="outlined-search" label="Search field" type="search" variant="outlined"
                  onChange={handleChangeSearchInput}
                  value={inputText}
                  onKeyPress={(ev) => {
                    console.log(`Pressed keyCode ${ev.key}`);
                    if (ev.key === 'Enter') {
                      ev.preventDefault();
                      const encodedText = encodeURIComponent(inputText)
                      goToSearchPage(history, encodedText);
                    }
                  }}
                  />
              </div>
              <div>
              <Button
                variant="contained"
                onClick={() => {
                  handleClickSearch();
                }}
              >
                Search
              </Button>
              </div>
            </form>

      );
    }

  return (
    <>
      {SearchBar()}
      {AddressSqueaksContent()}
    </>
  );
}
