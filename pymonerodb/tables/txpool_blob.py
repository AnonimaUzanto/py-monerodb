"""
Table contains one record for each transaction in the current transaction pool (8 entries).
"""
import binascii

from pymonerodb.utils.database import get_db_env
from pymonerodb.utils.readers import pretty_print
from pymonerodb.tables.txs_pruned import parse_transaction
from pymonerodb.tables.txs_prunable import parse_rctsig_prunable


def get_txpool_blob(env, txn_hash: str, parse: bool = True) -> dict:
    child_db = b'txpool_blob'
    txn_hash = binascii.unhexlify(txn_hash)
    db_child = env.open_db(child_db)
    with env.begin() as txn:
        with txn.cursor(db_child) as cursor:
            cursor.first()
            data = cursor.get(txn_hash)
            if parse:
                idx, pruned_transaction = parse_transaction(data)
                byte_length, prunable_transaction = parse_rctsig_prunable(data[idx:])
            return pruned_transaction | prunable_transaction


if __name__ == "__main__":
    txn_hash = "ba3053cfe21c632ed0b9771d2af963e335fdf22fcb0e7bfd17ce3ad4d1c28e14"
    pretty_print(get_txpool_blob(get_db_env(), txn_hash, True))

