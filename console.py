#!/usr/bin/python3
""" Define HBNB command class """


import cmd
from models.base_model import BaseModel
from models import storage


class HBNBCommand(cmd.Cmd):
    """ command interpreter class """
    prompt = "(hbnb) "
    classes = {"BaseModel": BaseModel}

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
            print([str(obj) for obj in objects.values()
                   if args[0] in obj.__class__.__name__])
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


if __name__ == '__main__':
    HBNBCommand().cmdloop()
