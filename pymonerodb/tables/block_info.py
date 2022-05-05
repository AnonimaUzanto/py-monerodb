"""
Table contains one record for each block (2,595,692 entries).
"""
from pymonerodb.utils.database import get_db_env, zero_k_value, piconero
from pymonerodb.utils.readers import pretty_print, format_timestamp


def get_block_info(env, block_height: int) -> dict:
    child_db = b'block_info'
    block_height = block_height.to_bytes(8, "little")
    db_child = env.open_db(child_db)
    with env.begin(db_child) as txn:
        txn.set_dupsort_uint64(db_child)
        with txn.cursor(db_child) as cursor:
            if cursor.set_key_dup(zero_k_value, block_height):
                data = cursor.value()
        return {'timestamp': format_timestamp(int.from_bytes(data[8:16], "little")),
                'total_coins_generated': f"{int.from_bytes(data[16:24], 'little') * piconero:,}",
                'bi_timestamp': int.from_bytes(data[8:16], "little"),
                'bi_coins': int.from_bytes(data[16:24], "little"),
                'bi_weight': int.from_bytes(data[24:32], "little"),
                'bi_diff_lo': int.from_bytes(data[32:40], "little"),
                'bi_diff_hi': int.from_bytes(data[40:48], "little"),
                'bi_hash': data[48:80].hex(),
                'bi_cum_rct': int.from_bytes(data[80:88], "little"),
                'bi_long_term_block_weight': int.from_bytes(data[88:], "little")}


if __name__ == "__main__":
    env = get_db_env()
    block_height = 2595691
    pretty_print(get_block_info(env, block_height))
