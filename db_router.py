class DBRouter:
    """
    A database router to control operations for user_management and analysis modules.
    """

    app_to_db = {
        'user_management': 'user_management_db',
        'analysis': 'analysis_db',
    }

    def db_for_read(self, model, **hints):
        """
        Direct read operations to the appropriate database.
        """
        return self.app_to_db.get(model._meta.app_label, 'default')

    def db_for_write(self, model, **hints):
        """
        Direct write operations to the appropriate database.
        """
        return self.app_to_db.get(model._meta.app_label, 'default')

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relationships only within the same database.
        """
        db_set = {self.app_to_db.get(obj1._meta.app_label, 'default'),
                  self.app_to_db.get(obj2._meta.app_label, 'default')}
        return len(db_set) == 1

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure that migrations occur only in the designated database.
        """
        return self.app_to_db.get(app_label) == db
