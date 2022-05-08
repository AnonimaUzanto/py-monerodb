from pymonerodb.monerodb import MoneroDB
from pymonerodb.constants import DATABASE_DIRECTORY


def test_monerodb_class():
    monerodb = MoneroDB(DATABASE_DIRECTORY)

    # get_block_height
    block_height = monerodb.get_block_height("f63f84ae373307d18cb1b59a01174d19d104d378cb905bccdd04c3938d7426e5")
    assert block_height == 2595691

    # get_block_info
    block_info = monerodb.get_block_info(2595691)
    assert type(block_info) is dict

    # get_hf_version
    hf_version = monerodb.get_hf_version(2595691)
    assert hf_version == 14

    # get_output_amount
    output_amount = monerodb.get_output_amount(500000000000000000)
    assert type(output_amount) is dict

    # get_output_tx
    output_tx = monerodb.get_output_tx(72892049)
    assert type(output_tx) is dict

    # get_spent_key
    spent_key = monerodb.get_spent_key("648f41c9299040eeb54711673e16b2f46154de5f3e1f98831387db6df8ffffff")
    assert type(spent_key) is bool

    # get_tx_indic
    txn_pruned = monerodb.get_tx_indic("84799c2fc4c18188102041a74cef79486181df96478b717e8703512c7f7f3349")
    txn_prunable = monerodb.get_tx_indic("92dc4bb60bb74e5f9ebdd565546efe949814c8cb24b5baa1d9cc520e4bf8ffff")
    assert type(txn_prunable) is dict
    assert type(txn_pruned) is dict

    # get_tx_output
    tx_output = monerodb.get_tx_output(23897631)
    assert type(tx_output) is list

    # get_txpool_blob
    txpool_blob = monerodb.get_txpool_blob("ba3053cfe21c632ed0b9771d2af963e335fdf22fcb0e7bfd17ce3ad4d1c28e14")
    assert type(txpool_blob) is dict

    # get_txpool_meta
    txpool_meta = monerodb.get_txpool_meta("ba3053cfe21c632ed0b9771d2af963e335fdf22fcb0e7bfd17ce3ad4d1c28e14")
    assert type(txpool_meta) is dict

    # get_txs_prunable_hash
    txs_prunable_hash = monerodb.get_txs_prunable_hash(23897631)
    assert type(txs_prunable_hash) is str

    # get_txs_prunable_tip
    tx_prunable_tip = monerodb.get_txs_prunable_tip(23897631)
    assert type(tx_prunable_tip) is int
