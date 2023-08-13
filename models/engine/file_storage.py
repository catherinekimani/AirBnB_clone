#!/usr/bin/python3
"""Define FileStorage Class"""
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
import json


class FileStorage:
    """Represents storagr engine"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects obj with key"""
        obj_name = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(obj_name, obj.id)] = obj

    def save(self):
        """ Serializes __objects to the JSON file """
        new_dict = FileStorage.__objects
        obj_dict = {obj: new_dict[obj].to_dict() for obj in new_dict.keys()}
        with open(FileStorage.__file_path, "w") as fd:
            json.dump(obj_dict, fd)

    def reload(self):
        """Deserializes the JSON file to __objects(If it exixts)
        Otherwise do nothing
        """
        try:
            with open(FileStorage.__file_path) as fd:
                obj_dict = json.load(fd)
                for ob in obj_dict.values():
                    cls_name = ob["__class__"]
                    del ob["__class__"]
                    self.new(eval(cls_name)(**ob))
        except FileNotFoundError:
            return
