from io import BytesIO

from scoap3.common.repository import IRepository
from pytest import fixture, raises


@fixture
def repo():
    return IRepository()


def test_find_all(repo):
    raises(NotImplementedError, repo.find_all)


def test_test_find_by_id(repo):
    raises(NotImplementedError, repo.get_by_id, id="")


def test_save(repo):
    raises(NotImplementedError, repo.save, filename="", obj=BytesIO())


def test_delete_all(repo):
    raises(NotImplementedError, repo.delete_all)
