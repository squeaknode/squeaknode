import React, { useState } from "react";
import {
  Paper,
  IconButton,
  Menu,
  MenuItem,
  Typography,
  Grid,
  Box,
  Link,
  Divider,
  Button,
} from "@material-ui/core";
import { MoreVert as MoreIcon } from "@material-ui/icons";
import {useHistory} from "react-router-dom";
import classnames from "classnames";

import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';

import CardHeader from '@material-ui/core/CardHeader';
import Avatar from '@material-ui/core/Avatar';

import MoreVertIcon from '@material-ui/icons/MoreVert';
import VpnKeyIcon from '@material-ui/icons/VpnKey';

// styles
import useStyles from "./styles";

import Widget from "../../components/Widget";
import DeleteProfileDialog from "../../components/DeleteProfileDialog";
import ExportPrivateKeyDialog from "../../components/ExportPrivateKeyDialog";
import ConfigureProfileDialog from "../../components/ConfigureProfileDialog";
import UpdateProfileImageDialog from "../../components/UpdateProfileImageDialog";


import {
  syncSqueakRequest,
} from "../../squeakclient/requests"

import {
  getBlockDetailUrl,
} from "../../bitcoin/blockexplorer"
import {
  getProfileImageSrcString,
} from "../../squeakimages/images"
import {
  goToSqueakAddressPage,
} from "../../navigation/navigation"


import moment from 'moment';

export default function SqueakProfileDetailItem({
  squeakProfile,
  handleReloadProfile,
  ...props
}) {
  var classes = useStyles();
  const [anchorEl, setAnchorEl] = React.useState(null);

  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [exportPrivateKeyDialogOpen, setExportPrivateKeyDialogOpen] = useState(false);
  const [configureDialogOpen, setConfigureDialogOpen] = useState(false);
  const [updateImageDialogOpen, setUpdateImageDialogOpen] = useState(false);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const history = useHistory();

  const onViewSqueaksClick = () => {
    console.log("Handling view squeaks click...");
    handleClose();
    if (!squeakProfile) {
      return;
    }
    goToSqueakAddressPage(history, squeakProfile.getAddress());
  }

  const onConfigureClick = () => {
    console.log("Handling configure click...");
    handleClose();
    if (!squeakProfile) {
      return;
    }
    setConfigureDialogOpen(true);
  }

  const onRenameClick = () => {
    console.log("Handling rename click...");
    handleClose();
    if (!squeakProfile) {
      return;
    }
    //handleRenameClick();
  }

  const onChangeImageClick = () => {
    console.log("Handling change image click...");
    handleClose();
    if (!squeakProfile) {
      return;
    }
    setUpdateImageDialogOpen(true);
  }

  const onExportClick = () => {
    console.log("Handling export click...");
    handleClose();
    if (!squeakProfile) {
      return;
    }
    setExportPrivateKeyDialogOpen(true);
  }

  const onDeleteClick = () => {
    console.log("Handling delete click...");
    handleClose();
    if (!squeakProfile) {
      return;
    }
    setDeleteDialogOpen(true);
  }

  const handleCloseDeleteDialog = () => {
     setDeleteDialogOpen(false);
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

    const profileImageBase64String = squeakProfile.getProfileImage();


      function DeleteProfileDialogContent() {
        return (
          <>
            <DeleteProfileDialog
              open={deleteDialogOpen}
              handleClose={handleCloseDeleteDialog}
              profile={squeakProfile}
              ></DeleteProfileDialog>
          </>
        )
      }

      function ExportPrivateKeyDialogContent() {
        return (
          <>
            <ExportPrivateKeyDialog
              open={exportPrivateKeyDialogOpen}
              handleClose={handleCloseExportPrivateKeyDialog}
              profile={squeakProfile}
              ></ExportPrivateKeyDialog>
          </>
        )
      }

      function ConfigureProfileDialogContent() {
        return (
          <>
            <ConfigureProfileDialog
              open={configureDialogOpen}
              handleClose={handleCloseConfigureDialog}
              squeakProfile={squeakProfile}
              reloadProfile={handleReloadProfile}
              ></ConfigureProfileDialog>
          </>
        )
      }

      function UpdateImageDialogContent() {
        return (
          <>
            <UpdateProfileImageDialog
              open={updateImageDialogOpen}
              handleClose={handleCloseUpdateImageDialog}
              squeakProfile={squeakProfile}
              reloadProfile={handleReloadProfile}
              ></UpdateProfileImageDialog>
          </>
        )
      }


    return (
      <>
        <Card className={classes.root}>

        <CardHeader
  action={
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
      {squeakProfile.getHasPrivateKey() &&
        <MenuItem onClick={onExportClick}>Export</MenuItem>
      }
      <MenuItem onClick={onDeleteClick}>Delete</MenuItem>
    </Menu>
    </>
  }
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
            </CardContent>
          <CardActions>
            <Button
              onClick={() => {
                onViewSqueaksClick();
              }}
              size="small" color="primary">
              View Squeaks
            </Button>
          </CardActions>
        </Card>
        {DeleteProfileDialogContent()}
        {ExportPrivateKeyDialogContent()}
        {ConfigureProfileDialogContent()}
        {UpdateImageDialogContent()}
        </>
      );
}
