"""
Table contains one record for each block (2,595,692 entries).
"""
from pymonerodb.utils.database import get_db_env
from pymonerodb.utils.readers import varint_decoder, pretty_print


def get_block(env, block_id: int, parse: bool = True) -> dict:
    child_db = b'blocks'
    db_child = env.open_db(child_db)
    with env.begin() as txn:
        with txn.cursor(db_child) as cursor:
            data = cursor.get(block_id.to_bytes(8, "little"))
            if parse:
                data = parse_block(data)
            return data


def parse_block(block: bytes) -> dict:
    idx = 0
    _, major_version = varint_decoder(block[idx:])
    idx = idx + _
    _, minor_version = varint_decoder(block[idx:])
    idx = idx + _
    _, timestamp = varint_decoder(block[idx:])
    idx = idx + _
    prev_id = block[idx:idx+32].hex()
    idx = idx + 32
    nonce = int.from_bytes(block[idx:idx+4], "little")
    idx = idx + 4
    _, miner_tx_ver = varint_decoder(block[idx:])
    idx = idx + _
    _, unlock_time = varint_decoder(block[idx:])
    idx = idx + _
    txin_to_scripthash = block[idx:idx+1].hex()  # https://github.com/monero-project/monero/blob/master/src/cryptonote_basic/cryptonote_basic.h#L572
    idx = idx + 1
    txin_gen = block[idx:idx+1].hex()  # https://github.com/monero-project/monero/blob/master/src/cryptonote_basic/cryptonote_basic.h#L572
    idx = idx + 1
    _, height = varint_decoder(block[idx:])
    idx = idx + _
    _, vout_count = varint_decoder(block[idx:])
    idx = idx + _
    _, vouts = parse_vouts(block[idx:], vout_count)
    idx = idx + _
    _, tx_extra_length = varint_decoder(block[idx:])
    idx = idx + _
    miner_tx_extra = list(block[idx:idx+tx_extra_length])
    # miner_tx_extra = parse_tx_extra(block[idx:idx+tx_extra_length])
    idx = idx + tx_extra_length
    _, rct_signatures_type = varint_decoder(block[idx:])
    idx = idx + _
    if idx == len(block):
        rct_signatures_type = None
        tx_hashes = None
    elif rct_signatures_type == 0:
        _, tx_count = varint_decoder(block[idx:])
        idx = idx + _
        _, tx_hashes = parse_tx_hashes(block[idx:], tx_count)
    else:
        tx_count = rct_signatures_type
        rct_signatures_type = None
        _, tx_hashes = parse_tx_hashes(block[idx:], tx_count)
    return {
        "major_version": major_version,
        "minor_version": minor_version,
        "timestamp": timestamp,
        "prev_id": prev_id,
        "nonce": nonce,
        "miner_tx": {
            "version": miner_tx_ver,
            "unlock_time": unlock_time,
            "vin": [ {
                "gen": {
                    "height": height
                }
            }
            ],
            "vout": vouts,
            "extra": miner_tx_extra,
            "rct_signatures": {
                "type": rct_signatures_type
            }
        },
        "tx_hashes": tx_hashes
    }


def parse_vouts(data: bytes, count: int) -> (int, list):
    # vout_tx_out_to_key is byte indicator
    # https://github.com/monero-project/monero/blob/master/src/cryptonote_basic/cryptonote_basic.h#L572
    idx = 0
    vouts = []
    for i in range(count):
        _, vout_amount = varint_decoder(data[idx:])
        idx = idx + _
        vout_tx_out_to_key = data[idx:idx+1].hex()
        idx = idx + 1
        vout_key = data[idx:idx+32].hex()
        idx = idx + 32
        vouts.append({"amount": vout_amount,
                      "target": {
                          "key": vout_key}
                      })
    return idx, vouts


def parse_tx_hashes(data: bytes, count: int) -> (int, list):
    idx = 0
    tx_hashes = []
    for i in range(count):
        tx_hashes.append(data[idx:idx+32].hex())
        idx = idx + 32
    return idx, tx_hashes


def parse_tx_extra(data: bytes) -> list:
    # https://github.com/monero-project/monero/blob/master/src/cryptonote_basic/tx_extra.h
    # https://monero.stackexchange.com/questions/11888/complete-extra-field-structure-standard-interpretation
    tx_extra_bytes = {
        # b'\x00': parse_padding,  # padding, zero bytes
        b'\x01': parse_public_key,  # public key, 32 bytes
        b'\x02': parse_extra_nonce,  # extra nonce, next byte equals byte length
        b'\x03': parse_merge_mining,  # no longer used
        b'\x04': parse_additional_public_keys,  # next byte equals number of public keys
        b'\xDE': parse_minergate_tag  # unknown
        }
    idx = 0
    tx_extra = []
    while data[idx:idx + 1] in tx_extra_bytes.keys():
        tag = data[idx:idx + 1]
        fn = tx_extra_bytes.pop(tag)
        idx = idx + 1
        if idx + data[idx] >= len(data):
            idx = idx - 1
            break
        _, extra = fn(data[idx:])
        tx_extra.append(extra)
        idx = idx + _
    return tx_extra


def parse_padding(data: bytes) -> (int, list):
    idx = 0
    while data[idx] == 0 and idx+1 < len(data):
        idx = idx + 1
    return idx, list(data[0:idx])


def parse_public_key(data: bytes) -> (int, str):
    idx = 0
    public_key = data[idx:idx+32].hex()
    idx = idx + 32
    return idx, public_key


def parse_extra_nonce(data: bytes) -> (int, list):
    idx = 0
    byte_length = data[idx]
    idx = idx + 1
    extra_nonce = list(data[idx:idx+byte_length])
    idx = idx + byte_length
    return idx, extra_nonce


def parse_merge_mining(data: bytes) -> (int, str):
    idx = 0
    byte_length = data[idx]
    idx = idx + 1
    merge_mining = data[idx:idx+byte_length]
    idx = idx + byte_length
    return idx, merge_mining


def parse_additional_public_keys(data: bytes) -> (int, list):
    idx = 0
    additional_public_keys = []
    count = data[idx]
    idx = idx + 1
    for i in range(count):
        additional_public_keys.append(data[idx:idx+32])
        idx = idx + 32
    return idx, additional_public_keys


def parse_minergate_tag(data: bytes) -> (int, str):
    idx = 0
    byte_length = data[idx]
    idx = idx + 1
    minergate = data[idx:idx+byte_length]
    idx = idx + byte_length
    return idx, minergate


if __name__ == "__main__":
    block_id = 2595691
    pretty_print(get_block(get_db_env(), block_id))
