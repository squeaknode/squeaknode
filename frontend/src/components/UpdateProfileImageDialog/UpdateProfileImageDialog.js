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
import {
  reloadRoute,
} from "../../navigation/navigation"


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
  var [imageBase64, setImageBase64] = useState(null);

  const resetFields = () => {
    setImageBase64(null);
  };

  const handleResponse = (response) => {
    // TODO: reload profile only.
    reloadRoute(history);
  };

  const handleErr = (err) => {
    alert('Error creating signing profile: ' + err);
  };

  const updateProfileImage = (imageStr) => {
    setSqueakProfileImageRequest(
      squeakProfile.getAddress(),
      imageStr,
      handleResponse,
      handleErr,
    );
  };

  function handleSubmit(event) {
    event.preventDefault();
    if (imageBase64 == null) {
      alert("Invalid image data.")
      return;
    }
    const imageBase64Stripped = imageBase64.split(',')[1];
    updateProfileImage(imageBase64Stripped);
    handleClose();
  }

  const handleChangeSelectedImage = (event) => {
    // alert("selected image changed.");
    if (event.target.files.length < 1) {
      alert("Invalid file selected");
      setSelectedFile(null);
    }
    const file = event.target.files[0];
    setSelectedFile(file);
    getFileAsBase64(file);
  };

  const getFileAsBase64 = (file) => {
    if (file == null) {
      setImageBase64(null);
    }
    const reader = new FileReader();
    reader.addEventListener("load", function () {
      // convert image file to base64 string
      // preview.src = reader.result;
      setImageBase64(reader.result);
    }, false);
    if (file) {
      reader.readAsDataURL(file);
    }
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

  function DisplaySelectedImageFileName() {
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

  function DisplaySelectedImageFile() {
    const imageStr = imageBase64 ? imageBase64 : "";
    return (
<img src={imageStr} height="200" alt="Image preview..."/>
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
  </DialogContent>
  <DialogContent>
    {DisplaySelectedImageFile()}
  </DialogContent>
  <DialogContent>
    {DisplaySelectedImageFileName()}
  </DialogContent>
  <DialogActions>
    {CancelButton()}
    {SetProfileImageButton()}
  </DialogActions>
  </form>
    </Dialog>
  )
}
