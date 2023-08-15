#!/usr/bin/python3
"""
Unittests for the console
"""
import os
import sys
import unittest
from unittest.mock import patch
from io import StringIO
from models import storage
from console import HBNBCommand


class TestHBNBCommand(unittest.TestCase):

    """
    Test cases for TestHBNBCommand console
    """
    def setUp(self):
        """ Set up the environment """
        self.console = HBNBCommand()

    def tearDown(self):
        """ clean up after each test """
        self.console = None

    def test_quit(self):
        """ Test quit command """
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd("quit"))
            self.assertEqual(f.getvalue().strip(), "")

    def test_EOF(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd("EOF"))
            self.assertEqual(f.getvalue().strip(), "")

    def test_empty_line(self):
        """ test empty line """
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", output.getvalue().strip())

    def test_help(self):
        """ help command test """
        e = ("Documented commands (type help <topic>):\n"
             "========================================\n"
             "EOF  all  count  create  destroy  help  quit  show  update")
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(e, output.getvalue().strip())

    def test_create(self):
        """ Test the create command """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            output = f.getvalue().strip()
            self.assertTrue(output)

    def test_show(self):
        """ Test show command"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel 12345")
            output = f.getvalue().strip()
            self.assertEqual(output, "** no instance found **")

    def test_check_show(self):
        """ check show method test"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("help show")
            output = f.getvalue().strip()
            self.assertTrue(
                "print string representation of an instance", output)

    def test_count(self):
        """ Test count command """

        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel")

        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("count BaseModel")

    def test_check_count(self):
        """ check count method test"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("help count")
            output = f.getvalue().strip()
            self.assertTrue(
                "Retrieve number of instances of a given class", output)

    def test_all(self):
        """ test all command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel")
            created_id = f.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all BaseModel")
            output = f.getvalue().strip()
            self.assertIn(created_id, output)

    def test_destroy(self):
        """
        Test destroy command.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel")
            created_id = f.getvalue().strip()

        with patch('sys.stdout', new=StringIO()):
            self.console.onecmd(f"destroy BaseModel {created_id}")
            self.assertNotIn(created_id, storage.all())

    def test_destroy_BaseModel(self):
        """ test destroy BaseModel """
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("help destroy")
            e = f.getvalue().strip()
            self.assertTrue("Delete an instance based on class name and id", e)

    def test_update_BaseModel(self):
        """ test update BaseModel """
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("help update")
            output = f.getvalue().strip()
            self.assertTrue(
                "update an instance based on class name and id", output)

    def test_check_BaseModel(self):
        """ check BaseModel test"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("help all")
            output = f.getvalue().strip()
            self.assertTrue(
                "print string representation of all instances", output)


if __name__ == "__main__":
    unittest.main()
