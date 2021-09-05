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
import CardMedia from '@material-ui/core/CardMedia';

import CardHeader from '@material-ui/core/CardHeader';

import MoreVertIcon from '@material-ui/icons/MoreVert';
import VpnKeyIcon from '@material-ui/icons/VpnKey';
import LocalOfferIcon from '@material-ui/icons/LocalOffer';

// styles
import useStyles from './styles';

import DeleteProfileDialog from '../DeleteProfileDialog';
import RenameProfileDialog from '../RenameProfileDialog';
import ExportPrivateKeyDialog from '../ExportPrivateKeyDialog';
import ConfigureProfileDialog from '../ConfigureProfileDialog';
import UpdateProfileImageDialog from '../UpdateProfileImageDialog';
import ClearProfileImageDialog from '../ClearProfileImageDialog';
import SqueakProfileFollowingIndicator from '../SqueakProfileFollowingIndicator';

import {
  getProfileImageSrcString,
} from '../../squeakimages/images';
import {
  goToSqueakAddressPage,
} from '../../navigation/navigation';

export default function SqueakProfileDetailItem({
  squeakProfile,
  handleReloadProfile,
  ...props
}) {
  const classes = useStyles();
  const [anchorEl, setAnchorEl] = React.useState(null);

  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [renameDialogOpen, setRenameDialogOpen] = useState(false);
  const [exportPrivateKeyDialogOpen, setExportPrivateKeyDialogOpen] = useState(false);
  const [configureDialogOpen, setConfigureDialogOpen] = useState(false);
  const [updateImageDialogOpen, setUpdateImageDialogOpen] = useState(false);
  const [clearImageDialogOpen, setClearImageDialogOpen] = useState(false);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const history = useHistory();

  const onViewSqueaksClick = () => {
    console.log('Handling view squeaks click...');
    handleClose();
    if (!squeakProfile) {
      return;
    }
    goToSqueakAddressPage(history, squeakProfile.getAddress());
  };

  const onConfigureClick = () => {
    console.log('Handling configure click...');
    handleClose();
    if (!squeakProfile) {
      return;
    }
    setConfigureDialogOpen(true);
  };

  const onRenameClick = () => {
    console.log('Handling rename click...');
    handleClose();
    if (!squeakProfile) {
      return;
    }
    setRenameDialogOpen(true);
  };

  const onChangeImageClick = () => {
    console.log('Handling change image click...');
    handleClose();
    if (!squeakProfile) {
      return;
    }
    setUpdateImageDialogOpen(true);
  };

  const onClearImageClick = () => {
    console.log('Handling clear image click...');
    handleClose();
    if (!squeakProfile) {
      return;
    }
    setClearImageDialogOpen(true);
  };

  const onExportClick = () => {
    console.log('Handling export click...');
    handleClose();
    if (!squeakProfile) {
      return;
    }
    setExportPrivateKeyDialogOpen(true);
  };

  const onDeleteClick = () => {
    console.log('Handling delete click...');
    handleClose();
    if (!squeakProfile) {
      return;
    }
    setDeleteDialogOpen(true);
  };

  const handleCloseDeleteDialog = () => {
    setDeleteDialogOpen(false);
  };

  const handleCloseRenameDialog = () => {
    setRenameDialogOpen(false);
  };

  const handleCloseExportPrivateKeyDialog = () => {
    setExportPrivateKeyDialogOpen(false);
  };

  const handleCloseConfigureDialog = () => {
    setConfigureDialogOpen(false);
  };

  const handleCloseUpdateImageDialog = () => {
    setUpdateImageDialogOpen(false);
  };

  const handleCloseClearImageDialog = () => {
    setClearImageDialogOpen(false);
  };

  function DeleteProfileDialogContent() {
    return (
      <>
        <DeleteProfileDialog
          open={deleteDialogOpen}
          handleClose={handleCloseDeleteDialog}
          profile={squeakProfile}
          reloadProfile={handleReloadProfile}
        />
      </>
    );
  }

  function RenameProfileDialogContent() {
    return (
      <>
        <RenameProfileDialog
          open={renameDialogOpen}
          handleClose={handleCloseRenameDialog}
          profile={squeakProfile}
          reloadProfile={handleReloadProfile}
        />
      </>
    );
  }

  function ExportPrivateKeyDialogContent() {
    return (
      <>
        <ExportPrivateKeyDialog
          open={exportPrivateKeyDialogOpen}
          handleClose={handleCloseExportPrivateKeyDialog}
          profile={squeakProfile}
        />
      </>
    );
  }

  function ConfigureProfileDialogContent() {
    return (
      <>
        <ConfigureProfileDialog
          open={configureDialogOpen}
          handleClose={handleCloseConfigureDialog}
          squeakProfile={squeakProfile}
          reloadProfile={handleReloadProfile}
        />
      </>
    );
  }

  function UpdateImageDialogContent() {
    return (
      <>
        <UpdateProfileImageDialog
          open={updateImageDialogOpen}
          handleClose={handleCloseUpdateImageDialog}
          squeakProfile={squeakProfile}
          reloadProfile={handleReloadProfile}
        />
      </>
    );
  }

  function ClearImageDialogContent() {
    return (
      <>
        <ClearProfileImageDialog
          open={clearImageDialogOpen}
          handleClose={handleCloseClearImageDialog}
          squeakProfile={squeakProfile}
          reloadProfile={handleReloadProfile}
        />
      </>
    );
  }

  function CustomPriceContent() {
    return (
      (squeakProfile &&
        <Typography variant="body2" color="textSecondary" component="p">
          <LocalOfferIcon />
          {' '}
          Using custom price:
        </Typography>
      )
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
                <MenuItem onClick={onRenameClick}>Rename</MenuItem>
                <MenuItem onClick={onChangeImageClick}>Change Image</MenuItem>
                <MenuItem onClick={onClearImageClick}>Clear Image</MenuItem>
                {squeakProfile.getHasPrivateKey()
        && <MenuItem onClick={onExportClick}>Export</MenuItem>}
                <MenuItem onClick={onDeleteClick}>Delete</MenuItem>
              </Menu>
            </>
  )}
          title={squeakProfile.getProfileName()}
        />

        <CardMedia
          component="img"
          className={classes.media}
          image={`${getProfileImageSrcString(squeakProfile)}`}
          title="Profile Image"
        />
        <CardContent>
          <Typography gutterBottom variant="h5" component="h2">
            {squeakProfile.getHasPrivateKey() && <VpnKeyIcon />}
          </Typography>
          <Typography variant="body2" color="textSecondary" component="p">
            {squeakProfile.getAddress()}
          </Typography>
          <SqueakProfileFollowingIndicator
            squeakProfile={squeakProfile}
          />
          <CustomPriceContent

          />
        </CardContent>
        <CardActions>
          <Button
            onClick={() => {
              onViewSqueaksClick();
            }}
            size="small"
            color="primary"
          >
            View Squeaks
          </Button>
        </CardActions>
      </Card>
      {DeleteProfileDialogContent()}
      {RenameProfileDialogContent()}
      {ExportPrivateKeyDialogContent()}
      {ConfigureProfileDialogContent()}
      {UpdateImageDialogContent()}
      {ClearImageDialogContent()}
    </>
  );
}
