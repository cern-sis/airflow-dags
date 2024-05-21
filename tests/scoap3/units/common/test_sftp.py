from unittest.mock import patch

from scoap3.common.sftp_service import DirectoryNotFoundException, SFTPService
from paramiko import SFTPClient
from pytest import raises


def test_connect():
    def initiate_sftp_service():
        with SFTPService() as sftp:
            return sftp

    assert initiate_sftp_service() is not None


@patch.object(SFTPClient, attribute="stat", side_effect=FileNotFoundError)
def test_connect_should_crash(connection_mock, *args):
    def initiate_sftp_service():
        with SFTPService():
            pass

    raises(DirectoryNotFoundException, initiate_sftp_service)


def test_error_raise():
    with raises(Exception):
        with SFTPService():
            raise Exception
