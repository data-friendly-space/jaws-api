class SignInUC:
    _instance = None

    def __init__(self):
        if SignInUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            SignInUC._instance = self

    @staticmethod
    def get_instance():
        if SignInUC._instance is None:
            SignInUC()
        return SignInUC._instance

    def exec(self, repository,data):
        return repository.sign_up(data)
