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
    print(txin_to_scripthash)
    idx = idx + 1
    txin_gen = block[idx:idx+1].hex()  # https://github.com/monero-project/monero/blob/master/src/cryptonote_basic/cryptonote_basic.h#L572
    print(txin_gen)
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
    parse_tx_extra(block[idx:idx+tx_extra_length])
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


def parse_tx_extra(data: bytes) -> dict:
    # https://github.com/monero-project/monero/blob/master/src/cryptonote_basic/tx_extra.h
    # https://monero.stackexchange.com/questions/11888/complete-extra-field-structure-standard-interpretation

    padding = []
    public_key = []
    extra_nonce = []
    merge_mining = []
    additional_public_keys = []
    minergate = []
    remainder = []

    idx = 0
    while idx < len(data):
        tag = data[idx:idx + 1]
        idx = idx + 1
        if tag == b'\x00':  # padding, zero bytes
            padding.append(idx-1)
        elif tag == b'\x01':  # public key, 32 bytes
            count = 1
            _, pk = parse_public_keys(data[idx:], count)
            public_key.append(pk)
            idx = idx + _
        elif tag == b'\x04':  # additional public keys, next byte equals number of public keys
            count = data[idx:idx+1]
            idx = idx + 1
            _, pk = parse_public_keys(data[idx:], count)
            additional_public_keys.append(pk)
            idx = idx + _
        elif tag == b'\x02':  # extra nonce, next byte equals byte length
            _, known = parse_known(data[idx:])
            extra_nonce.append(known)
            idx = idx + _
        elif tag == b'\x03':  # p2pool, next byte equals byte length
            _, known = parse_known(data[idx:])
            merge_mining.append(known)
            idx = idx + _
        elif tag == b'\xDE':  # minergate tag
            _, known = parse_known(data[idx:])
            minergate.append(known)
            idx = idx + _
        else:
            _, unknown = parse_unknown(data[idx:])
            remainder.append(unknown)
            idx = idx + _

    return {"padding": padding,
            "minergate": minergate,
            "public_key": public_key,
            "extra_nonce": extra_nonce,
            "merge_mining": merge_mining,
            "additional_public_keys": additional_public_keys,
            "remainder": remainder}


def parse_padding(data: bytes) -> (int, list):
    idx = 0
    while data[idx] == 0 and idx+1 < len(data):
        idx = idx + 1
    return idx, list(data[0:idx])


def parse_public_keys(data: bytes, count: int) -> (int, list):
    idx = 0
    public_keys = []
    for i in range(count):
        public_keys.append(data[idx:idx+32])
        idx = idx + 32
    return idx, public_keys


def parse_known(data: bytes) -> (int, list):
    idx = 0
    byte_length = data[idx]
    idx = idx + 1
    extra_nonce = data[idx:idx+byte_length]
    idx = idx + byte_length
    return idx, extra_nonce


def parse_unknown(data: bytes) -> (int, list):
    idx = 0
    _, byte_length = varint_decoder(data[idx:])
    idx = idx + _
    junk = data[idx:idx+byte_length]
    idx = idx + byte_length
    return idx, junk


if __name__ == "__main__":
    block_id = 2595691
    pretty_print(get_block(get_db_env(), block_id))
