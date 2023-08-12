#!/usr/bin/python3
"""Defines unittests for Amenity"""
from models.amenity import Amenity
from time import sleep
from datetime import datetime
import unittest
import models
import os


class TestAmenity_instantiation(unittest.TestCase):
    """testing instantiation of the Amenity class."""

    def test_no_args(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_new_instance(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_created_at_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_id_is_public(self):
        self.assertEqual(str, type(Amenity().id))

    def test_updated_at_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_name_attribute(self):
        amt = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(amt))
        self.assertNotIn("name", amt.__dict__)

    def test_two_amenities_uuid(self):
        amt1 = Amenity()
        amt2 = Amenity()
        self.assertNotEqual(amt1.id, amt2.id)

    def test_two_amenities_diff_time(self):
        amt1 = Amenity()
        sleep(0.05)
        amt2 = Amenity()
        self.assertLess(amt1.created_at, amt2.created_at)

    def test_two_amenites_diff_time_update(self):
        amt1 = Amenity()
        sleep(0.05)
        amt2 = Amenity()
        self.assertLess(amt1.updated_at, amt2.updated_at)

    def test_unused_args(self):
        amt = Amenity(None)
        self.assertNotIn(None, amt.__dict__.values())

    def test_instantce_None_kwargs(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)

    def test_instantce_with_kwargs(self):
        date_time = datetime.today()
        date_time_iso = date_time.isoformat()
        amt = Amenity(id="345", created_at=date_time_iso, updated_at=date_time_iso)
        self.assertEqual(amt.id, "345")
        self.assertEqual(amt.created_at, date_time)
        self.assertEqual(amt.updated_at, date_time)

    def test_string_representation(self):
        date_time = datetime.today()
        date_time_repr = repr(date_time)
        amt = Amenity()
        amt.id = "123456"
        amt.created_at = amt.updated_at = date_time
        amtstr = amt.__str__()
        self.assertIn("[Amenity] (123456)", amtstr)
        self.assertIn("'id': '123456'", amtstr)
        self.assertIn("'created_at': " + date_time_repr, amtstr)
        self.assertIn("'updated_at': " + date_time_repr, amtstr)

class TestAmenity_save(unittest.TestCase):
    """testing save method of the  state."""

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
        amt = Amenity()
        sleep(0.05)
        first_updated_at = amt.updated_at
        amt.save()
        self.assertLess(first_updated_at, amt.updated_at)

    def test_double_saves(self):
        amt = Amenity()
        sleep(0.05)
        first_updated_at = amt.updated_at
        amt.save()
        second_updated_at = amt.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        amt.save()
        self.assertLess(second_updated_at, amt.updated_at)

    def test_save_args(self):
        amt = Amenity()
        with self.assertRaises(TypeError):
            amt.save(None)

    def test_save_update_file(self):
        amt = Amenity()
        amt.save()
        amtid = "Amenity." + amt.id
        with open("file.json", "r") as fd:
            self.assertIn(amtid, fd.read())


class TestAmenity_to_dict(unittest.TestCase):
    """testing to_dict method of the Amenity class."""

    def test_dict_type(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_dict_with_correct_keys(self):
        amt = Amenity()
        self.assertIn("id", amt.to_dict())
        self.assertIn("created_at", amt.to_dict())
        self.assertIn("updated_at", amt.to_dict())
        self.assertIn("__class__", amt.to_dict())

    def test_dict_with_added_attributes(self):
        amt = Amenity()
        amt.middle_name = "School"
        amt.my_number = 89
        self.assertEqual("School", amt.middle_name)
        self.assertIn("my_number", amt.to_dict())

    def test_dict_datetime_att_str(self):
        amt = Amenity()
        amt_dict = amt.to_dict()
        self.assertEqual(str, type(amt_dict["id"]))
        self.assertEqual(str, type(amt_dict["created_at"]))
        self.assertEqual(str, type(amt_dict["updated_at"]))

    def test_dict_output(self):
        date_time = datetime.today()
        amt = Amenity()
        amt.id = "123456"
        amt.created_at = amt.updated_at = date_time
        todict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': date_time.isoformat(),
            'updated_at': date_time.isoformat(),
        }
        self.assertDictEqual(amt.to_dict(), todict)

    def test_diff_to_dict(self):
        amt = Amenity()
        self.assertNotEqual(amt.to_dict(), amt.__dict__)

    def test_to_dict_with_args(self):
        amt = Amenity()
        with self.assertRaises(TypeError):
            amt.to_dict(None)


if __name__ == "__main__":
    unittest.main()
