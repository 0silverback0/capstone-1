from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

class Follows(db.Model):
    """table for  user followers/following """

    __tablename__ = 'follows'

    user_followed_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True,
    )

    user_following_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True,
    )

class Likes(db.Model):
    """ add a like to post """

    __tablename__ = 'likes' 

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    post_id = db.Column(
        db.Integer,
        db.ForeignKey('post.id', ondelete='cascade')
    )

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.Text, default='https://bit.ly/2WBaPjg')

    following = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_following_id == id),
        secondaryjoin=(Follows.user_followed_id == id)
    )
    followers = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_followed_id == id),
        secondaryjoin=(Follows.user_following_id == id)
    )

    post = db.relationship('Post', passive_deletes=True)
    likes = db.relationship('Post', secondary="likes")

    @classmethod
    def signup(cls, username, password, img_url):
        """ signup user, hashes password and adds user to database """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
            img_url=img_url
        )

        db.session.add(user)
        return user

    @classmethod
    def login(cls, username, password):
        """ check password hash against password and logs in user """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Post(db.Model):
    """ post model """

    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    user = db.relationship('User')
    
class Artist(db.Model):
    """ Artist Model """

    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    artist_id = db.Column(db.Integer, nullable=False, unique=True)
    img_url = db.Column(db.Text, default='https://bit.ly/2WBaPjg')

