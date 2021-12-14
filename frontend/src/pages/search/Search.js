import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { useParams, useHistory } from 'react-router-dom';
import {
  Grid,
  Button,
  CircularProgress,
  TextField,
} from '@material-ui/core';

import ReplayIcon from '@material-ui/icons/Replay';

import SqueakList from '../../components/SqueakList';
import useStyles from './styles';

import {
  getSearchSqueakDisplaysRequest,
  getNetworkRequest,
  // subscribeAddressSqueakDisplaysRequest,
} from '../../squeakclient/requests';
import {
  goToSearchPage,
  reloadRoute,
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
  const [squeaks, setSqueaks] = useState(null);
  const [network, setNetwork] = useState('');
  const [waitingForSqueaks, setWaitingForSqueaks] = useState(false);
  const [inputText, setInputText] = useState('');

  const initialLoadComplete = useMemo(() => (squeaks), [squeaks]);

  const urlDecodedSearchText = searchText ? decodeURIComponent(searchText) : '';

  const getSqueaks = useCallback((urlDecodedSearchText, limit, lastEntry) => {
    setWaitingForSqueaks(true);
    getSearchSqueakDisplaysRequest(urlDecodedSearchText, limit, lastEntry, handleLoadedAddressSqueaks);
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
    resetResults();
    const encodedText = encodeURIComponent(inputText);
    if (encodedText === searchText) {
      reloadRoute(history);
    } else {
      goToSearchPage(history, encodedText);
    }
  };

  const resetResults = () => {
    setSqueaks(null);
  };

  useEffect(() => {
    resetResults();
    getSqueaks(urlDecodedSearchText, SQUEAKS_PER_PAGE, null);
  }, [getSqueaks, urlDecodedSearchText]);
  useEffect(() => {
    setInputText(urlDecodedSearchText);
  }, [urlDecodedSearchText]);
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
            {(squeaks)
              ? SqueaksContent()
              : NoSqueaksContent()}
          {ViewMoreSqueaksButton()}
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
                getSqueaks(urlDecodedSearchText, SQUEAKS_PER_PAGE, latestSqueak);
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
          <TextField
            id="outlined-search"
            label="Search field"
            type="search"
            variant="outlined"
            onChange={handleChangeSearchInput}
            value={inputText}
            onKeyPress={(ev) => {
              console.log(`Pressed keyCode ${ev.key}`);
              if (ev.key === 'Enter') {
                ev.preventDefault();
                handleClickSearch();
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

  function WaitingIndicator() {
    return (
      <CircularProgress size={48} className={classes.buttonProgress} />
    );
  }

  return (
    <>
      {(initialLoadComplete)
        ? (
          <>
            {SearchBar()}
            {searchText && AddressSqueaksContent()}
          </>
        )
        : WaitingIndicator()}
    </>
  );
}
