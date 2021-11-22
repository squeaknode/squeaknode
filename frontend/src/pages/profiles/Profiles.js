import React, { useState, useEffect, useCallback } from 'react';
import {
  Grid,
  Button,
  Tabs,
  Tab,
  AppBar,
  Box,
  CircularProgress,
} from '@material-ui/core';

// styles

// styles
import useStyles from './styles';

// components
import Widget from '../../components/Widget';
import CreateSigningProfileDialog from '../../components/CreateSigningProfileDialog';
import ImportSigningProfileDialog from '../../components/ImportSigningProfileDialog';
import CreateContactProfileDialog from '../../components/CreateContactProfileDialog';
import ProfileListItem from '../../components/ProfileListItem';

// data

import {
  getProfilesRequest,
} from '../../squeakclient/requests';

export default function Profiles() {
  const classes = useStyles();
  const [profiles, setProfiles] = useState([]);
  const [createSigningProfileDialogOpen, setCreateSigningProfileDialogOpen] = useState(false);
  const [importSigningProfileDialogOpen, setImportSigningProfileDialogOpen] = useState(false);
  const [createContactProfileDialogOpen, setCreateContactProfileDialogOpen] = useState(false);
  const [value, setValue] = useState(0);
  const [waitingForProfiles, setWaitingForProfiles] = useState(false);

  function a11yProps(index) {
    return {
      id: `simple-tab-${index}`,
      'aria-controls': `simple-tabpanel-${index}`,
    };
  }

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  const loadProfiles = useCallback(() => {
    setWaitingForProfiles(true);
    getProfilesRequest(handleLoadedProfiles);
  },
  []);

  const handleClickOpenCreateSigningProfileDialog = () => {
    setCreateSigningProfileDialogOpen(true);
  };

  const handleCloseCreateSigningProfileDialog = () => {
    setCreateSigningProfileDialogOpen(false);
  };

  const handleClickOpenCreateContactProfileDialog = () => {
    setCreateContactProfileDialogOpen(true);
  };

  const handleCloseCreateContactProfileDialog = () => {
    setCreateContactProfileDialogOpen(false);
  };

  const handleClickOpenImportSigningProfileDialog = () => {
    setImportSigningProfileDialogOpen(true);
  };

  const handleCloseImportSigningProfileDialog = () => {
    setImportSigningProfileDialogOpen(false);
  };

  const handleLoadedProfiles = (loadedProfiles) => {
    setWaitingForProfiles(false);
    setProfiles(loadedProfiles);
  };

  useEffect(() => {
    loadProfiles();
  }, [loadProfiles]);

  function TabPanel(props) {
    const {
      children, value, index, ...other
    } = props;

    return (
      <div
        role="tabpanel"
        hidden={value !== index}
        id={`simple-tabpanel-${index}`}
        aria-labelledby={`simple-tab-${index}`}
        {...other}
      >
        {value === index && (
          <div>{children}</div>
        )}
      </div>
    );
  }

  function ProfilesTabs() {
    return (
      <>
        <AppBar position="static" color="default">
          <Tabs value={value} onChange={handleChange} aria-label="simple tabs example">
            <Tab label="Profiles" {...a11yProps(0)} />
          </Tabs>
        </AppBar>
        <TabPanel value={value} index={0}>
          {ProfilesContent()}
        </TabPanel>
      </>
    );
  }

  function ProfilesContent() {
    return (
      <>
        <Grid container spacing={4}>
          <Grid item xs={12}>
            <Widget disableWidgetMenu>
              {CreateSigningProfileButton()}
              {ImportSigningProfileButton()}
              {CreateContactProfileButton()}
              {ProfilesGridItem(profiles)}
            </Widget>
          </Grid>
        </Grid>
      </>
    );
  }

  function ProfilesGridItem(profiles) {
    return (
      <Grid item xs={12}>
        {profiles.map((profile) => (
          <Box
            p={1}
            key={profile.getProfileName()}
          >
            <ProfileListItem
              key={profile.getProfileName()}
              handlePeerClick={() => console.log('clicked profile')}
              profile={profile}
            />
          </Box>
        ))}
      </Grid>
    );
  }

  function CreateSigningProfileButton() {
    return (
      <>
        <Grid item xs={12}>
          <div className={classes.root}>
            <Button
              variant="contained"
              onClick={() => {
                handleClickOpenCreateSigningProfileDialog();
              }}
            >
              Create Signing Profile
            </Button>
          </div>
        </Grid>
      </>
    );
  }

  function ImportSigningProfileButton() {
    return (
      <>
        <Grid item xs={12}>
          <div className={classes.root}>
            <Button
              variant="contained"
              onClick={() => {
                handleClickOpenImportSigningProfileDialog();
              }}
            >
              Import Signing Profile
            </Button>
          </div>
        </Grid>
      </>
    );
  }

  function CreateContactProfileButton() {
    return (
      <>
        <Grid item xs={12}>
          <div className={classes.root}>
            <Button
              variant="contained"
              onClick={() => {
                handleClickOpenCreateContactProfileDialog();
              }}
            >
              Add contact
            </Button>
          </div>
        </Grid>
      </>
    );
  }

  function CreateSigningProfileDialogContent() {
    return (
      <>
        <CreateSigningProfileDialog
          open={createSigningProfileDialogOpen}
          handleClose={handleCloseCreateSigningProfileDialog}
        />
      </>
    );
  }

  function ImportSigningProfileDialogContent() {
    return (
      <>
        <ImportSigningProfileDialog
          open={importSigningProfileDialogOpen}
          handleClose={handleCloseImportSigningProfileDialog}
        />
      </>
    );
  }

  function CreateContactProfileDialogContent() {
    return (
      <>
        <CreateContactProfileDialog
          open={createContactProfileDialogOpen}
          handleClose={handleCloseCreateContactProfileDialog}
        />
      </>
    );
  }

  function GridContent() {
    return (
      <Grid container spacing={0}>
        <Grid item xs={12} sm={9}>
          {ProfilesTabs()}
        </Grid>
        <Grid item xs={12} sm={3} />
      </Grid>
    );
  }

  function WaitingIndicator() {
    return (
      <CircularProgress size={48} className={classes.buttonProgress} />
    );
  }

  return (
    <>
      {!waitingForProfiles
        ? GridContent()
        : WaitingIndicator()}
      {CreateSigningProfileDialogContent()}
      {ImportSigningProfileDialogContent()}
      {CreateContactProfileDialogContent()}
    < />
  );
}
