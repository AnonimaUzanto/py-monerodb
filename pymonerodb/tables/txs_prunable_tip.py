"""
Table contains (188,901 entries).
"""
from pymonerodb.utils.database import get_db_env


def get_txs_prunable_tip(env, txn_id: int) -> int:
    child_db = b'txs_prunable_tip'
    db_child = env.open_db(child_db)
    with env.begin(db_child) as txn:
        with txn.cursor(db_child) as cursor:
            txn_tip = cursor.get(txn_id.to_bytes(8, "little"))
    return int.from_bytes(txn_tip, "little")


if __name__ == "__main__":
    txn_id = 23897631
    print(get_txs_prunable_tip(get_db_env(), txn_id))
