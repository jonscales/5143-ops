#!/usr/bin/env python
import os,sys
#from rich import print
from cmd_pkg import *
# sys.path.append(os.getcwd())

class CommandsHelper(object):
    """
    This function iterates over globals.items() and if one of the values is "callable"
    meaning it is a function, then I add it to a dictionary called 'invoke'. I also
    add the functions '__doc__' string to a help dictionary.

    Methods:
        exists (string) : checks if a command exists (dictionary points to the function)
        help (string) : returns the doc string for a function 
    """
    def __init__(self):                                 # constructor
        self.invoke = {}                                # dictionary to hold functions
        self.help = {}                                  # dictionary to hold doc strings

        for key, value in globals().items():            # iterate over globals
            if key != 'Commands' and callable(value):   # if it is a function
                self.invoke[key] = value                # add it to the dictionary
                self.help[key] = value.__doc__          # add the doc string to the dictionary

    def exists(self,cmd):   
        return cmd['name'] in self.invoke                       # check if command exists
    
    def run(self,cmd):
        if self.exists(cmd):                            # if it exists
            return self.invoke[cmd['name']](**cmd)                   # run it
        else:
            print(f"Command {cmd['name']} does not exist")
            return None
    
    def help(self,cmd):
        if self.exists(cmd):                                # if it exists
            return self.help[cmd['name']]                    # return the doc string
        else:
            return None
        

if __name__=='__main__':
    cmdHelper = CommandsHelper()
    print(cmdHelper.help['ls'])
    # print(os.getcwd())
    # print()
