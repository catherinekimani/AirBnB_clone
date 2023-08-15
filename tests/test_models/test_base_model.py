#!/usr/bin/python3
"""Defines unittests for BaseModel"""
from models.base_model import BaseModel
from time import sleep
from datetime import datetime
import unittest
import models
import os


class TestBaseModel_instantiation(unittest.TestCase):
    """testing instantiation of the BaseModel class."""

    def test_no_args(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_created_at_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_id_is_public(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_updated_at_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_BaseModels_uuid(self):
        BaseM1 = BaseModel()
        BaseM2 = BaseModel()
        self.assertNotEqual(BaseM1.id, BaseM2.id)

    def test_two_BaseModels_diff_time(self):
        BaseM1 = BaseModel()
        sleep(0.05)
        BaseM2 = BaseModel()
        self.assertLess(BaseM1.created_at, BaseM2.created_at)

    def test_two_BaseModels_diff_time_update(self):
        BaseM1 = BaseModel()
        sleep(0.05)
        BaseM2 = BaseModel()
        self.assertLess(BaseM1.updated_at, BaseM2.updated_at)

    def test_unused_args(self):
        BaseM = BaseModel(None)
        self.assertNotIn(None, BaseM.__dict__.values())

    def test_instantce_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantce_with_kwargs(self):
        date_time = datetime.today()
        date_time_iso = date_time.isoformat()
        BaseM = BaseModel(id="345", created_at=date_time_iso,
                          updated_at=date_time_iso)
        self.assertEqual(BaseM.id, "345")
        self.assertEqual(BaseM.created_at, date_time)
        self.assertEqual(BaseM.updated_at, date_time)

    def test_string_representation(self):
        date_time = datetime.today()
        date_time_repr = repr(date_time)
        BaseM = BaseModel()
        BaseM.id = "123456"
        BaseM.created_at = BaseM.updated_at = date_time
        BaseModelstr = BaseM.__str__()
        self.assertIn("[BaseModel] (123456)", BaseModelstr)
        self.assertIn("'id': '123456'", BaseModelstr)
        self.assertIn("'created_at': " + date_time_repr, BaseModelstr)
        self.assertIn("'updated_at': " + date_time_repr, BaseModelstr)


class TestBaseModel_save(unittest.TestCase):
    """testing save method of the BaseModel."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_save(self):
        BaseM = BaseModel()
        sleep(0.05)
        first_updated_at = BaseM.updated_at
        BaseM.save()
        self.assertLess(first_updated_at, BaseM.updated_at)

    def test_double_saves(self):
        BaseM = BaseModel()
        sleep(0.05)
        first_updated_at = BaseM.updated_at
        BaseM.save()
        second_updated_at = BaseM.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        BaseM.save()
        self.assertLess(second_updated_at, BaseM.updated_at)

    def test_save_args(self):
        BaseM = BaseModel()
        with self.assertRaises(TypeError):
            BaseM.save(None)

    def test_save_update_file(self):
        BaseM = BaseModel()
        BaseM.save()
        BaseMid = "BaseModel." + BaseM.id
        with open("file.json", "r") as fd:
            self.assertIn(BaseMid, fd.read())


class TestBaseModel_to_dict(unittest.TestCase):
    """testing to_dict method of the BaseModel class."""

    def test_dict_type(self):
        self.assertTrue(dict, type(BaseModel().to_dict()))

    def test_dict_with_correct_keys(self):
        BaseM = BaseModel()
        self.assertIn("id", BaseM.to_dict())
        self.assertIn("created_at", BaseM.to_dict())
        self.assertIn("updated_at", BaseM.to_dict())
        self.assertIn("__class__", BaseM.to_dict())

    def test_dict_with_added_attributes(self):
        BaseM = BaseModel()
        BaseM.middle_name = "School"
        BaseM.my_number = 89
        self.assertEqual("School", BaseM.middle_name)
        self.assertIn("my_number", BaseM.to_dict())

    def test_dict_datetime_att_str(self):
        BaseM = BaseModel()
        BaseM_dict = BaseM.to_dict()
        self.assertEqual(str, type(BaseM_dict["id"]))
        self.assertEqual(str, type(BaseM_dict["created_at"]))
        self.assertEqual(str, type(BaseM_dict["updated_at"]))

    def test_dict_output(self):
        date_time = datetime.today()
        BaseM = BaseModel()
        BaseM.id = "123456"
        BaseM.created_at = BaseM.updated_at = date_time
        todict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': date_time.isoformat(),
            'updated_at': date_time.isoformat(),
        }
        self.assertDictEqual(BaseM.to_dict(), todict)

    def test_diff_to_dict(self):
        BaseM = BaseModel()
        self.assertNotEqual(BaseM.to_dict(), BaseM.__dict__)

    def test_to_dict_with_args(self):
        BaseM = BaseModel()
        with self.assertRaises(TypeError):
            BaseM.to_dict(None)


if __name__ == "__main__":
    unittest.main()
