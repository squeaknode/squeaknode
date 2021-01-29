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

import VpnKeyIcon from '@material-ui/icons/VpnKey';

// styles
import useStyles from "./styles";

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
import DeleteProfileDialog from "../../components/DeleteProfileDialog";
import ExportPrivateKeyDialog from "../../components/ExportPrivateKeyDialog";
import ConfigureProfileDialog from "../../components/ConfigureProfileDialog";

import {
  getSqueakProfileRequest,
  setSqueakProfileFollowingRequest,
  setSqueakProfileSharingRequest,
} from "../../squeakclient/requests"

import {
  getProfileImageSrcString,
} from "../../squeakimages/images"



export default function ProfilePage() {
  var classes = useStyles();
  const { id } = useParams();
  const [squeakProfile, setSqueakProfile] = useState(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [exportPrivateKeyDialogOpen, setExportPrivateKeyDialogOpen] = useState(false);
  const [configureDialogOpen, setConfigureDialogOpen] = useState(false);
  const history = useHistory();

  const getSqueakProfile = (id) => {
    getSqueakProfileRequest(id, setSqueakProfile);
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

  const handleClickOpenExportPrivateKeyDialog = () => {
    setExportPrivateKeyDialogOpen(true);
  };

  const handleClickOpenConfigureDialog = () => {
    setConfigureDialogOpen(true);
  };

  const handleCloseDeleteDialog = () => {
     setDeleteDialogOpen(false);
  };

  const handleCloseExportPrivateKeyDialog = () => {
     setExportPrivateKeyDialogOpen(false);
  };

  const handleCloseConfigureDialog = () => {
     setConfigureDialogOpen(false);
  };

  const handleReloadProfile = () => {
    getSqueakProfile(id);
  };

  function ProfileContent() {
    return (
      <>
        {SqueakProfileImageDisplay()}
        {squeakProfile.getHasPrivateKey() &&
          ExportPrivateKeyButton()
        }
        {DeleteProfileButton()}
      </>
    )
  }

  function SqueakProfileImageDisplay() {
    const profileImageBase64String = squeakProfile.getProfileImage();
    return (
        <Card className={classes.root}>
            <CardMedia
              className={classes.media}
              image={`${getProfileImageSrcString(squeakProfile)}`}
              title="Profile Image"
            />
            <CardContent>
              <Typography gutterBottom variant="h5" component="h2">
                {squeakProfile.getProfileName()} {squeakProfile.getHasPrivateKey() && <VpnKeyIcon />}
              </Typography>
              <Typography variant="body2" color="textSecondary" component="p">
                {squeakProfile.getAddress()}
              </Typography>
            </CardContent>
          <CardActions>
            <Button
              onClick={() => {
                goToSqueakAddressPage(squeakProfile.getAddress());
              }}
              size="small" color="primary">
              View Squeaks
            </Button>
            <Button
              onClick={() => {
                handleClickOpenConfigureDialog();
              }}
              size="small" color="primary">
              Configure
            </Button>
          </CardActions>
        </Card>
      );
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
              goToSqueakAddressPage(squeakProfile.getAddress());
            }}>View Squeaks
          </Button>
        </div>
      </Grid>
      </>
    )
  }

  function ConfigureProfileButton() {
    return (
      <>
      <Grid item xs={12}>
        <div className={classes.root}>
          <Button
            variant="contained"
            onClick={() => {
              handleClickOpenConfigureDialog();
            }}>Configure Profile
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

  return (
    <>
      <PageTitle title={'Squeak Profile: ' + (squeakProfile ? squeakProfile.getProfileName() : null)} />
      <div>
      {squeakProfile &&
        ProfileContent()}
      </div>
      {DeleteProfileDialogContent()}
      {ExportPrivateKeyDialogContent()}
      {ConfigureProfileDialogContent()}
    </>
  );
}
