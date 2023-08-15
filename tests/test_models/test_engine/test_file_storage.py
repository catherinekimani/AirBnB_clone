#!/usr/bin/python3
"""Defines unittests for File Storage"""
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review
from time import sleep
from datetime import datetime
import unittest
import models
import os
import json


class TestFileStorage_instantiation(unittest.TestCase):
    """testing instantiation of the FileStorage class."""

    def test_FileStorage_instantce_no_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_instantce_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_file_path_str(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def testFileStorage_objects_dict(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_Filestorage_initialize(self):
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorage_methods(unittest.TestCase):
    """testing methods of the FileStorage class."""

    @classmethod
    def set_up(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tear_down(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all_no_args(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new_object(self):
        base_m = BaseModel()
        usr = User()
        new_st = State()
        plc = Place()
        cty = City()
        amty = Amenity()
        new_rv = Review()
        models.storage.new(base_m)
        models.storage.new(usr)
        models.storage.new(new_st)
        models.storage.new(plc)
        models.storage.new(cty)
        models.storage.new(amty)
        models.storage.new(new_rv)
        self.assertIn("BaseModel." + base_m.id, models.storage.all().keys())
        self.assertIn(base_m, models.storage.all().values())
        self.assertIn("User." + usr.id, models.storage.all().keys())
        self.assertIn(usr, models.storage.all().values())
        self.assertIn("State." + new_st.id, models.storage.all().keys())
        self.assertIn(new_st, models.storage.all().values())
        self.assertIn("Place." + plc.id, models.storage.all().keys())
        self.assertIn(plc, models.storage.all().values())
        self.assertIn("City." + cty.id, models.storage.all().keys())
        self.assertIn(cty, models.storage.all().values())
        self.assertIn("Amenity." + amty.id, models.storage.all().keys())
        self.assertIn(amty, models.storage.all().values())
        self.assertIn("Review." + new_rv.id, models.storage.all().keys())
        self.assertIn(new_rv, models.storage.all().values())

    def test_new_object_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_new_object_with_no_args(self):
        with self.assertRaises(AttributeError):
            models.storage.new(None)

    def test_save_no_args(self):
        base_m = BaseModel()
        usr = User()
        new_st = State()
        plc = Place()
        cty = City()
        amty = Amenity()
        new_rv = Review()
        models.storage.new(base_m)
        models.storage.new(usr)
        models.storage.new(new_st)
        models.storage.new(plc)
        models.storage.new(cty)
        models.storage.new(amty)
        models.storage.new(new_rv)
        models.storage.save()
        save_txt = ""
        with open("file.json", "r") as fd:
            save_txt = fd.read()
            self.assertIn("BaseModel." + base_m.id, save_txt)
            self.assertIn("User." + usr.id, save_txt)
            self.assertIn("State." + new_st.id, save_txt)
            self.assertIn("Place." + plc.id, save_txt)
            self.assertIn("City." + cty.id, save_txt)
            self.assertIn("Amenity." + amty.id, save_txt)
            self.assertIn("Review." + new_rv.id, save_txt)

    def test_save_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        base_m = BaseModel()
        usr = User()
        new_st = State()
        plc = Place()
        cty = City()
        amty = Amenity()
        new_rv = Review()
        models.storage.new(base_m)
        models.storage.new(usr)
        models.storage.new(new_st)
        models.storage.new(plc)
        models.storage.new(cty)
        models.storage.new(amty)
        models.storage.new(new_rv)
        models.storage.save()
        models.storage.reload()
        new_obj = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + base_m.id, new_obj)
        self.assertIn("User." + usr.id, new_obj)
        self.assertIn("State." + new_st.id, new_obj)
        self.assertIn("Place." + plc.id, new_obj)
        self.assertIn("City." + cty.id, new_obj)
        self.assertIn("Amenity." + amty.id, new_obj)
        self.assertIn("Review." + new_rv.id, new_obj)

    def test_reload_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
