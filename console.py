#!/usr/bin/python3
"""Console for managing instances of various classes."""

import cmd
from datetime import datetime
import models
from models import Amenity, BaseModel, City, Place, Review, State, User
import shlex

CLASSES = {
    "Amenity": Amenity,
    "BaseModel": BaseModel,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User,
}

class HBNBCommand(cmd.Cmd):
    """HBNB console"""

    prompt = '(hbnb) '

    def emptyline(self):
        """Overwrite emptyline to do nothing"""
        pass

    def do_EOF(self, arg):
        """Exits the console"""
        return True

    def do_quit(self, arg):
        """Quits the console"""
        return True

    def do_create(self, args):
        """Create a new instance of a class"""
        if not args:
            print("** class name missing **")
            return
        class_name = args.split()[0]
        if class_name not in CLASSES:
            print("** class doesn't exist **")
            return
        new_instance = CLASSES[class_name]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, args):
        """Show instance by class name and id"""
        if not args:
            print("** class name missing **")
            return
        args = args.split()
        if args[0] not in CLASSES:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = args[0] + "." + args[1]
        if key in models.storage.all():
            print(models.storage.all()[key])
        else:
            print("** no instance found **")

    def do_destroy(self, args):
        """Destroy an instance by class name and id"""
        if not args:
            print("** class name missing **")
            return
        args = args.split()
        if args[0] not in CLASSES:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = args[0] + "." + args[1]
        if key in models.storage.all():
            del models.storage.all()[key]
            models.storage.save()
        else:
            print("** no instance found **")

    def do_all(self, args):
        """Print all instances of a class"""
        if not args:
            print([str(obj) for obj in models.storage.all().values()])
            return
        args = args.split()
        if args[0] not in CLASSES:
            print("** class doesn't exist **")
            return
        print([str(obj) for obj in models.storage.all(CLASSES[args[0]]).values()])

    def do_update(self, args):
        """Update an instance by class name and id"""
        if not args:
            print("** class name missing **")
            return
        args = shlex.split(args)
        if args[0] not in CLASSES:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = args[0] + "." + args[1]
        if key not in models.storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        obj = models.storage.all()[key]
        try:
            attr_type = type(getattr(obj, args[2]))
            args[3] = attr_type(args[3])
        except Exception as e:
            pass
        setattr(obj, args[2], args[3])
        obj.save()

if __name__ == '__main__':
    HBNBCommand().cmdloop()
