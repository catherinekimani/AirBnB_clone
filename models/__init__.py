#!/usr/bin/python3
"""__init__ magic method to create unique FileStorage instance"""
from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
