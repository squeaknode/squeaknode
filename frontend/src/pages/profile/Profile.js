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
} from "@material-ui/core";

// styles
import useStyles from "./styles";

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
import DeleteProfileDialog from "../../components/DeleteProfileDialog";

import {
  getSqueakProfileRequest,
  setSqueakProfileFollowingRequest,
  setSqueakProfileSharingRequest,
} from "../../squeakclient/requests"


export default function ProfilePage() {
  var classes = useStyles();
  const { id } = useParams();
  const [squeakProfile, setSqueakProfile] = useState(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const history = useHistory();

  const getSqueakProfile = (id) => {
    getSqueakProfileRequest(id, setSqueakProfile);
  };
  const setFollowing = (id, following) => {
    setSqueakProfileFollowingRequest(id, following, () => {
      getSqueakProfile(id);
    })
  };
  const setSharing = (id, sharing) => {
    setSqueakProfileSharingRequest(id, sharing, () => {
      getSqueakProfile(id);
    })
  };

  const goToSqueakAddressPage = (squeakAddress) => {
    history.push("/app/squeakaddress/" + squeakAddress);
  };


  useEffect(()=>{
    getSqueakProfile(id)
  },[id]);

  const handleClickOpenDeleteDialog = () => {
    setDeleteDialogOpen(true);
  };

  const handleCloseDeleteDialog = () => {
     setDeleteDialogOpen(false);
  };

  const handleSettingsFollowingChange = (event) => {
    console.log("Following changed for profile id: " + id);
    console.log("Following changed to: " + event.target.checked);
    setFollowing(id, event.target.checked);
  };

  const handleSettingsSharingChange = (event) => {
    console.log("Sharing changed for profile id: " + id);
    console.log("Sharing changed to: " + event.target.checked);
    setSharing(id, event.target.checked);
  };

  function NoProfileContent() {
    return (
      <p>
        No profile loaded
      </p>
    )
  }

  function ProfileContent() {
    return (
      <>
        <p>
          Profile name: {squeakProfile.getProfileName()}
        </p>
        {ProfileSettingsForm()}
        {ViewSqueaksButton()}
        {DeleteProfileButton()}
      </>
    )
  }

  function ProfileSettingsForm() {
    return (
      <FormControl component="fieldset">
        <FormLabel component="legend">Profile settings</FormLabel>
        <FormGroup>
          <FormControlLabel
            control={<Switch checked={squeakProfile.getFollowing()} onChange={handleSettingsFollowingChange} />}
            label="Following"
          />
          <FormControlLabel
            control={<Switch checked={squeakProfile.getSharing()} onChange={handleSettingsSharingChange} />}
            label="Sharing"
          />
        </FormGroup>
      </FormControl>
    )
  }

  function DeleteProfileButton() {
    return (
      <>
      <Grid item xs={12}>
        <div className={classes.root}>
          <Button
            variant="contained"
            onClick={() => {
              handleClickOpenDeleteDialog();
            }}>Delete Profile
          </Button>
        </div>
      </Grid>
      </>
    )
  }

  function ViewSqueaksButton() {
    return (
      <>
      <Grid item xs={12}>
        <div className={classes.root}>
          <Button
            variant="contained"
            onClick={() => {
              goToSqueakAddressPage(squeakProfile.getAddress());
            }}>View Squeaks
          </Button>
        </div>
      </Grid>
      </>
    )
  }

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

  return (
    <>
      <PageTitle title={'Squeak Profile: ' + (squeakProfile ? squeakProfile.getProfileName() : null)} />
      <div>
      {squeakProfile
        ? ProfileContent()
        : NoProfileContent()
      }
      </div>
      {DeleteProfileDialogContent()}
    </>
  );
}
