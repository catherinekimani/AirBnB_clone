#!/usr/bin/python3
"""Defines unittests for state"""
from models.state import State
from time import sleep
from datetime import datetime
import unittest
import models
import os


class TestState_instantiation(unittest.TestCase):
    """testing instantiation of the State class."""

    def test_no_args(self):
        self.assertEqual(State, type(State()))

    def test_new_instance(self):
        self.assertIn(State(), models.storage.all().values())

    def test_created_at_datetime(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_id_is_public(self):
        self.assertEqual(str, type(State().id))

    def test_updated_at_datetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_name_attribute(self):
        new_state = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(new_state))
        self.assertNotIn("name", new_state.__dict__)

    def test_two_states_uuid(self):
        new_state1 = State()
        new_state2 = State()
        self.assertNotEqual(new_state1.id, new_state2.id)

    def test_two_states_diff_time(self):
        new_state1 = State()
        sleep(0.05)
        new_state2 = State()
        self.assertLess(new_state1.created_at, new_state2.created_at)

    def test_two_state_diff_time_update(self):
        new_state1 = State()
        sleep(0.05)
        new_state2 = State()
        self.assertLess(new_state1.updated_at, new_state2.updated_at)

    def test_unused_args(self):
        new_state = State(None)
        self.assertNotIn(None, new_state.__dict__.values())

    def test_instantce_None_kwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)

    def test_instantce_with_kwargs(self):
        date_time = datetime.today()
        date_time_iso = date_time.isoformat()
        new_state = State(id="345", created_at=date_time_iso,
                          updated_at=date_time_iso)
        self.assertEqual(new_state.id, "345")
        self.assertEqual(new_state.created_at, date_time)
        self.assertEqual(new_state.updated_at, date_time)

    def test_string_representation(self):
        date_time = datetime.today()
        date_time_repr = repr(date_time)
        new_state = State()
        new_state.id = "123456"
        new_state.created_at = new_state.updated_at = date_time
        new_statestr = new_state.__str__()
        self.assertIn("[State] (123456)", new_statestr)
        self.assertIn("'id': '123456'", new_statestr)
        self.assertIn("'created_at': " + date_time_repr, new_statestr)
        self.assertIn("'updated_at': " + date_time_repr, new_statestr)


class TestState_save(unittest.TestCase):
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
        new_state = State()
        sleep(0.05)
        first_updated_at = new_state.updated_at
        new_state.save()
        self.assertLess(first_updated_at, new_state.updated_at)

    def test_double_saves(self):
        new_state = State()
        sleep(0.05)
        first_updated_at = new_state.updated_at
        new_state.save()
        second_updated_at = new_state.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        new_state.save()
        self.assertLess(second_updated_at, new_state.updated_at)

    def test_save_args(self):
        new_state = State()
        with self.assertRaises(TypeError):
            new_state.save(None)

    def test_save_update_file(self):
        new_state = State()
        new_state.save()
        new_stateid = "State." + new_state.id
        with open("file.json", "r") as fd:
            self.assertIn(new_stateid, fd.read())


class TestState_to_dict(unittest.TestCase):
    """testing to_dict method of the State class."""

    def test_dict_type(self):
        self.assertTrue(dict, type(State().to_dict()))

    def test_dict_with_correct_keys(self):
        new_state = State()
        self.assertIn("id", new_state.to_dict())
        self.assertIn("created_at", new_state.to_dict())
        self.assertIn("updated_at", new_state.to_dict())
        self.assertIn("__class__", new_state.to_dict())

    def test_dict_with_added_attributes(self):
        new_state = State()
        new_state.middle_name = "School"
        new_state.my_number = 89
        self.assertEqual("School", new_state.middle_name)
        self.assertIn("my_number", new_state.to_dict())

    def test_dict_datetime_att_str(self):
        new_state = State()
        new_state_dict = new_state.to_dict()
        self.assertEqual(str, type(new_state_dict["id"]))
        self.assertEqual(str, type(new_state_dict["created_at"]))
        self.assertEqual(str, type(new_state_dict["updated_at"]))

    def test_dict_output(self):
        date_time = datetime.today()
        new_state = State()
        new_state.id = "123456"
        new_state.created_at = new_state.updated_at = date_time
        todict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': date_time.isoformat(),
            'updated_at': date_time.isoformat(),
        }
        self.assertDictEqual(new_state.to_dict(), todict)

    def test_diff_to_dict(self):
        new_state = State()
        self.assertNotEqual(new_state.to_dict(), new_state.__dict__)

    def test_to_dict_with_args(self):
        new_state = State()
        with self.assertRaises(TypeError):
            new_state.to_dict(None)


if __name__ == "__main__":
    unittest.main()
