from pymonerodb.utils.database import get_db_env
from pymonerodb.utils.readers import varint_decoder, pretty_print


def get_txs_prunable(env, txn_id: int, parse: bool = True) -> dict:
    child_db = b'txs_prunable'
    db_child = env.open_db(child_db)
    with env.begin() as txn:
        with txn.cursor(db_child) as cursor:
            data = cursor.get(txn_id.to_bytes(8, "little"))
            if parse:
                byte_length, data = parse_rctsig_prunable(data)
            return data


def parse_rctsig_prunable(transaction: bytes) -> (int, dict):
    # https://www.getmonero.org/library/Zero-to-Monero-2-0-0.pdf page 136
    idx = 0
    _, nbp = varint_decoder(transaction[idx:])
    idx = idx + _
    _, bp = parse_bp(transaction[idx:], nbp)
    idx = idx + _
    _, clsag = parse_clsag(transaction[idx:], nbp)
    idx = idx + _
    _, pseudoOuts = parse_pseudo_outs(transaction[idx:], nbp)
    idx = idx + 32
    return idx, {"nbp": nbp,
                 "bp": bp,
                 "CLSAGs": clsag,
                 "pseudoOuts": pseudoOuts
                 }


def parse_bp(data: bytes, count: int) -> (int, list):
    idx = 0
    bp = []
    for i in range(count):
        A = data[idx:idx + 32].hex()
        idx = idx + 32
        S = data[idx:idx + 32].hex()
        idx = idx + 32
        T1 = data[idx:idx + 32].hex()
        idx = idx + 32
        T2 = data[idx:idx + 32].hex()
        idx = idx + 32
        taux = data[idx:idx + 32].hex()
        idx = idx + 32
        mu = data[idx:idx + 32].hex()
        idx = idx + 32
        _, L_count = varint_decoder(data[idx:])
        idx = idx + _
        _, L = parse_l_r(data[idx:], L_count)
        idx = idx + _
        _, R_count = varint_decoder(data[idx:])
        idx = idx + _
        _, R = parse_l_r(data[idx:], R_count)
        idx = idx + _
        a = data[idx:idx + 32].hex()
        idx = idx + 32
        b = data[idx:idx + 32].hex()
        idx = idx + 32
        t = data[idx:idx + 32].hex()
        idx = idx + 32
        bp.append({
            "A": A,
            "S": S,
            "T1": T1,
            "T2": T2,
            "taux": taux,
            "mu": mu,
            "L": L,
            "R": R,
            "a": a,
            "b": b,
            "t": t,
        })
    return idx, bp


def parse_l_r(data: bytes, count: int) -> (int, list):
    idx = 0
    lr = []
    for i in range(count):
        lr.append(data[idx:idx+32].hex())
        idx = idx + 32
    return idx, lr


def parse_clsag(data: bytes, count: int) -> (int, list):
    idx = 0
    clsag = []
    for i in range(count):
        _, s = parse_s(data[idx:])
        idx = idx + _
        c1 = data[idx:idx+32].hex()
        idx = idx + 32
        D = data[idx:idx+32].hex()
        idx = idx + 32
        clsag.append({"s": s,
                      "c1": c1,
                      "D": D})
    return idx, clsag


def parse_s(data: bytes, count: int = 11) -> (int, list):
    idx = 0
    ss = []
    for i in range(count):
        ss.append(data[idx:idx+32].hex())
        idx = idx + 32
    return idx, ss


def parse_pseudo_outs(data: bytes, count: int) -> (int, list):
    idx = 0
    pseudo_outs = []
    for i in range(count):
        pseudo_outs.append(data[idx:idx+32].hex())
        idx = idx + 32
    return idx, pseudo_outs


if __name__ == "__main__":
    # txn_hash: 92dc4bb60bb74e5f9ebdd565546efe949814c8cb24b5baa1d9cc520e4bf8ffff
    txn_id = 16239072
    pretty_print(get_txs_prunable(get_db_env(), txn_id))
