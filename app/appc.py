from flask_pundit.application_policy import ApplicationPolicy

class PostPolicy(ApplicationPolicy):
        def get(self):
                return self.user == 'admin' and self.record.id == 1


        def scope(self):
                if self.user == 'admin':
                        return record.all()
                return record.filter_by(author='staff')
