import binascii

from pymonerodb.utils.database import get_db_env
from pymonerodb.utils.readers import pretty_print


def get_tx_indices(env, txn_hash: str) -> dict:
    child_db = b'tx_indices'
    zero_k_value = binascii.unhexlify('0000000000000000')
    txn_hash = binascii.unhexlify(txn_hash)
    db_child = env.open_db(child_db)
    with env.begin(db_child) as txn:
        txn.set_dupsort_hash32(db_child)
        with txn.cursor(db_child) as cursor:
            if cursor.set_key_dup(zero_k_value, txn_hash):
                data = cursor.value()
        return {"txn_id": int.from_bytes(data[32:40], "little"),
                "unlock_time": int.from_bytes(data[40:48], "little"),
                "block_id": int.from_bytes(data[48:], "little")}


if __name__ == "__main__":
    txn_pruned_hash = "84799c2fc4c18188102041a74cef79486181df96478b717e8703512c7f7f3349"
    txn_prunable_hash = "92dc4bb60bb74e5f9ebdd565546efe949814c8cb24b5baa1d9cc520e4bf8ffff"
    pretty_print(get_tx_indices(get_db_env(), txn_pruned_hash))
    pretty_print(get_tx_indices(get_db_env(), txn_prunable_hash))
