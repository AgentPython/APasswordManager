from .base import Base

from sqlalchemy import Column, Integer, String


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    key = Column(String)
    value = Column(String)

    def __repr__(self):
        return f"<UserModel(id='{self.id}', key='{self.key}', value='{self.value}')>"
