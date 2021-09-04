import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

// components
import SqueakProfileDetailItem from '../../components/SqueakProfileDetailItem';

import {
  getSqueakProfileRequest,
} from '../../squeakclient/requests';

export default function ProfilePage() {
  const { id } = useParams();
  const [squeakProfile, setSqueakProfile] = useState(null);

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

  function ProfileContent() {
    return (
      <>
        {SqueakProfileImageDisplay()}
      </>
    );
  }

  function SqueakProfileImageDisplay() {
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
