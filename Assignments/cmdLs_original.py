#!/usr/bin/env python
"""
    Name
       cmdLs.py
       function: ls
    Synopsis
        lists the contents of a directory
    Examples    
        ls
        ls -l
        ls -a
        ls -h
"""
import os, sys, stat, datetime

def ls(**kwargs):
    """"
        ls command  : lists the contents of a directory 
        flags       : -l (long format)
                      -a (all files)
                      -h (human readable)
    """
    output = []
    # Check for flags
    flags = kwargs.get('flags', '')
    long_format = 'l' in flags
    all_files = 'a' in flags
    human_readable = 'h' in flags

    # Get the current working directory
    current_directory = os.getcwd()
    # Get the contents of the directory
    if all_files:
        directory_contents = os.listdir(current_directory, hidden=True)
    else:
        directory_contents = os.listdir(current_directory)
    # Print the contents of the directory
    if long_format:
        for item in directory_contents:
            if all_files:
                # Print all files
                print(item)
            else:
                # Ignore hidden files
                if item[0] != '.':
                    print(item)
    else:
        for item in directory_contents:
            if all_files:
                # Print all files
                print(item)
            else:
                # Ignore hidden files
                if item[0] != '.':
                    print(item)
    

    
    # code to get permissions for a file/directory
    
    dir_info=os.stat("meat.txt")
    print(dir_info) # just to show for test - shows everything
    print(stat.filemode(dir_info[0])) # would print just the permissions in rwxrwxrwx version
   
   # this part gets the modified time and formats it 

# Get the st_mtime value from os.stat_result
    st_mtime = os.stat("meat.txt").st_mtime

# Convert st_mtime to a datetime object
    timestamp = datetime.datetime.fromtimestamp(st_mtime)

# Format the datetime object as "Month Day, Year 24Hr:Minute"
    formatted_time = timestamp.strftime("%B %d, %Y %H:%M")

    print(f"Modified time: {formatted_time}")

  # need to get user to be a name and group to be a name and size 
 #dfa 




    
if __name__ == '__main__':
    sample = {'name': 'ls', 'flags': ['l','a','h'], 'params': []}
    ls(**sample)