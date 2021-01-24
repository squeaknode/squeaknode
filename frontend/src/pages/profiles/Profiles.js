import React, {useState, useEffect} from 'react';
import {useHistory} from "react-router-dom";
import {
    Grid,
    Button,
    Paper,
    Tabs,
    Tab,
    AppBar,
    Box,
    Typography,
  } from "@material-ui/core";
import MUIDataTable from "mui-datatables";

// styles
import {makeStyles} from '@material-ui/core/styles';

// components
import PageTitle from "../../components/PageTitle";
import Widget from "../../components/Widget";
import Table from "../dashboard/components/Table/Table";
import CreateSigningProfileDialog from "../../components/CreateSigningProfileDialog";
import ImportSigningProfileDialog from "../../components/ImportSigningProfileDialog";
import CreateContactProfileDialog from "../../components/CreateContactProfileDialog";

// data
import mock from "../dashboard/mock";

import {
  getSigningProfilesRequest,
  getContactProfilesRequest,
} from "../../squeakclient/requests"
import {navigateTo, PROFILE_VIEW} from "../../navigation/routes";


const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1)
    }
  }
}));

export default function Profiles() {
  const classes = useStyles();
  const [signingProfiles, setSigningProfiles] = useState([]);
  const [contactProfiles, setContactProfiles] = useState([]);
  const [createSigningProfileDialogOpen, setCreateSigningProfileDialogOpen] = useState(false);
  const [importSigningProfileDialogOpen, setImportSigningProfileDialogOpen] = useState(false);
  const [createContactProfileDialogOpen, setCreateContactProfileDialogOpen] = useState(false);
  const [value, setValue] = useState(0);
  const history = useHistory();

  function a11yProps(index) {
    return {
      id: `simple-tab-${index}`,
      'aria-controls': `simple-tabpanel-${index}`,
    };
  }

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  const loadSigningProfiles = () => {
    getSigningProfilesRequest(setSigningProfiles);
  };
  const loadContactProfiles = () => {
    getContactProfilesRequest(setContactProfiles);
  };

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

  useEffect(() => {
    loadSigningProfiles()
  }, []);
  useEffect(() => {
    loadContactProfiles()
  }, []);

  function TabPanel(props) {
    const { children, value, index, ...other } = props;

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
          <Tab label="Signing Profiles" {...a11yProps(0)} />
          <Tab label="Contact Profiles" {...a11yProps(1)} />
        </Tabs>
      </AppBar>
      <TabPanel value={value} index={0}>
        {SigningProfilesContent()}
      </TabPanel>
      <TabPanel value={value} index={1}>
        {ContactProfilesContent()}
      </TabPanel>
      </>
    )
  }

  function SigningProfilesContent() {
    return (
      <>
      <Grid container spacing={4}>
        <Grid item xs={12}>
          <Widget disableWidgetMenu>
            {CreateSigningProfileButton()}
            {ImportSigningProfileButton()}
            {ShowProfiles("Signing profiles", signingProfiles)}
          </Widget>
        </Grid>
      </Grid>
      </>
    )
  }

  function ContactProfilesContent() {
    return (
      <>
      <Grid container spacing={4}>
        <Grid item xs={12}>
          <Widget disableWidgetMenu>
            {CreateContactProfileButton()}
            {ShowProfiles("Contact profiles", contactProfiles)}
          </Widget>
        </Grid>
      </Grid>
      </>
    )
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
            }}>Create Signing Profile
          </Button>
        </div>
      </Grid>
      </>
    )
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
            }}>Import Signing Profile
          </Button>
        </div>
      </Grid>
      </>
    )
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
            }}>Add contact
          </Button>
        </div>
      </Grid>
      </>
    )
  }

  function ShowProfiles(title, profiles) {
    return (
      <>
      <Grid container spacing={4}>
       <Grid item xs={12}>
         <MUIDataTable
           title={title}
           data={profiles.map(p =>
              [
                p.getProfileId(),
                p.getProfileName(),
                p.getAddress(),
                p.getFollowing().toString(),
                p.getSharing().toString(),
              ]
            )}
           columns={[
             {
               name: "Id",
               options: {
                 display: false,
               }
             },
             "Name", "Address", "Following", "Sharing"
           ]}
           options={{
             filter: false,
             print: false,
             viewColumns: false,
             selectableRows: "none",
             onRowClick: rowData => {
               var id = rowData[0];
               var address = rowData[2];
               //goToSqueakAddressPage(address);
               navigateTo(history, PROFILE_VIEW, [id]);
             }
           }}/>
       </Grid>
     </Grid>
      </>
    )
  }

  function CreateSigningProfileDialogContent() {
    return (
      <>
        <CreateSigningProfileDialog
          open={createSigningProfileDialogOpen}
          handleClose={handleCloseCreateSigningProfileDialog}
        />
      </>
    )
  }

  function ImportSigningProfileDialogContent() {
    return (
      <>
        <ImportSigningProfileDialog
          open={importSigningProfileDialogOpen}
          handleClose={handleCloseImportSigningProfileDialog}
        />
      </>
    )
  }

  function CreateContactProfileDialogContent() {
    return (
      <>
        <CreateContactProfileDialog
          open={createContactProfileDialogOpen}
          handleClose={handleCloseCreateContactProfileDialog}
         />
      </>
    )
  }

  return (
    <>
      < PageTitle title = "Profiles" />
      {ProfilesTabs()}
      {CreateSigningProfileDialogContent()}
      {ImportSigningProfileDialogContent()}
      {CreateContactProfileDialogContent()}
    </>
  )
}