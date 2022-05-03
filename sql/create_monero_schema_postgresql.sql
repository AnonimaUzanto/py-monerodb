CREATE TABLE "alt_blocks" (
  "block_hash" char[32] PRIMARY KEY,
  "alt_block_height" int,
  "cumulative_weight" int,
  "cumulative_difficulty_low" int,
  "cumulative_difficulty_hight" int,
  "already_generated_coins" int,
  "major_version" int,
  "minor_version" int,
  "timestamp" timestamp,
  "prev_id" char[32],
  "nonce" int,
  "miner_tx_ver" int,
  "unlock_time" int,
  "height" int,
  "vout_n_amount" int,
  "vout_n_key" char[32],
  "miner_tx_extra" varbinary,
  "rct_signatures_type" int,
  "tx_hashes" char[32]
);

CREATE TABLE "block_heights" (
  "zerokval" int,
  "block_hash" char[32] PRIMARY KEY,
  "block_height" int
);

CREATE TABLE "block_info" (
  "zerokval" int,
  "block_height" int PRIMARY KEY,
  "bi_timestamp" timestamp,
  "bi_coins" int,
  "bi_weight" int,
  "bi_diff_lo" int,
  "bi_diff_hi" int,
  "bi_hash" char[32],
  "bi_cum_rct" int,
  "bi_long_term_block_weight" int
);

CREATE TABLE "blocks" (
  "block_id" int PRIMARY KEY,
  "major_version" int,
  "minor_version" int,
  "timestamp" timestamp,
  "prev_id" char[32],
  "nonce" int,
  "miner_tx_ver" int,
  "unlock_time" int,
  "height" int,
  "vout_n_amount" int,
  "vout_n_key" char[32],
  "miner_tx_extra" varbinary,
  "rct_signatures_type" int,
  "tx_hashes" char[32]
);

CREATE TABLE "hf_versions" (
  "block_id" int PRIMARY KEY,
  "hf_version" int
);

CREATE TABLE "output_amounts" (
  "amount" int PRIMARY KEY,
  "amount_index" int,
  "output_id" int,
  "pubkey" char[32],
  "unlock_time" int,
  "height" int
);

CREATE TABLE "output_txs" (
  "zerokval" int,
  "output_id" int PRIMARY KEY,
  "txn_hash" char[32],
  "local_index" int
);

CREATE TABLE "spent_keys" (
  "zerokval" int,
  "spent_key" char[32] PRIMARY KEY
);

CREATE TABLE "tx_indices" (
  "zerokval" int,
  "txn_hash" char[32] PRIMARY KEY,
  "txn_id" int,
  "unlock_time" int,
  "block_id" int
);

CREATE TABLE "tx_outputs" (
  "txn_id" int PRIMARY KEY,
  "txn_indices" int
);

CREATE TABLE "txpool_blob" (
  "txn_hash" char[32] PRIMARY KEY,
  "txn_id" int,
  "version" int,
  "unlock_time" int,
  "vin_n_amount" int,
  "vin_n_key_offsets" int,
  "vin_n_k_image" char[32],
  "vout_n_amount" int,
  "vout_n_key" char[32],
  "tx_extra" varbinary,
  "rct_type" int,
  "txn_fee" int,
  "ecdhinfo" char[8],
  "outpk" char[32],
  "nbp" int,
  "A" char[32],
  "S" char[32],
  "T1" char[32],
  "T2" char[32],
  "taux" char[32],
  "mu" char[32],
  "L_n" char[32],
  "R_n" char[32],
  "a" char[32],
  "b" char[32],
  "t" char[32],
  "s_1_to_11" char[32],
  "c1" char[32],
  "D" char[32],
  "pseudoOuts" char[32]
);

CREATE TABLE "txpool_meta" (
  "txn_hash" char[32] PRIMARY KEY,
  "max_used_block_id" char[32],
  "last_failed_id" char[32],
  "weight" int,
  "fee" int,
  "max_used_block_height" int,
  "last_failed_height" int,
  "receive_time" int,
  "last_relayed_time" int,
  "kept_by_block" boolean,
  "relayed" boolean,
  "do_not_relay" boolean,
  "double_spend_seen" boolean,
  "pruned" boolean,
  "is_local" boolean,
  "dandelionpp_stem" boolean,
  "is_forwarding" boolean,
  "bf_padding" int,
  "padding" int
);

CREATE TABLE "txs_prunable" (
  "txn_id" int PRIMARY KEY,
  "nbp" int,
  "A" char[32],
  "S" char[32],
  "T1" char[32],
  "T2" char[32],
  "taux" char[32],
  "mu" char[32],
  "L_n" char[32],
  "R_n" char[32],
  "a" char[32],
  "b" char[32],
  "t" char[32],
  "s_1_to_11" char[32],
  "c1" char[32],
  "D" char[32],
  "pseudoOuts" char[32]
);

CREATE TABLE "txs_prunable_hash" (
  "txn_id" int PRIMARY KEY,
  "txn_hash" char[32]
);

CREATE TABLE "txs_prunable_tip" (
  "txn_id" int PRIMARY KEY,
  "height" int
);

CREATE TABLE "txs_pruned" (
  "txn_id" int PRIMARY KEY,
  "version" int,
  "unlock_time" int,
  "vin_n_amount" int,
  "vin_n_key_offsets" int,
  "vin_n_k_image" char[32],
  "vout_n_amount" int,
  "vout_n_key" char[32],
  "tx_extra" varbinary,
  "rct_type" int,
  "txn_fee" int,
  "ecdhinfo" char[8],
  "outpk" char[32]
);
