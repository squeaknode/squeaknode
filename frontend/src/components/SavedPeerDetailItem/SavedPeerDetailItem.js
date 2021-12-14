import React, { useState } from 'react';
import {
  IconButton,
  Menu,
  MenuItem,
  Typography,
  Button,
} from '@material-ui/core';
import { useHistory } from 'react-router-dom';

import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';

import CardHeader from '@material-ui/core/CardHeader';

import MoreVertIcon from '@material-ui/icons/MoreVert';

// styles
import useStyles from './styles';

import DeletePeerDialog from '../DeletePeerDialog';
import ConfigurePeerDialog from '../ConfigurePeerDialog';

import {
  goToPeerAddressPage,
} from '../../navigation/navigation';

export default function SavedPeerDetailItem({
  savedPeer,
  handleReloadPeer,
  ...props
}) {
  const classes = useStyles();
  const [anchorEl, setAnchorEl] = React.useState(null);

  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [configureDialogOpen, setConfigureDialogOpen] = useState(false);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const history = useHistory();

  const onViewPeerConnectionClick = () => {
    console.log('Handling view peer connection click...');
    handleClose();
    if (!savedPeer) {
      return;
    }
    goToPeerAddressPage(
      history,
      savedPeer.getPeerAddress().getNetwork(),
      savedPeer.getPeerAddress().getHost(),
      savedPeer.getPeerAddress().getPort(),
    );
  };

  const onConfigureClick = () => {
    console.log('Handling configure click...');
    handleClose();
    if (!savedPeer) {
      return;
    }
    setConfigureDialogOpen(true);
  };

  const onDeleteClick = () => {
    console.log('Handling delete click...');
    handleClose();
    if (!savedPeer) {
      return;
    }
    setDeleteDialogOpen(true);
  };

  const handleCloseDeleteDialog = () => {
    setDeleteDialogOpen(false);
  };

  const handleCloseConfigureDialog = () => {
    setConfigureDialogOpen(false);
  };

  function DeletePeerDialogContent() {
    return (
      <>
        <DeletePeerDialog
          open={deleteDialogOpen}
          handleClose={handleCloseDeleteDialog}
          peer={savedPeer}
          reloadPeer={handleReloadPeer}
        />
      </>
    );
  }

  function ConfigurePeerDialogContent() {
    return (
      <>
        <ConfigurePeerDialog
          open={configureDialogOpen}
          handleClose={handleCloseConfigureDialog}
          savedPeer={savedPeer}
          reloadPeer={handleReloadPeer}
        />
      </>
    );
  }


  return (
    <>
      <Card className={classes.root}>

        <CardHeader
          action={(
            <>
              <IconButton aria-label="settings" onClick={handleClick}>
                <MoreVertIcon />
              </IconButton>
              <Menu
                id="simple-menu"
                anchorEl={anchorEl}
                keepMounted
                open={Boolean(anchorEl)}
                onClose={handleClose}
              >
                <MenuItem onClick={onConfigureClick}>Configure</MenuItem>
                <MenuItem onClick={onDeleteClick}>Delete</MenuItem>
              </Menu>
            </>
  )}
          title={savedPeer.getPeerName()}
        />

        <CardContent>
          <Typography variant="body2" color="textSecondary" component="p">
            Network: {savedPeer.getPeerAddress().getNetwork()}
          </Typography>
          <Typography variant="body2" color="textSecondary" component="p">
            Host: {savedPeer.getPeerAddress().getHost()}
          </Typography>
          <Typography variant="body2" color="textSecondary" component="p">
            Port: {savedPeer.getPeerAddress().getPort()}
          </Typography>
          <Typography variant="body2" color="textSecondary" component="p">
            Autoconnect: {savedPeer.getAutoconnect().toString()}
          </Typography>
          <Typography variant="body2" color="textSecondary" component="p">
            Share for free: {savedPeer.getShareForFree().toString()}
          </Typography>
        </CardContent>
        <CardActions>
          <Button
            onClick={() => {
              onViewPeerConnectionClick();
            }}
            size="small"
            color="primary"
          >
            View Peer Connection
          </Button>
        </CardActions>
      </Card>
      {DeletePeerDialogContent()}
      {ConfigurePeerDialogContent()}
    </>
  );
}
