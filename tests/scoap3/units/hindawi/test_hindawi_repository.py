from io import BytesIO
from unittest.mock import patch

import pytest
from scoap3.hindawi.repository import HindawiRepository


class S3BucketResultObj:
    def __init__(self, key):
        self.key = key


S3_RETURNED_VALUES = ["file1.xml", "file2.xml"]
FIND_ALL_EXPECTED_VALUES = ["file1.xm", "file2.xml"]
expected_file = BytesIO()


@pytest.fixture(scope="function")
def boto3_fixture():
    with patch("scoap3.common.s3_service.boto3", autospec=True) as boto3_mock:
        boto3_mock.resource.return_value.Bucket.return_value.objects.all.return_value = [
            S3BucketResultObj(file) for file in S3_RETURNED_VALUES
        ]
        yield boto3_mock


def test_find_all(boto3_fixture):
    repo = HindawiRepository()
    assert repo.find_all() == S3_RETURNED_VALUES


def test_save_json_file(boto3_fixture):
    upload_mock = boto3_fixture.resource.return_value.Bucket.return_value.upload_fileobj
    key = "2022-01-01_00:00:00/test.xml"
    repo = HindawiRepository()
    repo.save(key, expected_file)
    upload_mock.assert_called_with(expected_file, key)


def test_find_by_id(boto3_fixture):
    repo = HindawiRepository()
    file = repo.get_by_id(id="1")
    assert isinstance(file, BytesIO)
