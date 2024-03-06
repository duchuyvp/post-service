import abc

"""
This module contains the AbstractRepository class and its subclasses.
"""

import abc


class AbstractRepository(abc.ABC):
    def __init__(self):
        """
        Initialize the AbstractRepository class.
        """
        self.seen = set()

    def add(self, product):
        """
        Add a product to the repository.
        """
        self._add(product)
        self.seen.add(product)

    def get(self, sku):
        """
        Get a product from the repository by SKU.
        """
        product = self._get(sku)
        if product:
            self.seen.add(product)
        return product

    def get_by_batchref(self, batchref):
        """
        Get a product from the repository by batch reference.
        """
        product = self._get_by_batchref(batchref)
        if product:
            self.seen.add(product)
        return product

    @abc.abstractmethod
    def _add(self, product):
        """
        Abstract method to add a product to the repository.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, sku):
        """
        Abstract method to get a product from the repository by SKU.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_batchref(self, batchref):
        """
        Abstract method to get a product from the repository by batch reference.
        """
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        """
        Initialize the SqlAlchemyRepository class.
        """
        super().__init__()
        self.session = session

    def _add(self, product):
        """
        Add a product to the SQL Alchemy repository.
        """

    def _get(self, sku):
        """
        Get a product from the SQL Alchemy repository by SKU.
        """

    def _get_by_batchref(self, batchref):
        """
        Get a product from the SQL Alchemy repository by batch reference.
        """
