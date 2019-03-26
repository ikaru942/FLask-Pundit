class ApplicationPolicy:
    '''Base class for all policy'''
    def __init__(self, user, record):
        self.user = user
        self.record = record

    def get(self):
        return self.user == 'admin' and self.post.id == 1
