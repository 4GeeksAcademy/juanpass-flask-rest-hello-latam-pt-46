from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    
    posts = relationship('Post', backref='user', lazy=True)
    comments = relationship('Comments', backref='author', lazy=True)
    profile = relationship('Profile', backref='user', uselist=False)
    followers = relationship('Followers', backref='user', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class Profile(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    nombre: Mapped[str] = mapped_column(String(255))
    correo: Mapped[str] = mapped_column(String(255))
    foto: Mapped[bytes] = mapped_column(nullable=True) # Puede ser un blob
    posts: Mapped[int] = mapped_column(Integer, nullable=True)
    followers: Mapped[int] = mapped_column(Integer, nullable=True)
    followed: Mapped[int] = mapped_column(Integer, nullable=True)
    thread: Mapped[str] = mapped_column(Text, nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "correo": self.correo,
        }

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    apellidos: Mapped[str] = mapped_column(String(255), nullable=True)
    telefono: Mapped[int] = mapped_column(nullable=True)

    media = relationship('Media', backref='post', lazy=True)
    comments = relationship('Comments', backref='post', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
        }

class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(Enum('image', 'video', name='media_types'))
    url: Mapped[str] = mapped_column(String(255))
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
        }

class Comments(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(Text)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'))

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
        }

class Followers(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
        }
