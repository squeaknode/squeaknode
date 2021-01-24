import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {useHistory} from "react-router-dom";
import {
   Grid,
   Button,
   Box,
} from "@material-ui/core";

// styles
import useStyles from "./styles";

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
import SqueakThreadItem from "../../components/SqueakThreadItem";
import CreateContactProfileDialog from "../../components/CreateContactProfileDialog";

import {
  getSqueakProfileByAddressRequest,
  getAddressSqueakDisplaysRequest,
  getNetworkRequest,
} from "../../squeakclient/requests"
import {navigateTo, PROFILE_VIEW} from "../../navigation/routes";


export default function SqueakAddressPage() {
  var classes = useStyles();
  const history = useHistory();
  const { address } = useParams();
  const [squeakProfile, setSqueakProfile] = useState(null);
  const [squeaks, setSqueaks] = useState([]);
  const [createContactProfileDialogOpen, setCreateContactProfileDialogOpen] = useState(false);
  const [network, setNetwork] = useState("");

  const getSqueakProfile = (address) => {
        getSqueakProfileByAddressRequest(address, setSqueakProfile);
  };
  const getSqueaks = (address) => {
      getAddressSqueakDisplaysRequest(address, setSqueaks);
  };
  const getNetwork = () => {
      getNetworkRequest(setNetwork);
  };

  const handleClickOpenCreateContactProfileDialog = () => {
    setCreateContactProfileDialogOpen(true);
  };

  const handleCloseCreateContactProfileDialog = () => {
    setCreateContactProfileDialogOpen(false);
  };

  useEffect(()=>{
    getSqueakProfile(address)
  },[address]);
  useEffect(()=>{
    getSqueaks(address)
  },[address]);
  useEffect(()=>{
    getNetwork()
  },[]);

  function NoProfileContent() {
    return (
      <div>
        No profile for address.
        <Button variant="contained" onClick={() => {
            handleClickOpenCreateContactProfileDialog();
          }}>Create Profile</Button>
      </div>
    )
  }

  function ProfileContent() {
    return (
      <div className={classes.root}>
        Profile:
        <Button variant="contained" onClick={() => {
            navigateTo(history, PROFILE_VIEW, [squeakProfile.getProfileId()]);
          }}>{squeakProfile.getProfileName()}</Button>
      </div>
    )
  }

  function NoSqueaksContent() {
    return (
      <div>
        Unable to load squeaks.
      </div>
    )
  }

  function SqueaksContent() {
    return (
      <>
        <div>
          {squeaks.map(squeak =>
            <Box
              p={1}
              key={squeak.getSqueakHash()}
              >
            <SqueakThreadItem
              hash={squeak.getSqueakHash()}
              key={squeak.getSqueakHash()}
              squeak={squeak}
              network={network}>
            </SqueakThreadItem>
            </Box>
          )}
        </div>
      </>
    )
  }

  function CreateContactProfileDialogContent() {
    return (
      <>
        <CreateContactProfileDialog
          open={createContactProfileDialogOpen}
          handleClose={handleCloseCreateContactProfileDialog}
          initialAddress={address}
          ></CreateContactProfileDialog>
      </>
    )
  }

  return (
    <>
      <PageTitle title={'Squeak Address: ' + address} />
      {squeakProfile
        ? ProfileContent()
        : NoProfileContent()
      }
      {(squeaks)
        ? SqueaksContent()
        : NoSqueaksContent()
      }
      {CreateContactProfileDialogContent()}
    </>
  );
}
