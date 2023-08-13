#!/usr/bin/python3
""" Define HBNB command class """


import cmd
import re
from shlex import split
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models import storage


def parse(arg):
    """
    parse command args enclosed in curly braces or brackets
    Return: A list of parsed arguments
    """
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [item.strip(",") for item in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            res_list = [item.strip(",") for item in lexer]
            res_list.append(brackets.group())
            return res_list
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        res_list = [item.strip(",") for item in lexer]
        res_list.append(curly_braces.group())
        return res_list


class HBNBCommand(cmd.Cmd):
    """ command interpreter class """
    prompt = "(hbnb) "
    classes = [
                "BaseModel",
                "User",
                "Place",
                "State",
                "City",
                "Amenity",
                "Review",
    ]

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

    def do_count(self, arg):
        """ Retrieve number of instances of a gieven class """
        args = parse(arg)
        idx = 0
        for obj in storage.all().values():
            if args[0] == obj.__class__.__name__:
                idx += 1
        print(idx)

    def do_update(self, arg):
        """ update an instance based on class name and id """
        args = parse(arg)
        obj_dict = storage.all()

        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(args) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(args[0], args[1]) not in obj_dict.keys():
            print("** no instance found **")
            return False
        if len(args) == 2:
            print("** attribute name missing **")
            return False
        if len(args) == 3:
            try:
                type(eval(args[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(args) == 4:
            obj = obj_dict["{}.{}".format(args[0], args[1])]
            if args[2] in obj.__class__.__dict__.keys():
                attr_type = type(obj.__class__.__dict__[args[2]])
                obj.__dict__[args[2]] = attr_type(args[3])
            else:
                obj.__dict__[args[2]] = args[3]
        elif type(eval(args[2])) == dict:
            obj = obj_dict["{}.{}".format(args[0], args[1])]
            for a, b in eval(args[2]).items():
                if (a in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[a]) in {str, int, float}):
                    attr_type = type(obj.__class__.__dict__[a])
                    obj.__dict__[a] = attr_type(b)
                else:
                    obj.__dict__[a] = b
        storage.save()

    def default(self, arg):
        """called on an input line when the cmd prefix is not known"""
        cmds_dict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update,
            "create": self.do_create
        }
        match = re.search(r"\.", arg)
        if match is not None:
            args = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", args[1])
            if match is not None:
                command = [args[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in cmds_dict.keys():
                    call = "{} {}".format(args[0], command[1])
                    return cmds_dict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False


if __name__ == '__main__':
    HBNBCommand().cmdloop()
