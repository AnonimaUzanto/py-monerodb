"""
Table contains one record for each block (2,595,692 entries).
"""
import binascii

from pymonerodb.utils.database import get_db_env, zero_k_value


def get_block_heights(env, block_hash: str) -> int:
    child_db = b'block_heights'
    block_hash = binascii.unhexlify(block_hash)
    db_child = env.open_db(child_db)
    with env.begin(db_child) as txn:
        txn.set_dupsort_hash32(db_child)
        with txn.cursor(db_child) as cursor:
            height = None
            if cursor.set_key_dup(zero_k_value, block_hash):
                height = cursor.value()
                height = int.from_bytes(height[32:], "little")
    return height


if __name__ == "__main__":
    env = get_db_env()
    block_hash = 'f63f84ae373307d18cb1b59a01174d19d104d378cb905bccdd04c3938d7426e5'
    print(get_block_heights(env, block_hash))
