export const reloadRoute = (history) => {
  history.go(0);
};

export const goToPeerPage = (history, peerHash) => {
  history.push("/app/peer/" + peerHash);
};

export const goToLightningNodePage = (history, pubkey, host, port) => {
    console.log("Go to lightning node for pubkey: " + pubkey);
    if (pubkey && host && port) {
      history.push("/app/lightningnode/" + pubkey + "/" + host + "/" + port);
    } else if (pubkey && host) {
      history.push("/app/lightningnode/" + pubkey + "/" + host);
    } else {
      history.push("/app/lightningnode/" + pubkey);
    }
};

export const goToSqueakPage = (history, squeakHash) => {
  history.push("/app/squeak/" + squeakHash);
};

export const goToSqueakAddressPage = (history, squeakAddress) => {
  history.push("/app/squeakaddress/" + squeakAddress);
};

export const goToChannelPage = (history, txId, outputIndex) => {
   history.push("/app/channel/" + txId + "/" + outputIndex);
};

export const goToProfilePage = (history, squeakAddress) => {
  history.push("/app/profile/" + squeakAddress);
};

export const goToWalletPage = (history) => {
  history.push("/app/wallet/");
};

export const goToSentPaymentsPage = (history) => {
  history.push("/app/sentpayments/");
};

export const goToReceivedPaymentsPage = (history) => {
  history.push("/app/receivedpayments/");
};
