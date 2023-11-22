#!/usr/bin/env python
# again ChatGPT did the lion's share of the work. 
"""
    Name
       For testing purposes, command call is cdir
       For actual operational version
       cd - changed directory from CWD to specified directtory in current or specified path 
    Synopsis
        for testing: 
            cdir directory name or cdir /path/path/directory name
            cdir .. changes CWD up one directory level in current path
            cdir . changes CWD to root directory
            cdir ~ changes CWD to /root/user directory
        for actual operation version:
            cd  /path/directory name or cd directory name or cd .. or cd . or cd ~ 
    Description
        when called, function shows cwd with command prompt
        requires a directory name parameter
        optionally can handle a /path/directory name and .. , . and ~ parameters                        
    """
import os

def cd(**kwargs):
    """
    Name
       For testing purposes, command call is cdir
       For actual operational version
       cd - changed directory from CWD to specified directtory in current or specified path 
    Synopsis
        for testing: 
            cdir directory name or cdir /path/path/directory name
            cdir .. changes CWD up one directory level in current path
            cdir . changes CWD to root directory
            cdir ~ changes CWD to /root/user directory
        for actual operation version:
            cd  /path/directory name or cd directory name or cd .. or cd . or cd ~ 
    Description
        when called, function shows cwd with command prompt
        requires a directory name parameter
        optionally can handle a /path/directory name and .. , . and ~ parameters                        
    """
    # while True:
    #     # Get the current working directory
    current_directory = os.getcwd()
    #     # Display the command prompt with '%' and current directory
    #     command_prompt = f"% {current_directory} $ "
        
    #     # Get user input for the command
    #     user_input = input(command_prompt)
        
    #     # Split the user input into command and arguments
    #     command_parts = user_input.split()
    #     if not command_parts:
    #         continue
        
    #     # Extract the command and arguments
    #     command = command_parts[0]
    #     arguments = command_parts[1:]
        
    #     if command == 'cd':  # used a unique name here for the command to ensure that this 
    #         #function is running rather than the system OS cd command
    #         # Handle 'cd' command to change the directory
    arguments = kwargs["params"][0]
    
    if not arguments:
        print("Usage: cd <directory>")
    elif arguments == '..':
        # Move up one directory
        directory = current_directory.split('/')
        directory.pop()
        new_directory = '/'.join(directory)
        os.chdir(new_directory)
        #print(os.getcwd())
    elif arguments == '.':
        # Stay in the current directory
        pass
    elif arguments == '~':
        # Change to the user's home directory
        os.chdir(os.path.expanduser("~"))
    else:
        # Change to the specified directory
        #specified = [current_directory, arguments]
        new_directory = current_directory+"/"+arguments
        try:
            os.chdir(new_directory)
        except FileNotFoundError:
            print(f"Directory '{new_directory}' not found.")
    return "this worked"        

if __name__ == "__main__":
    sample = {'name': 'cd', 'flag': [], 'params':["~"]}
    cd(**sample)
