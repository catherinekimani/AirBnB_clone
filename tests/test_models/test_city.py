#!/usr/bin/python3
"""Defines unittests for The City"""
from models.city import City
from time import sleep
from datetime import datetime
import unittest
import models
import os


class TestCity_instantiation(unittest.TestCase):
    """testing instantiation of the City class."""

    def test_no_args(self):
        self.assertEqual(City, type(City()))

    def test_new_instance(self):
        self.assertIn(City(), models.storage.all().values())

    def test_created_at_datetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_id_is_public(self):
        self.assertEqual(str, type(City().id))

    def test_updated_at_datetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_name_attribute(self):
        cty = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(cty))
        self.assertNotIn("name", cty.__dict__)

    def test_state_id_attribute(self):
        cty = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(cty))
        self.assertNotIn("state_id", cty.__dict__)

    def test_two_cities_uuid(self):
        cty1 = City()
        cty2 = City()
        self.assertNotEqual(cty1.id, cty2.id)

    def test_two_cities_diff_time(self):
        cty1 = City()
        sleep(0.05)
        cty2 = City()
        self.assertLess(cty1.created_at, cty2.created_at)

    def test_two_cities_diff_time_update(self):
        cty1 = City()
        sleep(0.05)
        cty2 = City()
        self.assertLess(cty1.updated_at, cty2.updated_at)

    def test_unused_args(self):
        cty = City(None)
        self.assertNotIn(None, cty.__dict__.values())

    def test_instantce_None_kwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)

    def test_instantce_with_kwargs(self):
        date_time = datetime.today()
        date_time_iso = date_time.isoformat()
        cty = City(id="345", created_at=date_time_iso,
                   updated_at=date_time_iso)
        self.assertEqual(cty.id, "345")
        self.assertEqual(cty.created_at, date_time)
        self.assertEqual(cty.updated_at, date_time)

    def test_string_representation(self):
        date_time = datetime.today()
        date_time_repr = repr(date_time)
        cty = City()
        cty.id = "123456"
        cty.created_at = cty.updated_at = date_time
        ctystr = cty.__str__()
        self.assertIn("[City] (123456)", ctystr)
        self.assertIn("'id': '123456'", ctystr)
        self.assertIn("'created_at': " + date_time_repr, ctystr)
        self.assertIn("'updated_at': " + date_time_repr, ctystr)


class TestCity_save(unittest.TestCase):
    """testing save method of the  city."""

    @classmethod
    def set_up(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tear_down(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_save(self):
        cty = City()
        sleep(0.05)
        first_updated_at = cty.updated_at
        cty.save()
        self.assertLess(first_updated_at, cty.updated_at)

    def test_double_saves(self):
        cty = City()
        sleep(0.05)
        first_updated_at = cty.updated_at
        cty.save()
        second_updated_at = cty.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        cty.save()
        self.assertLess(second_updated_at, cty.updated_at)

    def test_save_args(self):
        cty = City()
        with self.assertRaises(TypeError):
            cty.save(None)

    def test_save_update_file(self):
        cty = City()
        cty.save()
        ctyid = "City." + cty.id
        with open("file.json", "r") as fd:
            self.assertIn(ctyid, fd.read())


class TestCity_to_dict(unittest.TestCase):
    """testing to_dict method of the City class."""

    def test_dict_type(self):
        self.assertTrue(dict, type(City().to_dict()))

    def test_dict_with_correct_keys(self):
        cty = City()
        self.assertIn("id", cty.to_dict())
        self.assertIn("created_at", cty.to_dict())
        self.assertIn("updated_at", cty.to_dict())
        self.assertIn("__class__", cty.to_dict())

    def test_dict_with_added_attributes(self):
        cty = City()
        cty.middle_name = "School"
        cty.my_number = 89
        self.assertEqual("School", cty.middle_name)
        self.assertIn("my_number", cty.to_dict())

    def test_dict_datetime_att_str(self):
        cty = City()
        cty_dict = cty.to_dict()
        self.assertEqual(str, type(cty_dict["id"]))
        self.assertEqual(str, type(cty_dict["created_at"]))
        self.assertEqual(str, type(cty_dict["updated_at"]))

    def test_dict_output(self):
        date_time = datetime.today()
        cty = City()
        cty.id = "123456"
        cty.created_at = cty.updated_at = date_time
        todict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': date_time.isoformat(),
            'updated_at': date_time.isoformat(),
        }
        self.assertDictEqual(cty.to_dict(), todict)

    def test_diff_to_dict(self):
        cty = City()
        self.assertNotEqual(cty.to_dict(), cty.__dict__)

    def test_to_dict_with_args(self):
        cty = City()
        with self.assertRaises(TypeError):
            cty.to_dict(None)


if __name__ == "__main__":
    unittest.main()
