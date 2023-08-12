#!/usr/bin/python3
"""Defines unittests for Review"""
from models.review import Review
from time import sleep
from datetime import datetime
import unittest
import models
import os


class TestReview_instantiation(unittest.TestCase):
    """testing instantiation of the Review class."""

    def test_no_args(self):
        self.assertEqual(Review, type(Review()))

    def test_new_instance(self):
        self.assertIn(Review(), models.storage.all().values())

    def test_created_at_datetime(self):
        self.assertEqual(datetime, type(Review().created_at))

    def test_id_is_public(self):
        self.assertEqual(str, type(Review().id))

    def test_updated_at_datetime(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def test_place_id_attribute(self):
        new_rv = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(new_rv))
        self.assertNotIn("place_id", new_rv.__dict__)

    def test_user_id_attribute(self):
        new_rv = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(new_rv))
        self.assertNotIn("user_id", new_rv.__dict__)

    def test_text_attribute(self):
        new_rv = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(new_rv))
        self.assertNotIn("text", new_rv.__dict__)

    def test_two_reviews_uuid(self):
        new_rv1 = Review()
        new_rv2 = Review()
        self.assertNotEqual(new_rv1.id, new_rv2.id)

    def test_two_reviews_diff_time(self):
        new_rv1 = Review()
        sleep(0.05)
        new_rv2 = Review()
        self.assertLess(new_rv1.created_at, new_rv2.created_at)

    def test_two_reviews_diff_time_update(self):
        new_rv1 = Review()
        sleep(0.05)
        new_rv2 = Review()
        self.assertLess(new_rv1.updated_at, new_rv2.updated_at)

    def test_unused_args(self):
        new_rv = Review(None)
        self.assertNotIn(None, new_rv.__dict__.values())

    def test_instantce_None_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)

    def test_instantce_with_kwargs(self):
        date_time = datetime.today()
        date_time_iso = date_time.isoformat()
        new_rv = Review(id="345", created_at=date_time_iso, updated_at=date_time_iso)
        self.assertEqual(new_rv.id, "345")
        self.assertEqual(new_rv.created_at, date_time)
        self.assertEqual(new_rv.updated_at, date_time)

    def test_string_representation(self):
        date_time = datetime.today()
        date_time_repr = repr(date_time)
        new_rv = Review()
        new_rv.id = "123456"
        new_rv.created_at = new_rv.updated_at = date_time
        new_rvstr = new_rv.__str__()
        self.assertIn("[Review] (123456)", new_rvstr)
        self.assertIn("'id': '123456'", new_rvstr)
        self.assertIn("'created_at': " + date_time_repr, new_rvstr)
        self.assertIn("'updated_at': " + date_time_repr, new_rvstr)

class TestReview_save(unittest.TestCase):
    """testing save method of the  Review."""

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
        new_rv = Review()
        sleep(0.05)
        first_updated_at = new_rv.updated_at
        new_rv.save()
        self.assertLess(first_updated_at, new_rv.updated_at)

    def test_double_saves(self):
        new_rv = Review()
        sleep(0.05)
        first_updated_at = new_rv.updated_at
        new_rv.save()
        second_updated_at = new_rv.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        new_rv.save()
        self.assertLess(second_updated_at, new_rv.updated_at)

    def test_save_args(self):
        new_rv = Review()
        with self.assertRaises(TypeError):
            new_rv.save(None)

    def test_save_update_file(self):
        new_rv = Review()
        new_rv.save()
        new_rvid = "Review." + new_rv.id
        with open("file.json", "r") as fd:
            self.assertIn(new_rvid, fd.read())


class TestReview_to_dict(unittest.TestCase):
    """testing to_dict method of the Review class."""

    def test_dict_type(self):
        self.assertTrue(dict, type(Review().to_dict()))

    def test_dict_with_correct_keys(self):
        new_rv = Review()
        self.assertIn("id", new_rv.to_dict())
        self.assertIn("created_at", new_rv.to_dict())
        self.assertIn("updated_at", new_rv.to_dict())
        self.assertIn("__class__", new_rv.to_dict())

    def test_dict_with_added_attributes(self):
        new_rv = Review()
        new_rv.middle_name = "School"
        new_rv.my_number = 89
        self.assertEqual("School", new_rv.middle_name)
        self.assertIn("my_number", new_rv.to_dict())

    def test_dict_datetime_att_str(self):
        new_rv = Review()
        new_rv_dict = new_rv.to_dict()
        self.assertEqual(str, type(new_rv_dict["id"]))
        self.assertEqual(str, type(new_rv_dict["created_at"]))
        self.assertEqual(str, type(new_rv_dict["updated_at"]))

    def test_dict_output(self):
        date_time = datetime.today()
        new_rv = Review()
        new_rv.id = "123456"
        new_rv.created_at = new_rv.updated_at = date_time
        todict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': date_time.isoformat(),
            'updated_at': date_time.isoformat(),
        }
        self.assertDictEqual(new_rv.to_dict(), todict)

    def test_diff_to_dict(self):
        new_rv = Review()
        self.assertNotEqual(new_rv.to_dict(), new_rv.__dict__)

    def test_to_dict_with_args(self):
        new_rv = Review()
        with self.assertRaises(TypeError):
            new_rv.to_dict(None)


if __name__ == "__main__":
    unittest.main()
