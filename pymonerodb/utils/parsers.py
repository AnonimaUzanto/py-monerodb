from functools import partial

from pymonerodb.utils.readers import varint_decoder


def parse_tx_extra(data: bytes, minertx: bool) -> dict:
    # https://github.com/monero-project/monero/blob/master/src/cryptonote_basic/tx_extra.h
    # https://monero.stackexchange.com/questions/11888/complete-extra-field-structure-standard-interpretation
    padding = []
    public_key = []
    additional_public_keys = []
    extra_nonce = []
    merge_mining = []
    minergate = []
    unknown_tx_data = []

    known_bytes = {b'\x00': (parse_padding, padding),  # padding, zero bytes
                   b'\x01': (parse_public_key, public_key),  # public key, 32 bytes
                   b'\x04': (parse_additional_public_keys, additional_public_keys),  # additional public keys, next byte equals number of public keys
                   b'\x02': (partial(parse_extra_nonce, minertx=minertx), extra_nonce),  # extra nonce, next byte equals byte length
                   b'\x03': (parse_merge_mining, merge_mining),  # p2pool, next byte equals byte length
                   b'\xDE': (parse_minergate, minergate)  # minergate tag
                   }

    idx = 0
    len_tx_extra = len(data)
    if len_tx_extra == 0:
        return {}
    while idx < len_tx_extra:
        valid = False
        sub_idx = idx
        while not valid and sub_idx < len_tx_extra:
            # iterate to find first valid byte
            while data[sub_idx:sub_idx + 1] not in known_bytes.keys() and sub_idx < len_tx_extra:
                sub_idx = sub_idx + 1
            if sub_idx == len_tx_extra:
                unknown_tx_data.append(data[idx:sub_idx].hex())
                idx = sub_idx
                continue
            fn, lst = known_bytes.get(data[sub_idx:sub_idx + 1])
            valid, _, value = fn(data[sub_idx:])
            # check validity of byte data
            if valid:
                # if valid append two lists and continue
                lst.append(value)
                if sub_idx != idx:
                    unknown_tx_data.append(data[idx:sub_idx].hex())
                idx = sub_idx + _
                sub_idx = sub_idx + _
            else:
                # if not valid move sub_idx forward and continue
                sub_idx = sub_idx + _

    tx_extra_dict = {"padding": padding,
                     "public_key": public_key,
                     "additional_public_keys": additional_public_keys,
                     "extra_nonce": extra_nonce,
                     "merge_mining": merge_mining,
                     "minergate": minergate,
                     "unknown_tx_data": unknown_tx_data}

    return {k: v for k, v in tx_extra_dict.items() if v}


def parse_public_key(data: bytes) -> (int, str):
    valid = False
    idx = 1
    public_key = data[idx:idx+32].hex()
    if idx + 32 <= len(data):
        idx = idx + 32
        valid = True
    return valid, idx, public_key


def parse_additional_public_keys(data: bytes) -> (int, list):
    valid = False
    idx = 1
    public_key_count = data[idx]
    public_keys = []
    for i in range(public_key_count):
        public_keys.append(data[idx:idx+32].hex())
        idx = idx + 32
    if idx <= len(data):
        valid = True
    return valid, idx, public_keys


def parse_extra_nonce(data: bytes, minertx: bool) -> (int, str):
    known_nonces = {b'\x00': "tx_extra_nonce_payment_id",
                    b'\x01': "tx_extra_nonce_encrypted_payment_id"
                    }
    valid = False
    idx = 1
    byte_length = data[idx]
    idx = idx + 1
    tx_extra_nonce = "tx_extra_nonce"
    if not minertx:
        tx_extra_nonce = data[idx:idx+1]
        tx_extra_nonce = known_nonces.get(tx_extra_nonce)
        idx = idx + 1
        byte_length = byte_length - 1
    extra_nonce = data[idx:idx+byte_length].hex()
    idx = idx + byte_length
    if idx <= len(data):
        valid = True
        return valid, idx, {tx_extra_nonce: extra_nonce}
    idx = 1
    return valid, idx, None


def parse_merge_mining(data: bytes) -> (int, str):
    valid = False
    idx = 1
    _, byte_length = varint_decoder(data[idx:])
    if byte_length == 0:
        return valid, idx, None
    idx = idx + _
    merge_mining = data[idx:idx+byte_length].hex()
    idx = idx + byte_length
    if idx <= len(data):
        valid = True
    return valid, idx, merge_mining


def parse_minergate(data: bytes) -> (int, str):
    valid = False
    idx = 0
    byte_length = data[idx]
    if byte_length == 0:
        return valid, idx, None
    idx = idx + 1
    minergate = data[idx:idx+byte_length].hex()
    idx = idx + byte_length
    if idx <= len(data):
        valid = True
    return valid, idx, minergate


def parse_padding(data: bytes) -> (int, int):
    valid = False
    idx = 0
    while data[idx:idx+1] == b'\x00':
        idx = idx + 1
    padding = data[:idx].hex()
    if idx < len(data):
        return valid, idx, None
    valid = True
    return valid, idx, padding
