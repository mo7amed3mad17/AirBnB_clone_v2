#!/usr/bin/python3
""" DataBase Storage """
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """Interacts with the MySQL database via SQLAlchemy."""

    __engine = None
    __session = None

    def __init__(self):
        """Initialize the engine and link it to the MySQL database."""
        user = os.getenv('HBNB_MYSQL_USER')
        pwd = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST', 'localhost')
        db = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')

        # Create engine
        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{pwd}@{host}/{db}',
            pool_pre_ping=True)

        # Drop all tables if in test environment
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session."""
        if isinstance(cls, str):
            # Map the string to the actual class
            cls = {
                "State": State,
                "City": City,
                # Add other mappings as needed
            }.get(cls, None)

        if cls:
            query_results = self.__session.query(cls).all()
        else:
            query_results = self.__session.query(State).all()  # Example default query
        return {obj.id: obj for obj in query_results}
        """ def all(self, cls=None):
        Query the current database session.
        objects = {}
        if cls:
            query_results = self.__session.query(cls).all()
            for obj in query_results:
                key = f"{obj.__class__.__name__}.{obj.id}"
                objects[key] = obj
        else:
            for class_type in [User, State, City, Amenity, Place, Review]:
                query_results = self.__session.query(class_type).all()
                for obj in query_results:
                    key = f"{obj.__class__.__name__}.{obj.id}"
                    objects[key] = obj
        return objects"""

    def new(self, obj):
        """Add the object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete the object from the current database session."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and initialize a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        self.__session.close()
