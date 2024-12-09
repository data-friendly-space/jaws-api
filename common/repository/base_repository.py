from abc import abstractmethod, ABC

from common.helpers.query_options import QueryOptions


class BaseRepository(ABC):
    @abstractmethod
    def get_all(self,query_options: QueryOptions):
        """
        Retrieve all records from the database.
        """
        pass

    @abstractmethod
    def get_by_id(self, obj_id):
        """
        Retrieve a single record by ID.
        """
        pass

    @abstractmethod
    def delete_by_id(self, obj_id):
        """
        Delete a record by ID.
        """
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """
        Update a record by ID.
        """

        pass

    @abstractmethod
    def create(self, data):
        """
        Add a new record to the database.
        """
        pass
