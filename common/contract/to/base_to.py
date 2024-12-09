class BaseTO:

    @classmethod
    def from_models(self, models):
        """
        Transform a list of Workspace model instances into a list of WorkspaceTO instances.
        """
        return [self.from_model(model) for model in models]