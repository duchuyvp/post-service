"""
This module contains the AbstractRepository class and its subclasses.
"""

import abc
import datetime
import io
import tempfile
import typing as t

import fastapi
import minio
import minio.helpers


class AbstractFileStorage(abc.ABC):
    def __init__(self):
        self.BUCKET_NAME = "posts"

        """
        Initialize the AbstractFileStorage class.
        """

    def add(self, path: str, f: fastapi.UploadFile, **kwargs) -> int:
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
    def _add(self, path: str, f: fastapi.UploadFile, **kwargs):
        """
        Abstract method to add a file to the FileStorage.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, path: str) -> str:
        """
        Abstract method to get a presigned URL from the FileStorage by path.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _edit(self, path: str, f: fastapi.UploadFile):
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

    def _add(self, path: str, f: fastapi.UploadFile, **kwargs) -> int:
        """
        Add a file to the FileStorage.
        """
        file_data = f.file.read()
        self.client.put_object(
            bucket_name=self.BUCKET_NAME,
            object_name=path,
            data=io.BytesIO(file_data),
            length=len(file_data),
            content_type=f.content_type,
        )
        return 0

    def _get(self, path: str) -> str:
        """
        Get a presigned URL from the FileStorage by path.
        """
        return self.client.presigned_get_object(self.BUCKET_NAME, path)

    def _edit(self, path: str, f: fastapi.UploadFile):
        """
        Upload a replacement file to the FileStorage by path.
        """
        raise NotImplementedError

    def _delete(self, path: str):
        """
        Delete from the FileStorage by path.
        """
        raise NotImplementedError
