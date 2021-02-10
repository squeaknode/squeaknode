import React, { useState, useEffect } from 'react';
import {useHistory} from "react-router-dom";
import { useParams } from 'react-router-dom';
import {
  Grid,
  FormLabel,
  FormControl,
  FormGroup,
  FormControlLabel,
  FormHelperText,
  Switch,
  Button,
  Link,
  Typography,
} from "@material-ui/core";

import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';

import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import CardHeader from '@material-ui/core/CardHeader';
import Avatar from '@material-ui/core/Avatar';
import IconButton from '@material-ui/core/IconButton';
import MoreVertIcon from '@material-ui/icons/MoreVert';

import VpnKeyIcon from '@material-ui/icons/VpnKey';

// styles
import useStyles from "./styles";

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
import DeleteProfileDialog from "../../components/DeleteProfileDialog";
import ExportPrivateKeyDialog from "../../components/ExportPrivateKeyDialog";
import ConfigureProfileDialog from "../../components/ConfigureProfileDialog";
import UpdateProfileImageDialog from "../../components/UpdateProfileImageDialog";
import SqueakProfileDetailItem from "../../components/SqueakProfileDetailItem";

import {
  getSqueakProfileRequest,
  setSqueakProfileFollowingRequest,
  setSqueakProfileSharingRequest,
} from "../../squeakclient/requests"

import {
  getProfileImageSrcString,
} from "../../squeakimages/images"
import {
  goToSqueakAddressPage,
} from "../../navigation/navigation"


export default function ProfilePage() {
  var classes = useStyles();
  const { id } = useParams();
  const [squeakProfile, setSqueakProfile] = useState(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [exportPrivateKeyDialogOpen, setExportPrivateKeyDialogOpen] = useState(false);
  const [configureDialogOpen, setConfigureDialogOpen] = useState(false);
  const [updateImageDialogOpen, setUpdateImageDialogOpen] = useState(false);
  const history = useHistory();

  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleGetSqueakProfileErr = (err) => {
    setSqueakProfile(null);
  };

  const getSqueakProfile = (id) => {
    getSqueakProfileRequest(id, setSqueakProfile, handleGetSqueakProfileErr);
  };

  useEffect(()=>{
    getSqueakProfile(id)
  },[id]);

  const handleReloadProfile = () => {
    getSqueakProfile(id);
  };

  const handleViewSqueaks = () => {
    goToSqueakAddressPage(history, squeakProfile.getAddress());
  };

  function ProfileContent() {
    return (
      <>
        {SqueakProfileImageDisplay()}
      </>
    )
  }

  function SqueakProfileImageDisplay() {
    const profileImageBase64String = squeakProfile.getProfileImage();
    return (
        <SqueakProfileDetailItem
          squeakProfile={squeakProfile}
          handleReloadProfile={handleReloadProfile}
        />
      );
  }

  return (
    <>
      <PageTitle title={'Squeak Profile: ' + (squeakProfile ? squeakProfile.getProfileName() : null)} />
      <div>
      {squeakProfile &&
        ProfileContent()}
      </div>
    </>
  );
}
