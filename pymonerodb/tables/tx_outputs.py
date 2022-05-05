"""
Table contains one record for each transaction (23,897,632 entries).
"""
from pymonerodb.utils.database import get_db_env


def get_tx_outputs(env, txn_id: int) -> list:
    child_db = b'tx_outputs'
    db_child = env.open_db(child_db)
    with env.begin(db_child) as txn:
        with txn.cursor(db_child) as cursor:
            data = cursor.get(txn_id.to_bytes(8, "little"))
            txn_amount_output_indices = []
            idx = 0
            while idx < len(data):
                txn_amount_output_indices.append(int.from_bytes(data[idx:idx+8], "little"))
                idx = idx + 8
    return txn_amount_output_indices


if __name__ == "__main__":
    txn_id = 23897631
    print(get_tx_outputs(get_db_env(), txn_id))
