"""
This module contains the AbstractRepository class and its subclasses.
"""

import abc
import datetime
import tempfile
import typing as t

import minio
import minio.helpers


class AbstractFileStorage(abc.ABC):
    def __init__(self):
        self.BUCKET_NAME = "posts"

        """
        Initialize the AbstractFileStorage class.
        """

    def add(self, path: str, f: tempfile.SpooledTemporaryFile, **kwargs) -> int:
        """
        Add a file to the FileStorage.
        """
        try:
            self._add(path, f, **kwargs)
        except Exception as e:
            return 1
        return 0

    def get(self, path: str) -> str:
        """
        Get a presigned URL from the FileStorage by path.
        """
        r = self._get(path)
        return r

    def edit(self, path: str, f) -> None:
        """
        Upload a replacement file to the FileStorage by path.
        """
        self._edit(path, f)

    def delete(self, path: str) -> None:
        """
        Delete from the FileStorage by path.
        """
        self._delete(path)

    @abc.abstractmethod
    def _add(self, path: str, f: tempfile.SpooledTemporaryFile, **kwargs):
        """
        Abstract method to add a file to the FileStorage.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, path: str):
        """
        Abstract method to get a presigned URL from the FileStorage by path.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _edit(self, path: str, f: tempfile.SpooledTemporaryFile):
        """
        Abstract method to upload a replacement file to the FileStorage by path.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _delete(self, path: str):
        """
        Abstract method to delete from the FileStorage by path.
        """
        raise NotImplementedError


class MinIOFileStorage(AbstractFileStorage):

    def __init__(self, client: minio.Minio):
        """
        Initialize the MinIOFileStorage class.
        """
        super().__init__()

        self.client = client
        if not self.client.bucket_exists(self.BUCKET_NAME):
            self.client.make_bucket(self.BUCKET_NAME)

    def _add(self, path: str, f: tempfile.SpooledTemporaryFile, **kwargs) -> int:
        """
        Add a file to the FileStorage.
        """
        self.client.put_object(
            bucket_name=self.BUCKET_NAME,
            object_name=path,
            data=f,
            length=f.tell(),
            **kwargs,
        )
        return 0

    def _get(self, path: str):
        """
        Get a presigned URL from the FileStorage by path.
        """
        raise NotImplementedError

    def _edit(self, path: str, f: tempfile.SpooledTemporaryFile):
        """
        Upload a replacement file to the FileStorage by path.
        """
        raise NotImplementedError

    def _delete(self, path: str):
        """
        Delete from the FileStorage by path.
        """
        raise NotImplementedError
