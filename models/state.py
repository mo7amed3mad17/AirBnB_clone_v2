#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from models.city import City


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    cities = relationship("City", backref="state", cascade="all, delete")

    @property
    def cities(self):
        var = models.storage.all()
        lista = []
        result = []
        for key in var:
            city = key.replace('.', ' ')
            city = shlex.split(city)
            if city[0] == 'City':
                lista.append(var[key])
        for elem in lista:
            if elem.state_id == self.id:
                result.append(elem)
        return result
