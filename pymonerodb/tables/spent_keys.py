"""
Table contains one record for each spent key (64,238,296 records).
"""
import binascii

from pymonerodb.utils.database import get_db_env


def get_spent_keys(env, spent_key: str) -> bool:
    child_db = b'spent_keys'
    zero_k_value = binascii.unhexlify('0000000000000000')
    spent_key = binascii.unhexlify(spent_key)
    db_child = env.open_db(child_db)
    with env.begin(db_child) as txn:
        txn.set_dupsort_hash32(db_child)
        with txn.cursor(db_child) as cursor:
            return cursor.set_key_dup(zero_k_value, spent_key)


if __name__ == "__main__":
    spent_key = '648f41c9299040eeb54711673e16b2f46154de5f3e1f98831387db6df8ffffff'
    print(get_spent_keys(get_db_env(), spent_key))
