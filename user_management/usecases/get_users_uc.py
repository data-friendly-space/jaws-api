class GetUsersUC:
    _instance = None

    def __init__(self):
        if GetUsersUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetUsersUC._instance = self

    @staticmethod
    def get_instance():
        if GetUsersUC._instance is None:
            GetUsersUC()
        return GetUsersUC._instance

    def exec(self, repository):
        return repository.get_all()
