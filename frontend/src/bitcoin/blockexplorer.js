export function getBlockDetailUrl(blockHash, network) {
  switch (network) {
    case 'mainnet':
      return `https://blockstream.info/block/${blockHash}`;
    case 'testnet':
      return `https://blockstream.info/testnet/block/${blockHash}`;
    default:
      return '';
  }
}
