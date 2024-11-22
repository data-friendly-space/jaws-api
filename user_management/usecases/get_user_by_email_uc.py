class GetUserByEmailUC:
    _instance = None

    def __init__(self):
        if GetUserByEmailUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            GetUserByEmailUC._instance = self

    @staticmethod
    def get_instance():
        if GetUserByEmailUC._instance is None:
            GetUserByEmailUC()
        return GetUserByEmailUC._instance

    def exec(self, repository, email):
        return repository.get_user_by_email(email)
