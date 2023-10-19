"""
A simple program to test example files in a development environment.

The current working directory need to contain this file, then run in terminal:
    python test.py <*arguments>

Then input the file name to test, or leave it blank to use the previous entry
If the argument list is empty, it will prompt you are argument list. Leave it empty to use previous entry
If the argument list is just "--", it will default to previous entry
"""
import os
import sys

def info(*message):
    print("\x1B[36m[ INFO ]  " + " ".join(message) + "\x1B[0m")

def error(*message):
    print("\x1B[31m[ ERROR ] " + " ".join(message) + "\x1B[0m")

def inp(*message):
    try:
        return input("\x1B[32m[ INPUT ]  " + " ".join(message) + "\x1B[0m")
    except (KeyboardInterrupt, EOFError):
        print()
        error("Input was cancelled! Defaulting to no input!")
        return ""

print("----------[ EXAMPLES TESTING ]----------")

file = inp("Example module to load: examples/")

cache = None
if os.path.exists("test-cache.txt"):
    with open("test-cache.txt") as _:
        cache = _.read().split("\n")

import_ = None
if file:
    import_ = file.removesuffix(".py")
else:
    if cache:
        import_ = cache[0]
        info("No input provided. Using previous cache:", import_)
    else:
        error("No cache provided!")

if import_:
    argv = sys.argv
    this_file_name = argv.pop(0)

    if not argv:
        new_argv = inp("Please input argv: ")
        if new_argv:
            argv = new_argv.split()
        else:
            argv = cache[1].split()
            info("No input provided. Using previous cache:", *argv)
    else:
        if argv[0] == "--":
            argv = cache[1].split()
            info("Using previous cache:", *argv)

    sys.argv = [this_file_name] + argv

if import_ and len(sys.argv) > 1:
    info("Running", import_, "with arguments:", ", ".join(sys.argv[1:]))
    __import__("examples." + import_)

print("---------[ TESTING  INITIATED ]---------")