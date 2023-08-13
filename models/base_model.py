#!usr/bin/python3
"""BaseModel Class"""

import uuid
from datetime import datetime
import models


class BaseModel:
    """Respresent BaseModel"""
    def __init__(self, *args, **kwargs):
        """Initialize new BaseModel
        Args:
            *args (any) Unused
            **kwargs (dictionary): K/V pairs
        """
        time = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid.uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()

        if len(kwargs) != 0:
            for key, val in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    self.__dict__[key] = datetime.strptime(val, time)
                else:
                    self.__dict__[key] = val
        else:
            models.storage.new(self)

    def save(self):
        """Update update_at with current date."""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """Returns dictionary containing all keys/values of __dict__"""
        newdict = self.__dict__.copy()
        newdict["created_at"] = self.created_at.isoformat()
        newdict["updated_at"] = self.updated_at.isoformat()
        newdict["__class__"] = self.__class__.__name__
        return newdict

    def __str__(self):
        """Print/str representation of BaseModel."""
        cls_name = self.__class__.__name__
        return "[{}] ({}) {}".format(cls_name, self.id, self.__dict__)
