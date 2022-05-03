import lmdb
import pymonerodb.tables as xmrtables

from .constants import DATABASE_DIRECTORY


class MoneroDB:
    def __init__(self, directory=None):
        self.directory = DATABASE_DIRECTORY if directory is None else directory
        self.env = lmdb.open(self.directory, max_dbs=32, readonly=True)

    def get_alt_block(self, block_hash: str) -> dict:
        return xmrtables.get_alt_blocks(self.env, block_hash)

    def get_block_height(self, block_hash: str) -> int:
        return xmrtables.get_block_heights(self.env, block_hash)

    def get_block_info(self, block_height: int) -> dict:
        return xmrtables.get_block_info(self.env, block_height)

    def get_block(self, block_id: int) -> dict:
        return xmrtables.get_block(self.env, block_id)

    def get_hf_version(self, block_id: int) -> int:
        return xmrtables.get_hf_versions(self.env, block_id)

    def get_output_amount(self, amount: int) -> dict:
        return xmrtables.get_output_amounts(self.env, amount)

    def get_output_tx(self, output_id: int) -> dict:
        return xmrtables.get_output_txs(self.env, output_id)

    def get_spent_key(self, spent_key: str) -> bool:
        return xmrtables.get_spent_keys(self.env, spent_key)

    def get_tx_indic(self, txn_hash: str) -> dict:
        return xmrtables.get_tx_indices(self.env, txn_hash)

    def get_tx_output(self, txn_id: int) -> list:
        return xmrtables.get_tx_outputs(self.env, txn_id)

    def get_txpool_blob(self, txn_hash: str) -> dict:
        return xmrtables.get_txpool_blob(self.env, txn_hash)

    def get_txpool_meta(self, txn_hash: str) -> dict:
        return xmrtables.get_txpool_meta(self.env, txn_hash)

    def get_txs_prunable(self, txn_id: int) -> dict:
        return xmrtables.get_txs_prunable(self.env, txn_id)

    def get_txs_prunable_hash(self, txn_id: int) -> str:
        return xmrtables.get_txs_prunable_hash(self.env, txn_id)

    def get_txs_prunable_tip(self, txn_id: int) -> int:
        return xmrtables.get_txs_prunable_tip(self.env, txn_id)

    def get_txs_pruned(self, txn_id: int) -> dict:
        return xmrtables.get_txs_pruned(self.env, txn_id)
