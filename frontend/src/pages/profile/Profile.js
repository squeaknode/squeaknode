import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'react-router-dom';

import {
  CircularProgress,
  CardHeader,
  Card,
} from '@material-ui/core';

// components
import SqueakProfileDetailItem from '../../components/SqueakProfileDetailItem';

import useStyles from './styles';


import {
  getSqueakProfileRequest,
} from '../../squeakclient/requests';

export default function ProfilePage() {
  const classes = useStyles();
  const { id } = useParams();
  const [squeakProfile, setSqueakProfile] = useState(null);
  const [waitingForProfile, setWaitingForProfile] = useState(false);

  const handleGetSqueakProfileErr = (err) => {
    setSqueakProfile(null);
  };

  const getSqueakProfile = useCallback(() => {
    setWaitingForProfile(true);
    getSqueakProfileRequest(id, (profile => {
      setWaitingForProfile(false);
      setSqueakProfile(profile);
    }), handleGetSqueakProfileErr);
  },
  [id]);

  useEffect(() => {
    getSqueakProfile(id);
  }, [getSqueakProfile, id]);

  const handleReloadProfile = () => {
    getSqueakProfile(id);
  };

  function ProfileContent() {
    return (
      <>
      {squeakProfile
        ? SqueakProfileDisplay()
        : NoSqueakProfileDisplay()}
      </>
    );
  }

  function SqueakProfileDisplay() {
    return (
      <SqueakProfileDetailItem
        squeakProfile={squeakProfile}
        handleReloadProfile={handleReloadProfile}
      />
    );
  }

  function NoSqueakProfileDisplay() {
    return (
      <Card
        className={classes.root}
      >
        <CardHeader
          subheader="Profile not found."
        />
      </Card>
    );
  }

  function WaitingIndicator() {
    return (
      <CircularProgress size={48} className={classes.buttonProgress} />
    );
  }

  return (
    <>
      {!waitingForProfile
        ? ProfileContent()
        : WaitingIndicator()}
    </>
  );
}
