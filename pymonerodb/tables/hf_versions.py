"""
Table contains one record for each block (2,595,692 entries).
"""
from pymonerodb.utils.database import get_db_env


def get_hf_versions(env, block_id: int) -> int:
    child_db = b'hf_versions'
    db_child = env.open_db(child_db)
    with env.begin(db_child) as txn:
        with txn.cursor(db_child) as cursor:
            version = cursor.get(block_id.to_bytes(8, "little"))
    return int.from_bytes(version, "little")


if __name__ == "__main__":
    block_id = 2595691
    print(get_hf_versions(get_db_env(), block_id))
