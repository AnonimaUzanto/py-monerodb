import os

from pymonerodb.monerodb import MoneroDB
from pymonerodb.constants import DATABASE_DIRECTORY
from pymonerodb.utils.readers import read_json_from_file


def test_monerodb_blocks():
    monerodb = MoneroDB(DATABASE_DIRECTORY)

    test_alt_block_hash = 'e7ba7e4c1887a53758dca50a92af1de644ca47e61876d9fc13667b3ac77d41f5'

    block_test = monerodb.get_alt_block(test_alt_block_hash)
    assert type(block_test["miner_tx"]["extra"]) is list

    block_test = monerodb.get_alt_block(test_alt_block_hash, parse_tx=True)
    assert type(block_test["miner_tx"]["extra"]) is dict

