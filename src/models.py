from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Category(Base):
    __tablename__ = 'Category'

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(255), nullable=False)
    content_id = Column(ForeignKey('Content.content_id'), nullable=False)
    parent_id = Column(ForeignKey('Category.category_id'), nullable=False)

    content = relationship('Content', primaryjoin='Category.content_id == Content.content_id', backref='categories')
    parent = relationship('Category', remote_side=[category_id], primaryjoin='Category.parent_id == Category.category_id', backref='categories')


class Content(Base):
    __tablename__ = 'Content'

    content_id = Column(Integer, primary_key=True)
    data = Column(Text, nullable=False)
    title = Column(String(255), nullable=False)
    last_edited = Column(DateTime, nullable=False)
    last_edited_by = Column(String(255), nullable=False)
    owner_id = Column(ForeignKey('User.user_id'), nullable=False)
    tag_id = Column(ForeignKey('Tag.tag_id'), nullable=False)
    content_metadata_id = Column(ForeignKey('ContentMetadata.metadata_id'), nullable=False)

    content_metadata = relationship('ContentMetadatum', primaryjoin='Content.content_metadata_id == ContentMetadatum.metadata_id', backref='contents')
    owner = relationship('User', primaryjoin='Content.owner_id == User.user_id', backref='contents')
    tag = relationship('Tag', primaryjoin='Content.tag_id == Tag.tag_id', backref='contents')


class ContentMetadatum(Base):
    __tablename__ = 'ContentMetadata'

    metadata_id = Column(Integer, primary_key=True)
    content_metadata = Column(Text, nullable=False)


class Role(Base):
    __tablename__ = 'Role'

    role_id = Column(Integer, primary_key=True)
    role_name = Column(String(20), nullable=False)
    permission = Column(Integer, nullable=False)


class Tag(Base):
    __tablename__ = 'Tag'

    tag_id = Column(Integer, primary_key=True)
    tag_name = Column(String(255), nullable=False)


class User(Base):
    __tablename__ = 'User'

    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role_id = Column(ForeignKey('Role.role_id'), nullable=False)

    role = relationship('Role', primaryjoin='User.role_id == Role.role_id', backref='users')