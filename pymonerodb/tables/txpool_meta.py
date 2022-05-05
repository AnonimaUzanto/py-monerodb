"""
Table contains one record for each transaction in the current transaction pool (8 entries).
"""
import binascii

from pymonerodb.utils.database import get_db_env
from pymonerodb.utils.readers import pretty_print


def get_txpool_meta(env, txn_hash: str) -> dict:
    child_db = b'txpool_meta'
    txn_hash = binascii.unhexlify(txn_hash)
    db_child = env.open_db(child_db)
    with env.begin(db_child) as txn:
        with txn.cursor(db_child) as cursor:
            data = cursor.get(txn_hash)
    return {"max_used_block_id": data[0:32].hex(),
            "last_failed_id": data[32:64].hex(),
            "weight": int.from_bytes(data[64:72], "little"),
            "fee": int.from_bytes(data[72:80], "little"),
            "max_used_block_height": int.from_bytes(data[80:88], "little"),
            "last_failed_height": int.from_bytes(data[88:96], "little"),
            "receive_time": int.from_bytes(data[96:104], "little"),
            "last_relayed_time": int.from_bytes(data[104:112], "little"),
            "kept_by_block": int.from_bytes(data[112:113], "little"),
            "relayed": int.from_bytes(data[113:114], "little"),
            "do_not_relay": int.from_bytes(data[114:115], "little"),
            "double_spend_seen": int.from_bytes(data[115:116], "little"),
            "pruned": int.from_bytes(data[116:117], "little"),
            "is_local": int.from_bytes(data[117:118], "little"),
            "dandelionpp_stem": int.from_bytes(data[118:119], "little"),
            "is_forwarding": int.from_bytes(data[119:120], "little"),
            "bf_padding": data[120:123].hex(),
            "padding": data[123:192].hex()}


if __name__ == "__main__":
    txn_hash = "ba3053cfe21c632ed0b9771d2af963e335fdf22fcb0e7bfd17ce3ad4d1c28e14"
    pretty_print(get_txpool_meta(get_db_env(), txn_hash))
