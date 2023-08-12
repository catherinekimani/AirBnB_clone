#!/usr/bin/python3
""" Define HBNB command class """


import cmd


class HBNBCommand(cmd.Cmd):
    """ command interpreter class """
    prompt = "(hbnb) "

    def do_quit(self, arg):
        """ Quit command to exit the program """
        return True

    def do_EOF(self, arg):
        """ exit prog when EOF is encountered """
        print()
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
