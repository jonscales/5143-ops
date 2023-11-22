#!/usr/bin/env python
"""
    Name
       cmdLess.py
       function: less
    Synopsis
        returns a block of the test of a designated file to the screen 
        the # of lines in the block matches the size of the terminal
        when enter is pressed again, a second block of text of the file is 
        sent to the terminal. 
    Description
        function parameters/variables
            flag - 
            filename
    Examples    
        less pig.txt 
    Disclaimer
        I got an almost working version, but didn't know the correct python for loop syntax
        I pasted my code into ChatGPT which gave me a modified, cleaner, working version                    
"""
import os
import math
#import keyboard


def less(**kwargs):
    """
        Name
        cmdLess.py
        function: less
        Synopsis
            returns a block of the teXt of a designated file to the screen 
            the # of lines in the block matches the size of the terminal
            when enter is pressed again, a second block of text of the file is 
            sent to the terminal. 
        Description
            function parameters/variables
                filename
        Examples    
            less pig.txt               
    """
    # Get the terminal size
    try:
        termLines = int(os.environ.get('LINES', 10))  # Gets the number of terminal lines, defaults to 10
    except ValueError:
        termLines = 10  # Resets to 10 as a default if LINES cannot be converted to an integer

    # Get the file name to process
    file = kwargs['params'][0]

    # Check that the file name was entered and is a valid file
    if not os.path.isfile(file):
        print(f"{file} not found. Enter a valid filename.")
        return

    # Open the file and determine how many lines it has
    with open(file, 'r') as thisFile:
        lineList = thisFile.readlines()
        totalLineNum = len(lineList)

    # Calculate the number of pages
    pages = math.ceil(totalLineNum / termLines)

    print(f"Total lines in file = {totalLineNum}")
    print(f"Terminal lines = {termLines}")
    print(f"Pages = {pages}")

    pageCount = 1
    for p in range(pages):
        print(f"Page {pageCount}/{pages}:")
        for l in range(p * termLines, (p + 1) * termLines):
            if l < totalLineNum:
                print(lineList[l], end='')

        pageCount += 1
        if pageCount <= pages:
            #this waits until enter is pressed, but it allows other keys to be pressed and echos them to the console
            input("\nPress Enter to continue...")
            

if __name__ == '__main__':
    sample = {'params': ['meats.txt']}
    less(**sample)










