"""
Table contains one record for each transaction (23,897,632 entries).
"""
from pymonerodb.utils.database import get_db_env
from pymonerodb.utils.readers import varint_decoder, pretty_print


def get_txs_pruned(env, txn_id: int, parse: bool = True) -> dict:
    child_db = b'txs_pruned'
    db_child = env.open_db(child_db)
    with env.begin() as txn:
        with txn.cursor(db_child) as cursor:
            data = cursor.get(txn_id.to_bytes(8, "little"))
            if parse:
                byte_length, data = parse_transaction(data)
            return data


def parse_transaction(transaction: bytes) -> (int, dict):
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
    tx_extra = list(transaction[idx:idx+tx_extra_length])
    parse_tx_extra(transaction[idx:idx+tx_extra_length])
    idx = idx + tx_extra_length
    tx = {"version": version,
                 "unlock_time": unlock_time,
                 "vin": vins,
                 "vout": vouts,
                 "tx_extra": tx_extra}
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
    idx = 0
    vins = []
    for i in range(count):
        txin_to_key = data[idx:idx + 1].hex()  # https://github.com/monero-project/monero/blob/master/src/cryptonote_basic/cryptonote_basic.h#L572
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
    idx = 0
    vouts = []
    for i in range(count):
        _, vout_amount = varint_decoder(data[idx:])
        idx = idx + _
        txout_to_key = data[idx:idx+1].hex()  # https://github.com/monero-project/monero/blob/master/src/cryptonote_basic/cryptonote_basic.h#L572
        idx = idx + 1
        vout_key = data[idx:idx+32].hex()
        idx = idx + 32
        vouts.append({"amount": vout_amount,
                      "target": {
                          "key": vout_key}
                      })
    return idx, vouts


def parse_tx_extra(data: bytes) -> (int, list):
    # ToDo: Determine which tx_extra tags are valid for a transaction
    # https://github.com/monero-project/monero/blob/master/src/cryptonote_basic/tx_extra.h
    # https://monero.stackexchange.com/questions/11888/complete-extra-field-structure-standard-interpretation
    tx_extra_bytes = {
        # b'\x00': "padding",  # padding, zero bytes
        b'\x01': parse_public_key,  # public key, 32 bytes
        b'\x02': parse_extra_nonce,  # extra nonce, next byte equals byte length
        # b'\x03': parse_merge_mining,  # no longer used
        # b'\x04': parse_additional_public_keys,  # next byte equals number of public keys
        # b'\xDE': parse_minergate_tag  # unknown
        }
    idx = 0
    tx_extra = []
    while data[idx:idx + 1] in tx_extra_bytes.keys():
        fn = tx_extra_bytes.pop(data[idx:idx + 1])
        idx = idx + 1
        _, extra = fn(data[idx:])
        tx_extra.append(extra)
        idx = idx + _
    return idx, tx_extra


def parse_public_key(data: bytes) -> (int, str):
    idx = 0
    public_key = data[idx:idx+32].hex()
    idx = idx + 32
    return idx, public_key


def parse_extra_nonce(data: bytes) -> (int, str):
    idx = 0
    byte_length = data[idx]
    idx = idx + 1
    extra_nonce = data[idx:idx+byte_length]
    idx = idx + byte_length
    return idx, extra_nonce


def parse_ecdh_info(data: bytes, count: int) -> (int, list):
    idx = 0
    ecdh_info = []
    for i in range(count):
        ecdh = data[idx:idx+8].hex()
        idx = idx + 8
        ecdh_info.append(ecdh)
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
    # txn_hash: 84799c2fc4c18188102041a74cef79486181df96478b717e8703512c7f7f3349
    txn_id = 8562996
    pretty_print(get_txs_pruned(get_db_env(), txn_id))


# first tx id: 111
# first tx hash: beb76a82ea17400cd6d7f595f70e1667d2018ed8f5a78d1ce07484222618c3cd
