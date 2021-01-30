import React, {useState, useEffect} from 'react';
import {
  Paper,
  IconButton,
  Menu,
  MenuItem,
  Typography,
  Grid,
  Box,
  Link,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  TextField,
  DialogActions,
  Button,
  FormControl,
  InputLabel,
  Select,
} from "@material-ui/core";
import { MoreVert as MoreIcon } from "@material-ui/icons";
import {useHistory} from "react-router-dom";
import classnames from "classnames";

// styles
import useStyles from "./styles";

import Widget from "../../components/Widget";
import SqueakThreadItem from "../../components/SqueakThreadItem";

import {
  setSqueakProfileImageRequest,
} from "../../squeakclient/requests"


export default function UpdateProfileImageDialog({
  open,
  handleClose,
  squeakProfile,
  reloadProfile,
  ...props
}) {
  var classes = useStyles();
  const history = useHistory();

  var [selectedFile, setSelectedFile] = useState(null);
  var [imageBytes, setImageBytes] = useState([]);

  const resetFields = () => {
    setImageBytes([]);
  };

  const reloadRoute = () => {
    history.go(0);
  };

  const handleResponse = (response) => {
    // TODO: reload profile only.
    reloadRoute();
  };

  const handleErr = (err) => {
    alert('Error creating signing profile: ' + err);
  };

  const updateProfileImage = (imageBytes) => {
    setSqueakProfileImageRequest(
      squeakProfile.getProfileId(),
      imageBytes,
      handleResponse,
      handleErr,
    );
  };

  function handleSubmit(event) {
    event.preventDefault();
    // openChannel(pubkey, amount, satperbyte);

    // const imageBytes = selectedFile.

    handleClose();
  }

  const handleChangeSelectedImage = (event) => {
    // alert("selected image changed.");
    if (event.target.files.length < 1) {
      alert("Invalid file selected");
      setSelectedFile(null);
    }
    setSelectedFile(event.target.files[0]);
  };

  function FileInput() {
    return (
<>
<Button
  variant="contained"
  component="label"
>
  Select File
  <input
    type="file"
    hidden
    onChange={handleChangeSelectedImage}
  />
</Button>
</>
    )
  }

  function DisplaySelectedImageFile() {
    const fileName = selectedFile ? selectedFile.name : "";
    return (
      <TextField
        id="standard-textarea"
        label="selected-file"
        required
        autoFocus
        value={fileName}
        fullWidth
        inputProps={{
           readOnly: true,
        }}
      />
    )
  }

  function CancelButton() {
    return (
      <Button
        onClick={handleClose}
        variant="contained"
        color="secondary"
      >
        Cancel
      </Button>
    )
  }

  function SetProfileImageButton() {
    return (
      <Button
       type="submit"
       variant="contained"
       color="primary"
       className={classes.button}
       >
       Set Profile Image
       </Button>
    )
  }

  return (
    <Dialog open={open} onEnter={resetFields} onClose={handleClose} aria-labelledby="form-dialog-title">
  <DialogTitle id="form-dialog-title">Set Profile Image</DialogTitle>
  <form className={classes.root} onSubmit={handleSubmit} noValidate autoComplete="off">
  <DialogContent>
    {FileInput()}
    {DisplaySelectedImageFile()}
  </DialogContent>
  <DialogActions>
    {CancelButton()}
    {SetProfileImageButton()}
  </DialogActions>
  </form>
    </Dialog>
  )
}
