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
import CreateContactProfileDialog from "../../components/CreateContactProfileDialog";

// data
import mock from "../dashboard/mock";

import {
  getSigningProfilesRequest,
  getContactProfilesRequest,
} from "../../squeakclient/requests"


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

  const goToSqueakAddressPage = (squeakAddress) => {
    history.push("/app/squeakaddress/" + squeakAddress);
  };

  const goToProfilePage = (profileId) => {
    history.push("/app/profile/" + profileId);
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
        {SigningProfiles()}
      </TabPanel>
      <TabPanel value={value} index={1}>
        {ContactProfiles()}
      </TabPanel>
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

  function SigningProfiles() {
    return (
      <>
      <Grid container spacing={4}>
        {CreateSigningProfileButton()}
       <Grid item xs={12}>
         <MUIDataTable
           title="Signing Profiles"
           data={signingProfiles.map(p =>
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
               goToProfilePage(id);
             }
           }}/>
       </Grid>
     </Grid>
      </>
    )
  }

  function ContactProfiles() {
    return (
      <>
      <Grid container spacing={4}>
      {CreateContactProfileButton()}
       <Grid item xs={12}>
         <MUIDataTable
           title="Contact Profiles"
           data={contactProfiles.map(p =>
              [
                p.getProfileName(),
                p.getAddress(),
                p.getFollowing().toString(),
                p.getSharing().toString(),
              ]
            )}
           columns={["Name", "Address", "Following", "Sharing"]}
           options={{
             filter: false,
             print: false,
             viewColumns: false,
             selectableRows: "none",
             onRowClick: rowData => {
               var address = rowData[1];
               goToSqueakAddressPage(address);
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
          ></CreateSigningProfileDialog>
      </>
    )
  }

  function CreateContactProfileDialogContent() {
    return (
      <>
        <CreateContactProfileDialog
          open={createContactProfileDialogOpen}
          handleClose={handleCloseCreateContactProfileDialog}
          ></CreateContactProfileDialog>
      </>
    )
  }

  return (
    <>
     < PageTitle title = "Profiles" />
    {ProfilesTabs()}
    {CreateSigningProfileDialogContent()}
    {CreateContactProfileDialogContent()}
   < />);
}
