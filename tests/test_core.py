from unittest import mock

from averell.core import get_corpora


#@patch('averell.utils.download_corpora')
def test_download_corpora_called(mock):
    get_corpora([2, 3], "line", "corpora")
    assert mock.get_corpora


def test_get_corpora_index_not_in_range():
    corpus_indices = [500000]
    assert [] == get_corpora(corpus_indices)


@mock.patch('averell.utils.download_corpora')
def test_get_corpora():
    assert True
