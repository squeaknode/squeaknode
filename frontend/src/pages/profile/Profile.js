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
import ExportPrivateKeyDialog from "../../components/ExportPrivateKeyDialog";

import {
  getSqueakProfileRequest,
  setSqueakProfileFollowingRequest,
  setSqueakProfileSharingRequest,
} from "../../squeakclient/requests"
import {navigateTo, PROFILE_VIEW, SQUEAK_ADDRESS_VIEW} from "../../navigation/routes";


export default function ProfilePage() {
  var classes = useStyles();
  const { id } = useParams();
  const [squeakProfile, setSqueakProfile] = useState(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [exportPrivateKeyDialogOpen, setExportPrivateKeyDialogOpen] = useState(false);
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

  useEffect(()=>{
    getSqueakProfile(id)
  },[id]);

  const handleClickOpenDeleteDialog = () => {
    setDeleteDialogOpen(true);
  };

  const handleClickOpenExportPrivateKeyDialog = () => {
    setExportPrivateKeyDialogOpen(true);
  };

  const handleCloseDeleteDialog = () => {
     setDeleteDialogOpen(false);
  };

  const handleCloseExportPrivateKeyDialog = () => {
     setExportPrivateKeyDialogOpen(false);
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
          Address: {squeakProfile.getAddress()}
        </p>
        {ProfileSettingsForm()}
        {ViewSqueaksButton()}
        {DeleteProfileButton()}
        {squeakProfile.getHasPrivateKey() &&
          ExportPrivateKeyButton()
        }
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

  function ExportPrivateKeyButton() {
    return (
      <>
      <Grid item xs={12}>
        <div className={classes.root}>
          <Button
            variant="contained"
            onClick={() => {
              handleClickOpenExportPrivateKeyDialog();
            }}>Export Private Key
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
              navigateTo(history, SQUEAK_ADDRESS_VIEW, [squeakProfile.getAddress()]);
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
      {ExportPrivateKeyDialogContent()}
    </>
  );
}
