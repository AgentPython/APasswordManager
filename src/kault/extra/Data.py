from .base import ExtraBase

from sqlalchemy import Column, Integer, String


class DataModel(ExtraBase):
    __tablename__ = 'export_result'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)
    login = Column(String)
    password = Column(String)
    notes = Column(String)
    category = Column(String)

    def __init__(self, id, name, url='', login='', password='', notes='', category=''):
        # Set class level vars
        self.id = id
        self.name = name
        self.url = url
        self.login = login
        self.password = password
        self.notes = notes
        self.category = category

    def __repr__(self):
        return f"<DataModel(id='{self.id}', name='{self.name}', url='{self.url}', login='{self.login}', password='{self.password}', notes='{self.notes}', category='{self.category}')>" 
