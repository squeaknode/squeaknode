import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  Button,
} from '@material-ui/core';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import {CopyToClipboard} from 'react-copy-to-clipboard';

import {
  getExternalAddressRequest,
} from '../../squeakclient/requests';

export default function ShowExternalAddressDialog({
  open,
  handleClose,
  ...props
}) {

  const [externalAddress, setExternalAddress] = useState(null);

  const getExternalAddress = () => {
    getExternalAddressRequest(setExternalAddress);
  };

  function load(event) {
    getExternalAddress();
  }

  function cancel(event) {
    event.stopPropagation();
    handleClose();
  }

  function ignore(event) {
    event.stopPropagation();
  }

  function DisplayExternalAddress() {
    const address = externalAddress && `${externalAddress.getHost()}:${externalAddress.getPort()}`;
    return (
      <CopyToClipboard
        text={address}
        >
        <Button variant="outlined">
          {address}
          <ContentCopyIcon/>
        </Button>
      </CopyToClipboard>
    );
  }

  return (
    <Dialog open={open} onRendered={load} onClose={cancel} onClick={ignore} aria-labelledby="form-dialog-title" maxWidth="lg">
      <DialogTitle id="form-dialog-title">Show External Address</DialogTitle>
      <DialogContent>
        {DisplayExternalAddress()}
      </DialogContent>
    </Dialog>
  );
}
