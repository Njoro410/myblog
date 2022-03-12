from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    pass_secure = db.Column(db.String(255))
    about = db.Column(db.STring(255))
    profile_pic_path = db.Column(db.String())
    posts = db.relagionship('Posts', backref='user', lazy='dynamic')
    comments = db.relationship('Comments', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure, password)

    def __repr__(self):
        return f'User {self.firstname}'


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return f'User {self.name}'


class Categories(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15))
    posts = db.relationship('Posts', backref='categories', lazy="dynamic")

    def __repr__(self):
        return f'User {self.name}'


class Posts(db.Model):
    __tablename__ = 'posts'

    id = db.COlumn(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    sub_title = db.Column(db.String(255))
    content = db.Column9db.String(255)
    posted = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    categories_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    comments = db.relationship('Comments', backref='posts', lazy="dynamic")

    def __repr__(self):
        return f'User {self.content}'

    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_posts(cls):
        posts = Posts.query.all()
        return posts
    
class Comments(db.Model):
    __tablename__ = 'comments'
    
    id = db.column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_id = db.Colum(db.Intger, db.ForeignKey("posts.id"))
    
    def __repr__(self):
        return f'User {self.comment}'
    
    def save_comment(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_comments(cls, id):
        comments = Comments.query.filter_by(post_id=id).all()
        return comments