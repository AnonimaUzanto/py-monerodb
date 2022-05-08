import os

from pymonerodb.monerodb import MoneroDB
from pymonerodb.constants import DATABASE_DIRECTORY
from pymonerodb.utils.readers import read_json_from_file


def test_monerodb_blocks():
    monerodb = MoneroDB(DATABASE_DIRECTORY)

    test_blocks_old_signatures = [0,        # v1
                                  1009827,  # v2
                                  1141317]  # v3

    test_blocks = [1220516,  # v4
                   1288616,  # v5
                   1400000,  # v6
                   1546000,  # v7
                   1685555,  # v8
                   1686275,  # v9
                   1788000,  # v10
                   1788720,  # v11
                   1978433,  # v12
                   2210000,  # v13
                   2210720]  # v14

    block_root = f"{os.path.dirname(__file__)}/blocks/"

    for block_id in test_blocks:
        block_truth = read_json_from_file(f"{block_root}/block_{block_id}.json")
        block_test = monerodb.get_block(block_id)
        assert block_truth == block_test

        block_test = monerodb.get_block(block_id, parse_tx=True)
        assert type(block_test["miner_tx"]["extra"]) is dict
