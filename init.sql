CREATE TABLE IF NOT EXISTS squeak (
  hash CHAR(64) PRIMARY KEY,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  n_version INTEGER NOT NULL,
  hash_enc_content CHAR(64) NOT NULL,
  hash_reply_sqk CHAR(64) NOT NULL,
  hash_block CHAR(64) NOT NULL,
  n_block_height INTEGER NOT NULL,
  vch_script_pub_key bytea NOT NULL,
  vch_encryption_key bytea NOT NULL,
  enc_data_key CHAR(256) NOT NULL,
  iv CHAR(32) NOT NULL,
  n_time INTEGER NOT NULL,
  n_nonce BIGINT NOT NULL,
  enc_content CHAR(2272) NOT NULL, -- Encrypted content length is always 1136 bytes (2272 hex characters).
  vch_script_sig bytea NOT NULL,
  author_address VARCHAR(35) NOT NULL, -- Maximum length of a bitcoin address is 35.
  vch_decryption_key bytea,
  block_header bytea
);

CREATE INDEX IF NOT EXISTS idx_squeak_address
  ON squeak(author_address);

CREATE TABLE IF NOT EXISTS profile (
  profile_id SERIAL PRIMARY KEY,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  profile_name VARCHAR(64) NOT NULL,
  private_key bytea,
  address VARCHAR(35) UNIQUE NOT NULL, -- Maximum length of a bitcoin address is 35.
  sharing BOOLEAN NOT NULL,
  following BOOLEAN NOT NULL,
  whitelisted BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS peer (
  peer_id SERIAL PRIMARY KEY,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  peer_name VARCHAR(64),
  server_host VARCHAR(256) NOT NULL,
  server_port INTEGER NOT NULL,
  publishing BOOLEAN NOT NULL,
  subscribed BOOLEAN NOT NULL
);
