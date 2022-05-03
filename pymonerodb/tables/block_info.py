import binascii

from pymonerodb.utils.database import get_db_env
from pymonerodb.utils.readers import pretty_print


def get_block_info(env, block_height: int) -> dict:
    child_db = b'block_info'
    zero_k_value = binascii.unhexlify('0000000000000000')
    block_height = block_height.to_bytes(8, "little")
    db_child = env.open_db(child_db)
    with env.begin(db_child) as txn:
        txn.set_dupsort_uint64(db_child)
        with txn.cursor(db_child) as cursor:
            if cursor.set_key_dup(zero_k_value, block_height):
                data = cursor.value()
        return {'bi_timestamp': int.from_bytes(data[8:16], "little"),
                'bi_coins': int.from_bytes(data[16:24], "little"),
                'bi_weight': int.from_bytes(data[24:32], "little"),
                'bi_diff_lo': int.from_bytes(data[32:40], "little"),
                'bi_diff_hi': int.from_bytes(data[40:48], "little"),
                'bi_hash': data[48:80].hex(),
                'bi_cum_rct': int.from_bytes(data[80:88], "little"),
                'bi_long_term_block_weight': int.from_bytes(data[88:96], "little")}


if __name__ == "__main__":
    block_height = 2595691
    pretty_print(get_block_info(get_db_env(), block_height))
