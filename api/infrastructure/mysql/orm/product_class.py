# coding: utf-8
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.mysql import INTEGER, LONGTEXT, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class ProductClass(Base):
    __tablename__ = 'product_class'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(LONGTEXT, nullable=False)
    active = Column(TINYINT(1), nullable=False)
    created = Column(DateTime, nullable=False)
