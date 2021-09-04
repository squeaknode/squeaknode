import React, { useState } from 'react';
import {
  IconButton,
  Grid,
  Divider,
} from '@material-ui/core';
import { useHistory } from 'react-router-dom';

import ReplyIcon from '@material-ui/icons/Reply';
import RepeatIcon from '@material-ui/icons/Repeat';
import FavoriteIcon from '@material-ui/icons/Favorite';
import DeleteIcon from '@material-ui/icons/Delete';
import ZoomInIcon from '@material-ui/icons/ZoomIn';

// styles
import useStyles from './styles';

import MakeSqueakDialog from '../MakeSqueakDialog';
import DeleteSqueakDialog from '../DeleteSqueakDialog';
import SqueakDetailsDialog from '../SqueakDetailsDialog';

import {
  likeSqueakRequest,
  unlikeSqueakRequest,
} from '../../squeakclient/requests';

export default function SqueakActionBar({
  hash,
  squeak,
  network,
  reloadSqueak,
  ...props
}) {
  const [replyDialogOpen, setReplyDialogOpen] = useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [viewDetailsDialogOpen, setViewDetailsDialogOpen] = useState(false);

  const handleClickOpenReplyDialog = () => {
    setReplyDialogOpen(true);
  };

  const handleCloseReplyDialog = () => {
    setReplyDialogOpen(false);
  };

  const handleClickOpenDeleteDialog = () => {
    setDeleteDialogOpen(true);
    console.log(`deleteDialogOpen: ${deleteDialogOpen}`);
  };

  const handleCloseDeleteDialog = () => {
    setDeleteDialogOpen(false);
  };

  const handleClickOpenViewDetailsDialog = () => {
    setViewDetailsDialogOpen(true);
  };

  const handleCloseViewDetailsDialog = () => {
    setViewDetailsDialogOpen(false);
  };

  const handleLikeSqueak = () => {
    console.log('liked.');
    likeSqueakRequest(hash, (response) => {
      reloadSqueak();
    });
  };

  const handleUnlikeSqueak = () => {
    console.log('unliked.');
    unlikeSqueakRequest(hash, (response) => {
      reloadSqueak();
    });
  };

  const onReplyClick = (event) => {
    event.preventDefault();
    event.stopPropagation();
    console.log('Handling reply click...');
    if (!squeak) {
      return;
    }
    handleClickOpenReplyDialog();
  };

  const onResqueakClick = (event) => {
    event.preventDefault();
    event.stopPropagation();
    console.log('Handling resqueak click...');
    if (!squeak) {

    }
    // TODO: handleClickOpenReplyDialog();
  };

  const onLikeClick = (event) => {
    event.preventDefault();
    event.stopPropagation();
    console.log('Handling like click...');
    if (!squeak) {
      return;
    }
    handleLikeSqueak();
  };

  const onUnlikeClick = (event) => {
    event.preventDefault();
    event.stopPropagation();
    console.log('Handling like click...');
    if (!squeak) {
      return;
    }
    handleUnlikeSqueak();
  };

  const onDeleteClick = (event) => {
    event.preventDefault();
    event.stopPropagation();
    console.log('Handling delete click...');
    if (!squeak) {
      return;
    }
    handleClickOpenDeleteDialog();
    event.stopPropagation();
  };

  const onZoomInClick = (event) => {
    event.preventDefault();
    event.stopPropagation();
    console.log('Handling zoomin click...');
    if (!squeak) {
      return;
    }
    handleClickOpenViewDetailsDialog();
  };

  function MakeSqueakDialogContent() {
    return (
      <>
        <MakeSqueakDialog
          open={replyDialogOpen}
          handleClose={handleCloseReplyDialog}
          replytoSqueak={squeak}
        />
      </>
    );
  }

  function DeleteSqueakDialogContent() {
    return (
      <>
        <DeleteSqueakDialog
          open={deleteDialogOpen}
          handleClose={handleCloseDeleteDialog}
          squeakToDelete={squeak}
        />
      </>
    );
  }

  function ViewDetailsDialogContent() {
    return (
      <>
        {squeak
            && (
            <SqueakDetailsDialog
              open={viewDetailsDialogOpen}
              handleClose={handleCloseViewDetailsDialog}
              hash={hash}
              squeak={squeak}
            />
            )}
      </>
    );
  }

  function ActionBarContent() {
    return (
      <>
        <Divider />
        <Grid
          container
          direction="row"
          justify="flex-start"
          alignItems="flex-start"
        >
          <Grid item xs={3} sm={1}>
            {ReplyIconContent()}
          </Grid>
          <Grid item xs={3} sm={1}>
            {ResqueakIconContent()}
          </Grid>
          <Grid item xs={3} sm={1}>
            {LikeIconContent()}
          </Grid>
          <Grid item xs={3} sm={1}>
            {DeleteIconContent()}
          </Grid>
          <Grid item xs={3} sm={1}>
            {DetailsIconContent()}
          </Grid>
        </Grid>
      </>
    );
  }

  function ReplyIconContent() {
    return (
      <IconButton
        aria-label="reply"
        onClick={onReplyClick}
      >
        <ReplyIcon />
      </IconButton>
    );
  }

  function ResqueakIconContent() {
    return (
      <IconButton
        aria-label="resqueak"
        onClick={onResqueakClick}
      >
        <RepeatIcon />
      </IconButton>
    );
  }

  function LikeIconContent() {
    if (squeak && !squeak.getLikedTimeS()) {
      return (
        <IconButton
          aria-label="like"
          onClick={onLikeClick}
        >
          <FavoriteIcon />
        </IconButton>
      );
    }
    return (
      <IconButton
        aria-label="unlike"
        onClick={onUnlikeClick}
      >
        <FavoriteIcon
          color="secondary"
        />
      </IconButton>
    );
  }

  function DeleteIconContent() {
    return (
      <IconButton
        aria-label="delete"
        onClick={onDeleteClick}
      >
        <DeleteIcon />
      </IconButton>
    );
  }

  function DetailsIconContent() {
    return (
      <IconButton
        aria-label="details"
        onClick={onZoomInClick}
      >
        <ZoomInIcon />
      </IconButton>
    );
  }

  return (
    <>
      {ActionBarContent()}
      {MakeSqueakDialogContent()}
      {DeleteSqueakDialogContent()}
      {ViewDetailsDialogContent()}
    </>
  );
}
