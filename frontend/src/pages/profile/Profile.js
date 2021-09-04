import React, { useState, useEffect, useCallback } from 'react';
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

  const getSqueakProfile = useCallback(() => {
    getSqueakProfileRequest(id, setSqueakProfile, handleGetSqueakProfileErr);
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
