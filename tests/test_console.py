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

    def test_help(self):
        """ test help command"""

        e = ("Documented commands (type help <topic>):\n"
             "========================================\n"
             "EOF  all  count  create  destroy  help  quit  show  update\n")
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(e, f.getvalue().strip())

    def test_create(self):
        """ Test the create command """
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel")
            self.assertTrue(len(f.getvalue().strip()) == 36)

    def test_show(self):
        """ test show method """
        e = ("Usage: show <class> <id> or <class>.show(<id>)\n        "
             "Display the string representation of a class instance of"
             " a given id.")
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help show"))
            self.assertEqual(e, f.getvalue().strip())

    def test_empty_line(self):

        """ test empty line """
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertNotEqual("", f.getvalue().strip())

    def test_EOF(self):
        """ test EOF command"""

        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(HBNBCommand().onecmd("EOF"))

    def test_quit(self):
        """ test quit command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_count(self):

        """ Test count command """

        e = ("Usage: count <class> or <class>.count()\n        "
             "Retrieve number of instances of a given class")
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(HBNBCommand().onecmd("help count"))
            self.assertEqual(e, f.getvalue().strip())

    def test_all(self):
        """ test all command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("all")
            output = f.getvalue().strip()
            self.assertTrue("BaseModel" in output)

    def test_destroy(self):
        """
        Test destroy command.
        """
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create BaseModel")
            created_id = f.getvalue().strip()

        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd(f"destroy BaseModel {created_id}")
            self.assertFalse(created_id in storage.all())


if __name__ == "__main__":
    unittest.main()
