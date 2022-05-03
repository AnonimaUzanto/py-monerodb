from pymonerodb.utils.database import get_db_env


def get_txs_prunable_hash(env, txn_id: int) -> str:
    child_db = b'txs_prunable_hash'
    db_child = env.open_db(child_db)
    with env.begin(db_child) as txn:
        with txn.cursor(db_child) as cursor:
            txn_hash = cursor.get(txn_id.to_bytes(8, "little"))
    return txn_hash.hex()


if __name__ == "__main__":
    txn_id = 23897631
    print(get_txs_prunable_hash(get_db_env(), txn_id))
