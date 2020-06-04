CREATE DATABASE squeakserver;

CREATE TABLE squeak (
  hash CHAR(32) PRIMARY KEY,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  nVersion INTEGER NOT NULL,
  hashEncContent CHAR(32) NOT NULL,
  hashReplySqk CHAR(32) NOT NULL,
  hashBlock CHAR(32) NOT NULL,
  nBlockHeight INTEGER NOT NULL,
  scriptPubKey VARCHAR(50) NOT NULL,
  hashDataKey CHAR(32) NOT NULL,
  vchIv CHAR(16) NOT NULL,
  nTime INTEGER NOT NULL,
  nNonce INTEGER NOT NULL,
  encContent CHAR(1136) NOT NULL,
  scriptSig VARCHAR(200) NOT NULL,
  address VARCHAR(50) NOT NULL,
  vchDataKey CHAR(32),
  content CHAR(1120)
);
