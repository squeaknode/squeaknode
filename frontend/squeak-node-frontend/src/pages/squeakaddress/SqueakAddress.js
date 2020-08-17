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
   GetAddressSqueakDisplaysRequest,
   GetSqueakProfileByAddressRequest,
   GetSqueakProfileRequest,
} from "../../proto/squeak_admin_pb"
import { client } from "../../squeakclient/squeakclient"


export default function SqueakAddressPage() {
  var classes = useStyles();
  const history = useHistory();
  const { address } = useParams();
  const [squeakProfile, setSqueakProfile] = useState(null);
  const [squeaks, setSqueaks] = useState([]);
  const [createContactProfileDialogOpen, setCreateContactProfileDialogOpen] = useState(false);

  const getSqueakProfile = (address) => {
        var getSqueakProfileByAddressRequest = new GetSqueakProfileByAddressRequest()
        getSqueakProfileByAddressRequest.setAddress(address);
        console.log(getSqueakProfileByAddressRequest);

        client.getSqueakProfileByAddress(getSqueakProfileByAddressRequest, {}, (err, response) => {
          console.log(response);
          setSqueakProfile(response.getSqueakProfile())
        });
  };
  const getSqueaks = (address) => {
      var getAddressSqueakDisplaysRequest = new GetAddressSqueakDisplaysRequest()
      getAddressSqueakDisplaysRequest.setAddress(address);
      console.log(getAddressSqueakDisplaysRequest);

      client.getAddressSqueakDisplays(getAddressSqueakDisplaysRequest, {}, (err, response) => {
        console.log(response);
        console.log(response.getSqueakDisplayEntriesList());
        setSqueaks(response.getSqueakDisplayEntriesList())
      });
};

  const goToCreateProfilePage = (profileId) => {
    history.push("/app/profile/" + profileId);
  };

  const goToSqueakPage = (hash) => {
    history.push("/app/squeak/" + hash);
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
            goToCreateProfilePage(squeakProfile.getProfileId());
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
              key={squeak.getSqueakHash()}
              handleSqueakClick={() => goToSqueakPage(squeak.getSqueakHash())}
              squeak={squeak}>
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
