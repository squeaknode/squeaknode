import React, { useState, useEffect } from 'react';
import { useHistory, useParams } from 'react-router-dom';

// styles
import useStyles from './styles';

// components
import SqueakProfileDetailItem from '../../components/SqueakProfileDetailItem';

import {
  getSqueakProfileRequest,
} from '../../squeakclient/requests';

import {
  goToSqueakAddressPage,
} from '../../navigation/navigation';

export default function ProfilePage() {
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

  useEffect(() => {
    getSqueakProfile(id);
  }, [id]);

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
    );
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
      {squeakProfile
        && ProfileContent()}
    </>
  );
}
