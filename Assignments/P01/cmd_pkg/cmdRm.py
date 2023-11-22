#!/usr/bin/env python"""
"""    
    Name
        cmdRm.py
        function: rm
    Synopsis
        removes a file from the file system or a directory and all its contents
    Description
        function parameters/variables
            flag - 
            filename
    Examples    
        rm pig.txt      removes pig.txt from the file system
        rm -r pig       removes the directory pig and all its contents
    Disclaimer
 
"""
import os
import shutil
import sys
def rm(**kwargs):
    """
    Usage: rm [OPTION]... [FILE]...
        Removes the FILE(s).
    Options:
        -r recursively remove directories and their contents
    Examples:
        rm pig.txt      removes pig.txt from the file system
        rm -r pig       removes the directory pig and all its contents
    """
    flag = kwargs.get('flags', None)
    if 'r' in flag:
        # recursively remove directories and their contents
        try:
            shutil.rmtree(kwargs['params'][0])
        except FileNotFoundError or IsADirectoryError:
            print(f"rm: cannot remove '{kwargs['params'][0]}': No such file or directory")
    else:
        # remove the file
        try:
            os.remove(kwargs['params'][0])
        except FileNotFoundError:
            print(f"rm: cannot remove '{kwargs['params'][0]}': No such file or directory")
    return