CREATE DATABASE squeakserver;

CREATE TABLE squeak (
  hash CHAR(32) PRIMARY KEY,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  nVersion INTEGER NOT NULL,
  hashEncContent CHAR(32) NOT NULL,
  hashReplySqk CHAR(32) NOT NULL,
  hashBlock CHAR(32) NOT NULL,
  nBlockHeight INTEGER NOT NULL,
  scriptPubKey VARCHAR(32) NOT NULL,
  hashDataKey CHAR(32) NOT NULL,
  vchIv CHAR(16) NOT NULL,
  nTime INTEGER NOT NULL,
  nNonce INTEGER NOT NULL,
  encContent VARCHAR(32) NOT NULL,
  scriptSig VARCHAR(32) NOT NULL,
  address VARCHAR(32) NOT NULL,
  vchDataKey CHAR(32),
  content VARCHAR(32)
);
