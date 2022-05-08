"""
Table contains one record for each transaction (23,897,632 entries).
"""
from pymonerodb.utils.database import get_db_env
from pymonerodb.utils.readers import varint_decoder, pretty_print
from pymonerodb.utils.parsers import parse_tx_extra


def get_txs_pruned(env, txn_id: int, parse: bool = True, parse_tx: bool = False) -> dict:
    child_db = b'txs_pruned'
    db_child = env.open_db(child_db)
    with env.begin() as txn:
        with txn.cursor(db_child) as cursor:
            data = cursor.get(txn_id.to_bytes(8, "little"))
    if parse:
        byte_length, data = parse_transaction(data, parse_tx)
    return data


def parse_transaction(transaction: bytes, parse_tx: bool = False) -> (int, dict):
    # https://www.getmonero.org/library/Zero-to-Monero-2-0-0.pdf page 136
    idx = 0
    _, version = varint_decoder(transaction[idx:])
    idx = idx + _
    _, unlock_time = varint_decoder(transaction[idx:])
    idx = idx + _
    _, vin_count = varint_decoder(transaction[idx:])
    idx = idx + _
    _, vins = parse_vins(transaction[idx:], vin_count)
    idx = idx + _
    _, vout_count = varint_decoder(transaction[idx:])
    idx = idx + _
    _, vouts = parse_vouts(transaction[idx:], vout_count)
    idx = idx + _
    _, tx_extra_length = varint_decoder(transaction[idx:])
    idx = idx + _
    tx_extra = transaction[idx:idx+tx_extra_length]
    if parse_tx:
        tx_extra = parse_tx_extra(tx_extra, minertx=False)
    else:
        tx_extra = list(tx_extra)
    idx = idx + tx_extra_length
    tx = {"version": version,
          "unlock_time": unlock_time,
          "vin": vins,
          "vout": vouts,
          "extra": tx_extra}
    if version > 1:
        _, rct_type = varint_decoder(transaction[idx:])
        idx = idx + _
        _, txn_fee = varint_decoder(transaction[idx:])
        idx = idx + _
        _, ecdh_info = parse_ecdh_info(transaction[idx:], vout_count)
        idx = idx + _
        _, outpk = parse_outpk(transaction[idx:], vout_count)
        idx = idx + _
        tx = tx | {"rct_signatures": {
            "type": rct_type,
            "txnFee": txn_fee,
            "ecdhInfo": ecdh_info,
            "outPk": outpk}
        }
    return idx, tx


def parse_vins(data: bytes, count: int) -> (int, list):
    # https://github.com/monero-project/monero/blob/master/src/cryptonote_basic/cryptonote_basic.h#L572
    idx = 0
    vins = []
    for i in range(count):
        txin_to_key = data[idx:idx + 1].hex()
        idx = idx + 1
        _, vin_amount = varint_decoder(data[idx:])
        idx = idx + _
        _, vin_key_count = varint_decoder(data[idx:])
        idx = idx + _
        _, key_offsets = parse_key_offsets(data[idx:], vin_key_count)
        idx = idx + _
        k_image = data[idx:idx+32].hex()
        idx = idx + 32
        vins.append({"key": {"amount": vin_amount,
                             "key_offsets": key_offsets,
                             "k_image": k_image}})
    return idx, vins


def parse_key_offsets(data: bytes, count: int) -> (int, list):
    idx = 0
    key_offsets = []
    for i in range(count):
        _, key_offset = varint_decoder(data[idx:])
        idx = idx + _
        key_offsets.append(key_offset)
    return idx, key_offsets


def parse_vouts(data: bytes, count: int) -> (int, list):
    # https://github.com/monero-project/monero/blob/master/src/cryptonote_basic/cryptonote_basic.h#L572
    idx = 0
    vouts = []
    for i in range(count):
        _, vout_amount = varint_decoder(data[idx:])
        idx = idx + _
        txout_to_key = data[idx:idx+1].hex()
        idx = idx + 1
        vout_key = data[idx:idx+32].hex()
        idx = idx + 32
        vouts.append({"amount": vout_amount,
                      "target": {
                          "key": vout_key}
                      })
    return idx, vouts


def parse_ecdh_info(data: bytes, count: int) -> (int, list):
    idx = 0
    ecdh_info = []
    for i in range(count):
        ecdh = data[idx:idx+8].hex()
        idx = idx + 8
        ecdh_info.append({"amount": ecdh})
    return idx, ecdh_info


def parse_outpk(data: bytes, count: int) -> (int, list):
    idx = 0
    outpk = []
    for i in range(count):
        pk = data[idx:idx+32].hex()
        idx = idx + 32
        outpk.append(pk)
    return idx, outpk


if __name__ == "__main__":
    # first txn_id: 111, tx_hash: beb76a82ea17400cd6d7f595f70e1667d2018ed8f5a78d1ce07484222618c3cd
    # txn_id: 8562996, txn_hash: 84799c2fc4c18188102041a74cef79486181df96478b717e8703512c7f7f3349
    txn_id = 111
    pretty_print(get_txs_pruned(get_db_env(), txn_id))
