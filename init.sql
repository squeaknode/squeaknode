CREATE TABLE IF NOT EXISTS squeak (
  hash CHAR(64) PRIMARY KEY,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  nVersion INTEGER NOT NULL,
  hashEncContent CHAR(64) NOT NULL,
  hashReplySqk CHAR(64) NOT NULL,
  hashBlock CHAR(64) NOT NULL,
  nBlockHeight INTEGER NOT NULL,
  vchScriptPubKey bytea NOT NULL,
  vchEncryptionKey bytea NOT NULL,
  encDatakey CHAR(256) NOT NULL,
  iv CHAR(32) NOT NULL,
  nTime INTEGER NOT NULL,
  nNonce BIGINT NOT NULL,
  encContent CHAR(2272) NOT NULL, -- Encrypted content length is always 1136 bytes (2272 hex characters).
  vchScriptSig bytea NOT NULL,
  address VARCHAR(35) NOT NULL, -- Maximum length of a bitcoin address is 35.
  vchDecryptionKey bytea NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_squeak_address
  ON squeak(address);

CREATE TABLE IF NOT EXISTS profile (
  profile_id SERIAL PRIMARY KEY,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  profile_name VARCHAR(64) NOT NULL,
  private_key bytea,
  address VARCHAR(35) UNIQUE NOT NULL, -- Maximum length of a bitcoin address is 35.
  sharing BOOLEAN NOT NULL,
  following BOOLEAN NOT NULL
);
