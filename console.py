#!/usr/bin/python3
""" Define HBNB command class """


import cmd
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

from models import storage


class HBNBCommand(cmd.Cmd):
    """ command interpreter class """
    prompt = "(hbnb) "
    classes = {
                "BaseModel": BaseModel,
                "User": User,
                "Place": Place,
                "State": State,
                "City": City,
                "Amenity": Amenity,
                "Review": Review
                }

    def emptyline(self):
        """ Do nothing on empty input line """
        pass

    def do_quit(self, arg):
        """ Quit command to exit the program """
        return True

    def do_EOF(self, arg):
        """ exit prog when EOF is encountered """
        print()
        return True

    def do_create(self, arg):
        """ Create new instance of BaseModel """
        args = arg.split()
        if not arg:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        else:
            new_instance = HBNBCommand.classes[args[0]]()
            new_instance.save()
            print(new_instance.id)

    def do_show(self, arg):
        """ print string representation of an instance """
        args = arg.split()
        if not arg:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            obj_key = "{}.{}".format(args[0], args[1])
            if obj_key in storage.all():
                print(storage.all()[obj_key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """ Delete an instance based on class name and id """
        args = arg.split()
        if not arg:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            obj_key = "{}.{}".format(args[0], args[1])
            if obj_key in storage.all():
                storage.all().pop(obj_key)
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """ print string representation of all instances """
        args = arg.split()
        objects = storage.all()
        if not args:
            print([str(obj) for obj in objects.values()])
        elif args[0] in HBNBCommand.classes:
            class_name = args[0]
            class_instance = HBNBCommand.classes[class_name]
            print([str(obj) for obj in class_instance.all().values()])
        else:
            print("** class doesn't exist **")

    def do_update(self, arg):
        """ update an instance based on class name and id """
        args = arg.split()
        objects = storage.all()
        if not arg:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            obj_key = "{}.{}".format(args[0], args[1])
            if obj_key in objects:
                if len(args) < 3:
                    print("** attribute name missing **")
                elif len(args) < 4:
                    print("** value missing **")
                else:
                    instance = objects[obj_key]
                    attr_name = args[2]
                    attr_val = args[3]
                    setattr(instance, attr_name, attr_val)
                    instance.save()
            else:
                print("** no instance found **")

    def default(self, line):
        """ called on an input line when the cmd prefix is not known"""
        input_parts = line.split('.')
        if len(input_parts) == 2 and input_parts[1] == "all()":
            class_name = input_parts[0]
            if class_name in HBNBCommand.classes:
                class_instance = HBNBCommand.classes[class_name]
                print([str(obj) for obj in storage.all().values()
                       if type(obj) == class_instance])
            else:
                print("** class doesn't exist **")
        else:
            print("*** Unknown syntax:", line)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
