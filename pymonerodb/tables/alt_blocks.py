"""
Table typically contains very few records (1 entry).
"""
import binascii

from pymonerodb.utils.database import get_db_env
from pymonerodb.utils.readers import pretty_print
from pymonerodb.tables.blocks import parse_block


def get_alt_blocks(env, block_hash: str) -> dict:
    child_db = b'alt_blocks'
    block_hash = binascii.unhexlify(block_hash)
    db_child = env.open_db(child_db)
    with env.begin(db_child) as txn:
        with txn.cursor(db_child) as cursor:
            data = cursor.get(block_hash)
    return {"height": int.from_bytes(data[0:8], "little"),
            "cumulative_weight": int.from_bytes(data[8:16], "little"),
            "cumulative_difficulty_low": int.from_bytes(data[16:24], "little"),
            "cumulative_difficulty_high": int.from_bytes(data[24:32], "little"),
            "already_generated_coins": int.from_bytes(data[32:40], "little")
            } | parse_block(data[40:])


if __name__ == "__main__":
    block_hash = 'e7ba7e4c1887a53758dca50a92af1de644ca47e61876d9fc13667b3ac77d41f5'
    pretty_print(get_alt_blocks(get_db_env(), block_hash))
