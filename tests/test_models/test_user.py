#!/usr/bin/python3
"""Defines unittests for user"""
from models.user import User
from time import sleep
from datetime import datetime
import unittest
import models
import os


class TestUser_instantiation(unittest.TestCase):
    """testing instantiation of the User class."""

    def test_no_args(self):
        self.assertEqual(User, type(User()))

    def test_new_instance(self):
        self.assertIn(User(), models.storage.all().values())

    def test_created_at_datetime(self):
        self.assertEqual(datetime, type(User().created_at))

    def test_id_is_public(self):
        self.assertEqual(str, type(User().id))

    def test_updated_at_datetime(self):
        self.assertEqual(datetime, type(User().updated_at))

    def test_email_str(self):
        self.assertEqual(str, type(User.email))

    def test_password_str(self):
        self.assertEqual(str, type(User.password))

    def test_first_name_str(self):
        self.assertEqual(str, type(User.first_name))

    def test_last_name_str(self):
        self.assertEqual(str, type(User.last_name))

    def test_two_users_uuid(self):
        usr1 = User()
        usr2 = User()
        self.assertNotEqual(usr1.id, usr2.id)

    def test_two_users_diff_time(self):
        usr1 = User()
        sleep(0.05)
        usr2 = User()
        self.assertLess(usr1.created_at, usr2.created_at)

    def test_two_users_diff_time_update(self):
        usr1 = User()
        sleep(0.05)
        usr2 = User()
        self.assertLess(usr1.updated_at, usr2.updated_at)

    def test_unused_args(self):
        usr = User(None)
        self.assertNotIn(None, usr.__dict__.values())

    def test_instantce_None_kwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)

    def test_instantce_with_kwargs(self):
        date_time = datetime.today()
        date_time_iso = date_time.isoformat()
        usr = User(id="345", created_at=date_time_iso, updated_at=date_time_iso)
        self.assertEqual(usr.id, "345")
        self.assertEqual(usr.created_at, date_time)
        self.assertEqual(usr.updated_at, date_time)

    def test_string_representation(self):
        date_time = datetime.today()
        date_time_repr = repr(date_time)
        usr = User()
        usr.id = "123456"
        usr.created_at = usr.updated_at = date_time
        usrstr = usr.__str__()
        self.assertIn("[User] (123456)", usrstr)
        self.assertIn("'id': '123456'", usrstr)
        self.assertIn("'created_at': " + date_time_repr, usrstr)
        self.assertIn("'updated_at': " + date_time_repr, usrstr)

class TestUser_save(unittest.TestCase):
    """testing save method of the  class."""

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
        usr = User()
        sleep(0.05)
        first_updated_at = usr.updated_at
        usr.save()
        self.assertLess(first_updated_at, usr.updated_at)

    def test_double_saves(self):
        usr = User()
        sleep(0.05)
        first_updated_at = usr.updated_at
        usr.save()
        second_updated_at = usr.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        usr.save()
        self.assertLess(second_updated_at, usr.updated_at)

    def test_save_args(self):
        usr = User()
        with self.assertRaises(TypeError):
            usr.save(None)

    def test_save_update_file(self):
        usr = User()
        usr.save()
        usrid = "User." + usr.id
        with open("file.json", "r") as fd:
            self.assertIn(usrid, fd.read())


class TestUser_to_dict(unittest.TestCase):
    """testing to_dict method of the User class."""

    def test_dict_type(self):
        self.assertTrue(dict, type(User().to_dict()))

    def test_dict_with_correct_keys(self):
        usr = User()
        self.assertIn("id", usr.to_dict())
        self.assertIn("created_at", usr.to_dict())
        self.assertIn("updated_at", usr.to_dict())
        self.assertIn("__class__", usr.to_dict())

    def test_dict_with_added_attributes(self):
        usr = User()
        usr.middle_name = "School"
        usr.my_number = 89
        self.assertEqual("School", usr.middle_name)
        self.assertIn("my_number", usr.to_dict())

    def test_dict_datetime_att_str(self):
        usr = User()
        usr_dict = usr.to_dict()
        self.assertEqual(str, type(usr_dict["id"]))
        self.assertEqual(str, type(usr_dict["created_at"]))
        self.assertEqual(str, type(usr_dict["updated_at"]))

    def test_dict_output(self):
        date_time = datetime.today()
        usr = User()
        usr.id = "123456"
        usr.created_at = usr.updated_at = date_time
        todict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': date_time.isoformat(),
            'updated_at': date_time.isoformat(),
        }
        self.assertDictEqual(usr.to_dict(), todict)

    def test_diff_to_dict(self):
        usr = User()
        self.assertNotEqual(usr.to_dict(), usr.__dict__)

    def test_to_dict_with_args(self):
        usr = User()
        with self.assertRaises(TypeError):
            usr.to_dict(None)


if __name__ == "__main__":
    unittest.main()
