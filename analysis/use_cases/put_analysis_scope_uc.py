class PutAnalysisScopeUc:
    _instance = None

    def __init__(self):
        if PutAnalysisScopeUc._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            PutAnalysisScopeUc._instance = self

    @staticmethod
    def get_instance():
        if PutAnalysisScopeUc._instance is None:
            PutAnalysisScopeUc()
        return PutAnalysisScopeUc._instance

    def exec(self, repository):
        return repository.update()
