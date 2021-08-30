import React, { useState, useEffect } from 'react';
import { useParams, useHistory } from 'react-router-dom';
import {
  Grid,
  Button,
} from '@material-ui/core';

// styles

// components

import TimelineDot from '@material-ui/lab/TimelineDot';
import Paper from '@material-ui/core/Paper';

import FaceIcon from '@material-ui/icons/Face';
import CreateContactProfileDialog from '../../components/CreateContactProfileDialog';
import SqueakList from '../../components/SqueakList';
import useStyles from './styles';

import {
  getSqueakProfileByAddressRequest,
  getAddressSqueakDisplaysRequest,
  getNetworkRequest,
  subscribeAddressSqueakDisplaysRequest,
} from '../../squeakclient/requests';
import {
  goToSqueakAddressPage,
  goToProfilePage,
} from '../../navigation/navigation';

export default function SqueakAddressPage() {
  const classes = useStyles();
  const history = useHistory();
  const { address } = useParams();
  const [squeakProfile, setSqueakProfile] = useState(null);
  const [squeaks, setSqueaks] = useState([]);
  const [createContactProfileDialogOpen, setCreateContactProfileDialogOpen] = useState(false);
  const [network, setNetwork] = useState('');

  const getSqueakProfile = (address) => {
    getSqueakProfileByAddressRequest(address, setSqueakProfile);
  };
  const getSqueaks = (address) => {
    getAddressSqueakDisplaysRequest(address, setSqueaks);
  };
  const subscribeSqueaks = (hash) => {
    return subscribeAddressSqueakDisplaysRequest(address, (resp) => {
      setSqueaks([resp].concat(squeaks));
    });
  };
  const getNetwork = () => {
    getNetworkRequest(setNetwork);
  };

  const handleClickOpenCreateContactProfileDialog = () => {
    setCreateContactProfileDialogOpen(true);
  };

  const handleCloseCreateContactProfileDialog = () => {
    setCreateContactProfileDialogOpen(false);
  };

  useEffect(() => {
    getSqueakProfile(address);
  }, [address]);
  useEffect(() => {
    getSqueaks(address);
  }, [address]);
  useEffect(() => {
    const stream = subscribeSqueaks(address);
    return () => stream.cancel();
  }, [squeaks, address]);
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

  function TimelineUserAvatar(squeak) {
    const handleAvatarClick = () => {
      console.log('Avatar clicked...');
      goToSqueakAddressPage(history, squeak.getAuthorAddress());
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
      {squeakProfile
        ? ProfileContent()
        : NoProfileContent()}
      {GridContent()}
      {CreateContactProfileDialogContent()}
    </>
  );
}
