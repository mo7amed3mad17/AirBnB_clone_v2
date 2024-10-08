#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, DateTime
from datetime import datetime


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}



    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        super().__init__(*args)  # Call parent class constructor, if applicable

        if kwargs:

            # Ensure 'id' is always set, defaulting to a new UUID if missing
            self.id = kwargs.get('id', str(uuid.uuid4()))

            # Parse 'created_at' and 'updated_at' if provided, or set to now if missing
            kwargs['updated_at'] = datetime.strptime(
                kwargs.get('updated_at', datetime.now().isoformat()), 
                '%Y-%m-%dT%H:%M:%S.%f'
            )
            kwargs['created_at'] = datetime.strptime(
                kwargs.get('created_at', datetime.now().isoformat()), 
                '%Y-%m-%dT%H:%M:%S.%f'
            )
            # Remove the __class__ key if present
            if '__class__' in kwargs:
                del kwargs['__class__']
            # Update the instance's dictionary with the kwargs
            self.__dict__.update(kwargs)
        else:
            # If no kwargs, create a new instance with default values
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        """def __init__(self, *args, **kwargs):
        Instatntiates a new model
        super().__init__(*args)  # Call parent class constructor, if applicable

        for key, value in kwargs.items():
            if not hasattr(self, key):  # Check if attribute already exists
                setattr(self, key, value)  # Set attribute if it doesn't exist

        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                    datetime.now(), '%Y-%m-%dT%H:%M:%S.%f')
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                    datetime.now(), '%Y-%m-%dT%H:%M:%S.%f')
            del kwargs['__class__']
            self.__dict__.update(kwargs)"""

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)

        # Remove the _sa_instance_state key if it exists
        if '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']

        dictionary.update({
            '__class__': (str(type(self)).split('.')[-1]).split('\'')[0]
        })
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary

    def delete(self):
        """
            delete the current instance
        """
        models.storage.delete(self)
