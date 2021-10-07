0.1.160 - 2021-10-07
===================

### Features
- Add unit test for timeline query.
    - #1518
- Add OpenTimestamps github action.
    - #1524

0.1.159 - 2021-10-04
===================

### Features
- Improve handling of duplicate entries in database.
    - #1478
- Refactor core functions to separate modules
    - #1460, #1464, #1468, #1473

0.1.158 - 2021-10-01
===================

### Features
- Show full date and time of squeak in tooltip.
    - #1393 PR by @abhiShandy

0.1.157 - 2021-09-28
===================

### Fixes
- Upgrade SQLAlchemy to version 1.4.
    - #1438

0.1.156 - 2021-09-27
===================

### Fixes
- Fix display external address text with full width.
    - #1429 PR by @abhiShandy

0.1.155 - 2021-09-27
===================

### Features
- Make p2p protocol more efficient by only requesting
  incremental changes when interests are updated.
    - #1424 and #1423

0.1.154 - 2021-09-24
===================

### Features
- Include saved peer name in list of connected peers.
    - #1361 and #1362
- Add button in UI to convert connected peer to saved peer.
    - #1365
- Improve dialog for showing external address, and include copy to
  clipboard.
    - #1380 PR by @abhiShandy
- Show connection status next to each item in saved peers list.
    - #1399

### Fixes
- Fix bug in p2p connection where the connection does not shut down
  properly in some cases.
    - #1397
- Fail gracefully in peer connection when LND is not available.
    - #1389 and #1395

0.1.153 - 2021-09-19
===================

### Features
- Better p2p networking. Inactive peer connection is now detected with
  `ping` message and stopped.
    - #1342 and #1347
- Better peer connection UI. `ConnectPeer` RPC is now synchronous, and
  the connect peer dialog in the frontend now updates with the result
  of the RPC, or error message.
    - #1326, #1327 and #1332
- Full-text search on squeak content.
	- #1287 and #1293
- Change display unit from msats to sats in received payments and sent
  payments.
	- #1341
- Show waiting indicator for more pages and dialogs in frontend UI.
	- #1338, 1343, 1344

### Fixes
- Fix broken unit test caused by unpinned dependencies in requirements.txt
    - #1310
