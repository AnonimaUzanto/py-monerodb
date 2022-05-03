import lmdb

from pymonerodb.constants import DATABASE_DIRECTORY


piconero = 10E-12


def get_db_env(directory: str = DATABASE_DIRECTORY) -> lmdb.Environment:
    return lmdb.open(directory, max_dbs=32, readonly=True)


def list_tables(env: lmdb.Environment) -> dict:
    tables = {}

    with env.begin() as txn:
        with txn.cursor() as cursor:
            for key, value in cursor:
                tables[key.decode()] = key
    return tables


def describe_tables(env: lmdb.Environment) -> dict:
    tables = {}

    with env.begin() as txn:
        with txn.cursor() as cursor:
            for key, value in cursor:
                db_child = env.open_db(key)
                tables[key.decode()] = db_child.flags()
    return tables


def last_cursor_data(env: lmdb.Environment, child_db: bytes):
    db_child = env.open_db(child_db)
    with env.begin(db_child) as txn:
        with txn.cursor() as cursor:
            cursor.last()
            key = cursor.key()
            val = cursor.value()
    return {"key": key, "val": val}


def get_n_records(cursor: lmdb.Cursor, n_records: int, orientation: str = "first") -> list:
    records = []
    cursor.last() if orientation == "last" else cursor.first()
    for i in range(n_records):
        k, v = cursor.item()
        records.append((k, v))
        cursor.iterprev() if orientation == "last" else cursor.iternext()
    return records
