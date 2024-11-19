class GetUsersUc:
    _instance = None

    def __init__(self):
        if GetUsersUc._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetUsersUc._instance = self

    @staticmethod
    def get_instance():
        if GetUsersUc._instance is None:
            GetUsersUc()
        return GetUsersUc._instance

    def exec(self, repository):
        return repository.get_all()
