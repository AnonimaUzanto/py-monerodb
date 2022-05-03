from pymonerodb.utils.database import get_db_env
from pymonerodb.utils.readers import pretty_print


def get_output_amounts(env, amount: int) -> dict:
    child_db = b'output_amounts'
    amount = amount.to_bytes(8, "little")
    db_child = env.open_db(child_db)
    with env.begin(db_child) as txn:
        with txn.cursor(db_child) as cursor:
            data = cursor.get(amount)
    return {"amount_index": int.from_bytes(data[:8], "little"),
            "output_id": int.from_bytes(data[8:16], "little"),
            "pubkey": data[16:48].hex(),
            "unlock_time": int.from_bytes(data[48:56], "little"),
            "height": int.from_bytes(data[56:64], "little")}


if __name__ == "__main__":
    output_amount = 500000000000000000
    pretty_print(get_output_amounts(get_db_env(), output_amount))
