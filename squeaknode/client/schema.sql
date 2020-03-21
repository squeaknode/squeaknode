-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS post;

CREATE TABLE squeak (
  hash TEXT PRIMARY KEY,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  nVersion INTEGER NOT NULL,
  hashEncContent TEXT NOT NULL,
  hashReplySqk TEXT NOT NULL,
  hashBlock TEXT NOT NULL,
  nBlockHeight INTEGER NOT NULL,
  scriptPubKey BLOB NOT NULL,
  hashDataKey TEXT NOT NULL,
  vchIv TEXT NOT NULL,
  nTime INTEGER NOT NULL,
  nNonce INTEGER NOT NULL,
  encContent BLOB NOT NULL,
  scriptSig BLOB NOT NULL,
  vchDataKey TEXT,
  content BLOB
);
