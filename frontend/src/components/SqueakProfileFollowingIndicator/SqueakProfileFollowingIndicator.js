import React, { useState } from "react";
import {
  Paper,
  IconButton,
  Menu,
  MenuItem,
  Typography,
  Grid,
  Box,
  Link,
  Divider,
  Button,
} from "@material-ui/core";
import { MoreVert as MoreIcon } from "@material-ui/icons";
import {useHistory} from "react-router-dom";
import classnames from "classnames";

import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';

import CardHeader from '@material-ui/core/CardHeader';
import Avatar from '@material-ui/core/Avatar';

import MoreVertIcon from '@material-ui/icons/MoreVert';
import VpnKeyIcon from '@material-ui/icons/VpnKey';
import NotificationsActiveIcon from '@material-ui/icons/NotificationsActive';
import NotificationsNoneIcon from '@material-ui/icons/NotificationsNone';

// styles
import useStyles from "./styles";

import Widget from "../../components/Widget";
import DeleteProfileDialog from "../../components/DeleteProfileDialog";
import RenameProfileDialog from "../../components/RenameProfileDialog";
import ExportPrivateKeyDialog from "../../components/ExportPrivateKeyDialog";
import ConfigureProfileDialog from "../../components/ConfigureProfileDialog";
import UpdateProfileImageDialog from "../../components/UpdateProfileImageDialog";
import ClearProfileImageDialog from "../../components/ClearProfileImageDialog";

export default function SqueakProfileFollowingIndicator({
  squeakProfile,
  ...props
}) {
  var classes = useStyles();


      function FollowingIndicator() {
        return (
          <>
            <Typography variant="body2" color="textSecondary" component="p">
              <NotificationsActiveIcon /> Following
            </Typography>
          </>
        )
      }

      function NotFollowingIndicator() {
        return (
          <>
            <Typography variant="body2" color="textSecondary" component="p">
              <NotificationsNoneIcon /> Not Following
            </Typography>
          </>
        )
      }

    return (
      <>
      {(squeakProfile.getFollowing())
        ? FollowingIndicator()
        : NotFollowingIndicator()
      }
      </>
      );
}
