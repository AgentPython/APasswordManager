from sqlalchemy import Column, Integer, String

from .base import Base

class CategoryModel(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    active = Column(Integer, default=1)

    def __repr__(self):
        return f"<CategoryModel(id={self.id}, name={self.name}, active={self.active})"
