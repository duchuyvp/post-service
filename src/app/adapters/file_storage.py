"""
This module contains the AbstractRepository class and its subclasses.
"""

import abc
import datetime
import typing as t

import minio


class AbstractFileStorage(abc.ABC):
    def __init__(self):
        """
        Initialize the AbstractFileStorage class.
        """

    def add(self, f) -> None:
        """
        Add a file to the FileStorage.
        """
        self._add(f)

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
    def _add(self, f):
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
    def _edit(self, path: str, f):
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
    def __init__(self):
        """
        Initialize the MinIOFileStorage class.
        """
        self.instance = None
        super().__init__()

    def _add(self, f):
        """
        Add a file to the FileStorage.
        """
        raise NotImplementedError

    def _get(self, path: str):
        """
        Get a presigned URL from the FileStorage by path.
        """
        raise NotImplementedError

    def _edit(self, path: str, f):
        """
        Upload a replacement file to the FileStorage by path.
        """
        raise NotImplementedError

    def _delete(self, path: str):
        """
        Delete from the FileStorage by path.
        """
        raise NotImplementedError
