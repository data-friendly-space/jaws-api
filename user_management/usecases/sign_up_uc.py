class SignUpUC:
    _instance = None

    def __init__(self):
        if SignUpUC._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            SignUpUC._instance = self

    @staticmethod
    def get_instance():
        if SignUpUC._instance is None:
            SignUpUC()
        return SignUpUC._instance

    def exec(self, repository, name, lastname, email, password):
        return repository.sign_up(name, lastname, email, password)
