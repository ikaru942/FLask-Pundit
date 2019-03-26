from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.search import add_to_index, remove_from_index, query_index


class User(UserMixin, db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    password = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(100), index=True, unique=True)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password(password)

    def check_password(self, password):
        return check_password(password)

class SearchableMixin(object):
    @classmethod
    def search(email_id):
        email = query_index(cls.__tablename__, email)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.email_id.in_(ids)).order_by(
            db.case(when, value=cls.email_id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'Add': list(session.new),
            'Update': list(session.dirty),
            'Delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['Add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['Update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['Delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


@login.user_loader
def load_user(id):
    return user.query.get(int(email_id))
