import os
import re
import traceback

import paramiko
from scoap3.common.exceptions import DirectoryNotFoundException, NotConnectedException
from scoap3.common.utils import append_not_excluded_files, walk_sftp
from structlog import get_logger


class SFTPService:
    def __init__(
        self,
        host="localhost",
        username="airflow",
        password="airflow",
        port=2222,
        dir="/upload",
    ):
        self.connection = None
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.logger = get_logger().bind(class_name=type(self).__name__)
        self.dir = dir

    def __connect(self):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            banner_timeout=200,
            hostname=self.host,
            username=self.username,
            password=self.password,
            port=self.port,
        )
        connection = client.open_sftp()
        try:
            connection.stat(self.dir)
        except FileNotFoundError:
            raise DirectoryNotFoundException(
                "Remote directory doesn't exist. Abort connection."
            )
        return connection

    def __enter__(self):
        self.connection = self.__connect()
        return self

    def __exit__(self, exception_type, exception_value, tb):
        if self.connection:
            self.connection.close()
        if exception_type is not None:
            formed_exception = traceback.format_exception_only(
                exception_type, exception_value
            )
            self.logger.error(
                "An error occurred while exiting SFTPService",
                execption=formed_exception,
            )
            return False
        return True

    def list_files(self, excluded_directories=None):
        try:
            file_names = []
            filtered_files = []
            walk_sftp(sftp=self.connection, remotedir=self.dir, paths=file_names)
            for file_name in file_names:
                append_not_excluded_files(
                    re.sub(self.dir + "/", "", file_name),
                    excluded_directories,
                    filtered_files,
                )
            return filtered_files
        except AttributeError:
            raise NotConnectedException

    def get_file(self, file):
        try:
            file_ = self.connection.open(os.path.join(self.dir, file))
            file_.prefetch()
            return file_
        except AttributeError:
            raise NotConnectedException
