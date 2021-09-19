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
