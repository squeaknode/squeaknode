
export const goToPeerPage = (history, peerId) => {
  history.push("/app/peer/" + peerId);
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
