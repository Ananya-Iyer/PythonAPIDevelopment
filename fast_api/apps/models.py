from .database import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

# whenever we launch our application it checks if the tablename exists if yes it wont do antyhing if not then it will create the table for us based 
# on the model we defined here

# SQLALCHEMY MODELS

# Post Table
class Post(Base):

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False) # creates a column id with datatype integer and sets it as primary key and not null
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    reference = Column(String, nullable=True)
    publish = Column(Boolean, server_default=text("true"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="cascade"), nullable=False) # ForeignKey Syntax: ForeignKey(TABLENAME, ACTION_ON_DELETE)

    # tells sql alchemy to automatically fetch some piece of info based off the 
    # it creates a owner property and figure out the relationship with User capital U bcuz we're not referencing the table but actual sql alchemy class
    owner = relationship("User")


# User Table
class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


class Vote(Base):

    __tablename__ = "votes"

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="cascade"), primary_key=True) # ForeignKey & PrimaryKey
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="cascade"), primary_key=True) # ForeignKey & PrimaryKey
