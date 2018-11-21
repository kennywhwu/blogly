"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

DEFAULT_IMG_URL = 'https://apprecs.org/ios/images/app-icons/256/f6/1014381046.jpg'
db = SQLAlchemy()


def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User model"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True)  # have to autoincrement?
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.Text, default=DEFAULT_IMG_URL)

    posts = db.relationship(
        'Post', backref='users', cascade='all, delete')
    # Why doesn't cascade work?

    @property
    def full_name(self):
        """Return full name of user"""
        return f'{self.first_name} {self.last_name}'


class Post(db.Model):
    """Post model"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    tags = db.relationship('Tag', secondary='posttag', backref='posts')

    @property
    def friendly_date(self):
        """Return friendly formatted date"""
        return self.created_at.strftime('%a %b %-d %Y, %-I:%M %p')
        # Datetime Explanation: https://linux.die.net/man/3/strftime


class Tag(db.Model):
    """Tag model"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)


class PostTag(db.Model):
    """PostTag model"""

    __tablename__ = 'posttag'

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), primary_key=True, )
    tag_id = db.Column(db.Integer, db.ForeignKey(
        'tags.id'), primary_key=True, )
