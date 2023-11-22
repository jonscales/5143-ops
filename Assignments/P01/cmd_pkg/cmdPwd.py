#!/usr/bin/env python
"""
    This fild is used for the 'pwd' command. It is responsible for printing the
    current working directory.
"""
import os,sys

def pwd(**kwargs):
    """
        pwd command : prints the current working directory
    """
    if not kwargs['stdin']:
        print(os.getcwd())
    return os.getcwd()

if __name__ == '__main__':
    pwd()