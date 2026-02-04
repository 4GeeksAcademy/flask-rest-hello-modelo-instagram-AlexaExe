from flask_sqlalchemy import SQLAlchemy #importa la librería SQLAlchemy para que Flask conecte 
#con una base de datos.
from sqlalchemy import String, Boolean, ForeignKey, Table, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship  #esto es para declarar columnas en SQLAlchemy versión 2.0.
from eralchemy2 import render_er #para cambiar el diagrama porque no aparecía más que el de base

db = SQLAlchemy() #para conectar con el appy gestionar la base de datos

#En caso de que la tabla se llame diferente el nombre de la clase colocar >>" __tablename__ = 'users'"

# TABLAS INTERMEDIAS DE FOLLOWER

followers = Table(
    'followers',
    db.metadata,   #aqui ya llamo a db            
    Column('user_from_id', db.Integer, ForeignKey('user.id'), primary_key=True), #seguidor
    Column('user_to_id', db.Integer, ForeignKey('user.id'),primary_key=True), #seguido

)



class User(db.Model): #representa mi tabla user de mi base de datos
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False) #yo he agregado esto como en el ejemplo
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    # relacion con followers, siguiendo lo anterior del diagrama
    following = db.relationship (
        'User',
        secondary=followers,
        primaryjoin=(id == followers.c.user_from_id),
        secondaryjoin=(id == followers.c.user_to_id),
        backref='followers'      
        # agrego backref para tambipen poder acceder a quienes "siguen"
    )
  
    posts = db.relationship("Post", backref="author", lazy=True)


    def serialize(self): #método    
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Post(db.Model):#representa mi tabla Posts(publicaciones) de mi base de datos
    __tablename__ = 'post'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False) #este dato pertenece a otro que ya existe en otra tabla
    
    #Relación con comentarios y media, usando backref
    comments = relationship("Comment", backref="post", lazy=True)
    media = relationship("Media", backref="post", lazy=True)
    # esto es para que poder acceder desde comment a post y desde media a post.


    def serialize(self): #método    
        return {
            "id": self.id,
            "user_id": self.user_id,
        }
    


class Comment(db.Model):#representa mi tabla Coment(comentarios) de mi base de datos
    __tablename__ = 'comment'

    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(500), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False) #porque está relacionada con el "USUARIO" quién realizó el post
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False) #porque está relacionada con el número de post


    def serialize(self): #método    
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id
        }



class Media (db.Model): #representa mi tabla Media de mi base de datos
    __tablename__ = 'media'
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(200), nullable=False) #texto
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False) #porque va a buscar en otra table el post id
    

    def serialize(self): #método    
        return {
            "id": self.id,
            "url": self.url,
            "post_id": self.post_id,
        }

#para generar el diagrama... 
render_er(db.Model.metadata, 'diagram.png')