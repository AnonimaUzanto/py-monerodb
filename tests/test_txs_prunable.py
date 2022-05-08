import os

from pymonerodb.monerodb import MoneroDB
from pymonerodb.constants import DATABASE_DIRECTORY
from pymonerodb.utils.readers import read_json_from_file


def test_monerodb_txs_pruned():
    monerodb = MoneroDB(DATABASE_DIRECTORY)

    test_transactions = [16239072]

    transaction_root = f"{os.path.dirname(__file__)}/transactions/"

    for transaction_id in test_transactions:
        transaction_truth = read_json_from_file(f"{transaction_root}/txn_{transaction_id}.json")
        transaction_test = monerodb.get_txs_prunable(transaction_id)
        assert transaction_truth["rctsig_prunable"] == transaction_test
