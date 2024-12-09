"""This module contains the base repository"""
from abc import abstractmethod, ABC


class BaseRepository(ABC):
    """Base repository"""
    @abstractmethod
    def get_all(self):
        """
        Retrieve all records from the database.
        """

    @abstractmethod
    def get_by_id(self, obj_id):
        """
        Retrieve a single record by ID.
        """


    def delete_by_id(self, obj_id):
        """
        Delete a record by ID.
        """


    def update(self, obj_id, data):
        """
        Update a record by ID.
        """


    @abstractmethod
    def create(self, data):
        """
        Add a new record to the database.
        """
