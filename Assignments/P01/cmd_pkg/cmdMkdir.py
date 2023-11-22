#!/usr/bin/env python
# code help from GPT
"""
    Name
       For testing purposes, command call is makedir
       For actual operational version
       mkdir - creates (makes) a new directory
    Synopsis
        for testing: 
            makedir /path/filenameext or makedir filename.ext
        for actual operation version:
            mkdir  /path/filename.ext or mkdir filename.ext
    Description
        when called, function shows cwd with command prompt
        requires a filename parameter
        optionally can handle a /path/filename 
        if path not spedified, will create new directory in current working directory
    Examples
        mkdir filename.txt
        mkdir /user/path/filename.txt                
    """
import os

def mkdir(**kwargs):        
    """
    Name
       For testing purposes, command call is makedir
       For actual operational version
       mkdir - creates (makes) a new directory
    Synopsis
        for testing: 
            makedir /path/filenameext or makedir filename.ext
        for actual operation version:
            mkdir  /path/filename.ext or mkdir filename.ext
    Description
        when called, function shows cwd with command prompt
        requires a filename parameter
        optionally can handle a /path/filename 
        if path not spedified, will create new directory in current working directory
    Examples
        mkdir filename.txt
        mkdir /user/path/filename.txt                
    """
    #while True:
    current_directory = os.getcwd()      
    try:
        if len(kwargs["params"]) == 0:
            print("Usage: mkdir <directory_name>. Directory name may not contain spaces.")
        else:
            directory_name = kwargs['params'][0]
            # Check if the user specified a different path
            if '/' in directory_name:
                # Use the provided path to create the directory
                try:
                    os.makedirs(directory_name)
                    print(f"Directory '{directory_name}' created successfully.")
                except FileExistsError:
                    print(f"Directory '{directory_name}' already exists.")
                except Exception as e:
                    print(f"Error creating directory: {e}")
            else:
                # Create the directory in the current directory
                new_directory_path = os.path.join(current_directory, directory_name)
                try:
                    os.mkdir(new_directory_path)
                    print(f"Directory '{new_directory_path}' created successfully.")
                except FileExistsError:
                    print(f"Directory '{new_directory_path}' already exists.")
                except Exception as e:
                    print(f"Error creating directory: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    sample = {'params':['testdir']}
    mkdir(**sample)


