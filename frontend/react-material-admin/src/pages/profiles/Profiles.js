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

// data
import mock from "../dashboard/mock";

import {GetInfoRequest} from "../../proto/lnd_pb"
import {
  HelloRequest,
  GetFollowedSqueakDisplaysRequest,
  GetSigningProfilesRequest,
  GetContactProfilesRequest,
} from "../../proto/squeak_admin_pb"
import {SqueakAdminClient} from "../../proto/squeak_admin_grpc_web_pb"

var client = new SqueakAdminClient('http://' + window.location.hostname + ':8080')

const datatableData = [
  [
    "Joe James", "Example Inc.", "Yonkers", "NY"
  ],
  [
    "John Walsh", "Example Inc.", "Hartford", "CT"
  ],
  [
    "Bob Herm", "Example Inc.", "Tampa", "FL"
  ],
  [
    "James Houston", "Example Inc.", "Dallas", "TX"
  ],
  [
    "Prabhakar Linwood", "Example Inc.", "Hartford", "CT"
  ],
  [
    "Kaui Ignace", "Example Inc.", "Yonkers", "NY"
  ],
  [
    "Esperanza Susanne", "Example Inc.", "Hartford", "CT"
  ],
  [
    "Christian Birgitte", "Example Inc.", "Tampa", "FL"
  ],
  [
    "Meral Elias", "Example Inc.", "Hartford", "CT"
  ],
  [
    "Deep Pau", "Example Inc.", "Yonkers", "NY"
  ],
  [
    "Sebastiana Hani", "Example Inc.", "Dallas", "TX"
  ],
  [
    "Marciano Oihana", "Example Inc.", "Yonkers", "NY"
  ],
  [
    "Brigid Ankur", "Example Inc.", "Dallas", "TX"
  ],
  [
    "Anna Siranush", "Example Inc.", "Yonkers", "NY"
  ],
  [
    "Avram Sylva", "Example Inc.", "Hartford", "CT"
  ],
  [
    "Serafima Babatunde", "Example Inc.", "Tampa", "FL"
  ],
  [
    "Gaston Festus", "Example Inc.", "Tampa", "FL"
  ]
];

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

  const getLndInfo = () => {
    console.log("called getLndInfo");

    var getInfoRequest = new GetInfoRequest()

    client.lndGetInfo(getInfoRequest, {}, (err, response) => {
      if (err) {
        console.log(err.message);
        return;
      }
      console.log(response);
    });
  };
  const getSigningProfiles = () => {
    console.log("called getSigningProfiles");

    var getSigningProfilesRequest = new GetSigningProfilesRequest()

    client.getSigningProfiles(getSigningProfilesRequest, {}, (err, response) => {
      if (err) {
        console.log(err.message);
        return;
      }
      console.log(response);
      setSigningProfiles(response.getSqueakProfilesList());
    });
  };
  const getContactProfiles = () => {
    console.log("called getContactProfiles");

    var getContactProfilesRequest = new GetContactProfilesRequest()

    client.getSigningProfiles(getContactProfilesRequest, {}, (err, response) => {
      if (err) {
        console.log(err.message);
        return;
      }
      console.log(response);
      setContactProfiles(response.getSqueakProfilesList());
    });
  };

  const goToCreateSigningProfilePage = () => {
    history.push("/app/createsigningprofile");
  };

  const goToCreateContactProfilePage = () => {
    history.push("/app/createcontactprofile");
  };

  const goToSqueakAddressPage = (squeakAddress) => {
    history.push("/app/squeakaddress/" + squeakAddress);
  };

  useEffect(() => {
    getLndInfo()
  }, []);
  useEffect(() => {
    getSigningProfiles()
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
          <Box p={3}>
            <Typography>{children}</Typography>
          </Box>
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
              goToCreateSigningProfilePage();
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
              goToCreateContactProfilePage();
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

  return (
    <>
     < PageTitle title = "Profiles" />
    {ProfilesTabs()}
   < />);
}
