import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';

import {
  IconButton,
  Menu,
  MenuItem,
  Typography,
  Button,
} from '@material-ui/core';

import Card from '@material-ui/core/Card';
import Box from '@material-ui/core/Box';
import CardHeader from '@material-ui/core/CardHeader';

// icons
import VpnKeyIcon from '@material-ui/icons/VpnKey';
import LocalOfferIcon from '@material-ui/icons/LocalOffer';
import MoreVertIcon from '@material-ui/icons/MoreVert';

import useStyles from '../../pages/wallet/styles';
import SqueakUserAvatar from '../SqueakUserAvatar';
import SqueakProfileFollowingIndicator from '../SqueakProfileFollowingIndicator';
import DeleteTwitterAccountDialog from '../DeleteTwitterAccountDialog';



export default function TwitterAccountListItem({
  accountEntry,
  reloadAccountsFn,
  ...props
}) {
  const classes = useStyles({
    clickable: true,
  });

  const [anchorEl, setAnchorEl] = useState(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);


  const handleClickMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleCloseMenu = () => {
    setAnchorEl(null);
  };

  const onDeleteClick = () => {
    console.log('Handling delete click...');
    handleCloseMenu();
    setDeleteDialogOpen(true);
  };

  const handleCloseDeleteDialog = () => {
    setDeleteDialogOpen(false);
  };

  // const onProfileClick = (event) => {
  //   event.preventDefault();
  //   console.log('Handling profile click...');
  //   const profileId = profile.getProfileId();
  //   // const host = getPeerHost();
  //   // const port = getPeerPort();
  //   goToProfilePage(history, profileId);
  // };

  // const getPeerHost = () => {
  //   const address = peer.getAddress();
  //   if (address == null) {
  //     return null;
  //   }
  //   const pieces = address.split(":");
  //   return pieces[0];
  // }
  //
  // const getPeerPort = () => {
  //   const address = peer.getAddress();
  //   if (address == null) {
  //     return null;
  //   }
  //   const pieces = address.split(":");
  //   if (pieces.length < 2) {
  //     return null;
  //   }
  //   return pieces[1];
  // }

  const twitterHandle = accountEntry.getHandle();
  const profile = accountEntry.getProfile();

  function DeleteTwitterAccountDialogContent() {
    return (
      <>
        <DeleteTwitterAccountDialog
          open={deleteDialogOpen}
          handleClose={handleCloseDeleteDialog}
          twitterAccount={accountEntry}
          reloadAccountsFn={reloadAccountsFn}
        />
      </>
    );
  }

  function AccountCardContent() {
    const name = profile.getProfileName();
    const address = profile.getAddress();
    return (
      <>
        <Box>
          {`Profile Name: ${name}`}
        </Box>
        <Box>
          {`Address: ${address}`}
        </Box>
      </>
    );
  }

  return (
    <>
    <Card
      className={classes.root}
      // onClick={alert('do something')}
    >
      <CardHeader
      action={(
        <>
          <IconButton aria-label="settings" onClick={handleClickMenu}>
            <MoreVertIcon />
          </IconButton>
          <Menu
            id="simple-menu"
            anchorEl={anchorEl}
            keepMounted
            open={Boolean(anchorEl)}
            onClose={handleCloseMenu}
          >
            <MenuItem onClick={onDeleteClick}>Delete</MenuItem>
          </Menu>
        </>
      )}
        avatar={(
          <SqueakUserAvatar
            squeakAddress={(profile && profile.getAddress())}
            squeakProfile={profile}
          />
)}
        title={`Twitter handle: ${twitterHandle}`}
        subheader={AccountCardContent()}
      />
    </Card>
    {DeleteTwitterAccountDialogContent()}
    </>
  );
}
