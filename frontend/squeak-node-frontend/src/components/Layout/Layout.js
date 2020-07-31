import React from "react";
import {
  Route,
  Switch,
  Redirect,
  withRouter,
} from "react-router-dom";
import classnames from "classnames";

// styles
import useStyles from "./styles";

// components
import Header from "../Header";
import Sidebar from "../Sidebar";

// pages
import Timeline from "../../pages/timeline";
import Dashboard from "../../pages/dashboard";
import SqueakAddress from "../../pages/squeakaddress";
import Squeak from "../../pages/squeak";
import Profile from "../../pages/profile";
import Lightning from "../../pages/lightning";
import Notifications from "../../pages/notifications";
import Maps from "../../pages/maps";
import Profiles from "../../pages/profiles";
import Icons from "../../pages/icons";
import Charts from "../../pages/charts";

// context
import { useLayoutState } from "../../context/LayoutContext";

function Layout(props) {
  var classes = useStyles();

  // global
  var layoutState = useLayoutState();

  return (
    <div className={classes.root}>
        <>
          <Header history={props.history} />
          <Sidebar />
          <div
            className={classnames(classes.content, {
              [classes.contentShift]: layoutState.isSidebarOpened,
            })}
          >
            <div className={classes.fakeToolbar} />
            <Switch>
              <Route path="/app/timeline" component={Timeline} />
              <Route path="/app/dashboard" component={Dashboard} />
              <Route path="/app/squeakaddress/:address" component={SqueakAddress} />
              <Route path="/app/squeak/:hash" component={Squeak} />
              <Route path="/app/profile/:id" component={Profile} />
              <Route path="/app/profiles" component={Profiles} />
              <Route path="/app/lightning" component={Lightning} />
              <Route path="/app/notifications" component={Notifications} />
              <Route
                exact
                path="/app/ui"
                render={() => <Redirect to="/app/ui/icons" />}
              />
              <Route path="/app/ui/maps" component={Maps} />
              <Route path="/app/ui/icons" component={Icons} />
              <Route path="/app/ui/charts" component={Charts} />
            </Switch>
          </div>
        </>
    </div>
  );
}

export default withRouter(Layout);
