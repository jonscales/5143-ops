#cmdChmod
"""
    Name
       cmdChmod.py
       
    Synopsis
        Change the permissions  
    Description
        change the permissions

        required parameters
            filename or path/filename
            numbers to convert to binary to change each permission to be true or false
    Example
        chmod 777 filename                      
    """
import os, sys
import rich
import shutil

def chmod(**kwargs):
    """
    Name
       cmdChmod.py
    Synopsis
        Change the permissions of a file 
        required parameters
            filename or path/filename
            numeric permissions specification
    Description
        change the permissions using the numberic method
        The numeric equivalencies are listed here
        7  sets rwx    
        6  sets rw-
        5  sets r-x
        4  sets r--
        3  sets -wx
        2  sets -w-
        1  sets --x
        0  sets ---
        Using a combination of 3 numbers, i.e. 674, sets the permissions
        respectively for user (1st digit), group (2nd digit), world (3rd digit) 
    Example
        Chmod 777 filename
        Chmod 777 path/filename
        Chmod filename 777
        Chmod path/filname 777                      
    """
    import os

def chmod(**kwargs):
    # Extract permission mode and filename from kwargs
    permission_mode = None
    filename = None
    #print(kwargs['params']) # just to test
    addbackempty=False
    if '' in kwargs['params']:
        kwargs['params'].remove('')  # removes any empty strings from params
        addbackempty=True        # bool to add back empty string after function runs
        #print(kwargs['params']) # just to test
    for param in kwargs.get('params', []):
        #print(param +"  in for param loop") # just to test
        if param == '':
            #print(param + " if param =='' ")  # just to test
            break
        elif param.isdigit() and len(param) == 3:
            permission_mode = param
            #print(permission_mode +" in elif perm mode")  # just to test
        else:
            filename = param.strip()  # Remove leading/trailing whitespace
            #print(filename +" in else filename assgn") # just to test
    if permission_mode is None:
        print("Error: Permission mode (a 3-digit number) is required.")
        return

    if filename is None:
        print("Error: Please provide a filename.")
        return

    # Convert permission mode to an integer
    try:
        permission_mode = int(permission_mode, 8)
    except ValueError:
        print("Error: Invalid permission mode.")
        return
    
    if addbackempty==True:
        kwargs['params'].append('')
        #print(kwargs['params'])  # just to test
    
    # Check if the filename exists
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' does not exist.")
        return

    # Change the file permissions
    try:
        os.chmod(filename, permission_mode)
        print(f"Changed permissions of '{filename}' to {oct(permission_mode)[2:]}.")
    except OSError as e:
        print(f"Error: {e}")
    
    


if __name__ == '__main__':
    # Example usage:
    sample1 = {'params': ['baconater.txt', '666','']}
    sample2 = {'params': ['666', 'baconater.txt','']}
    
    chmod(**sample1)
    #Chmod(**sample2)
