"""
Table contains (72,892,050 entries).
"""
import binascii

from pymonerodb.utils.database import get_db_env
from pymonerodb.utils.readers import pretty_print


def get_output_txs(env, output_id: int) -> dict:
    child_db = b'output_txs'
    zero_k_value = binascii.unhexlify('0000000000000000')
    output_id = output_id.to_bytes(8, "little")
    db_child = env.open_db(child_db)
    with env.begin(db_child) as txn:
        txn.set_dupsort_uint64(db_child)
        with txn.cursor(db_child) as cursor:
            if cursor.set_key_dup(zero_k_value, output_id):
                data = cursor.value()
        return {"txn_hash": data[8:40].hex(),
                "local_index": int.from_bytes(data[40:], "little")}


if __name__ == "__main__":
    output_id = 72892049
    pretty_print(get_output_txs(get_db_env(), output_id))
