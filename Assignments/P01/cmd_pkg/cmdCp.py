#!/usr/bin/env python
"""
    Name
       cmdCp.py
       copy command function
       cp 
    Synopsis
        cp   /path/directory name or cd directory name or cd .. or cd . or cd ~ 
    Description
        copies a file to a new directory
        whereas move removes the file from the current location and puts it in a new location
        copy retains the original file in the current location and makes a new
        version of the file in a new location

        required parameters
            filename or path/filename
            newfilename or newpath/filename or newpath/newfilename
    Example
        cp somefile.txt  /newpath/somefile.txt
        cp /somepath/somfile.txt  /newpath/somefile.txt  
        cp somefile.txt  /samedirectory/newfilenamesamefilecontent.txt                      
"""
import os, sys
import shutil

def cp(**kwargs):
    """
    Name
       cmdCp.py
       copy command function
       cp 
    Synopsis
        cp   /path/directory name or cd directory name or cd .. or cd . or cd ~ 
    Description
        copies a file to a new directory
        whereas move removes the file from the current location and puts it in a new location
        copy retains the original file in the current location and makes a new
        version of the file in a new location

        required parameters
            filename or path/filename
            newfilename or newpath/filename or newpath/newfilename
    Example
        cp somefile.txt  /newpath/somefile.txt
        cp /somepath/somfile.txt  /newpath/somefile.txt  
        cp somefile.txt  /samedirectory/newfilenamesamefilecontent.txt                      
"""
    # handle kwargs parameters
    sourcePath = kwargs['params'][0]
    destDir = kwargs['params'][1]
    sourceFile = os.path.basename(sourcePath)
    print(f"the file to be copied is '{sourceFile}'")
    destPath = os.path.join(destDir,sourceFile)
    print(f"The file will be copied into directory '{destPath}'")  
    # check that filename or path/filename exists
    if not os.path.exists(sourcePath):
        print(f"Source file '{sourcePath}' does not exist.")
        return
    # check that new path exists.  if it does not create directory
    os.makedirs(os.path.dirname(destPath), exist_ok=True)
   
    # check if the newfilename already exists. If so, create new filename with
    # uniquie identifyer (-1, -2, etc) appended to filename
    if os.path.exists(destPath):
        base, ext = os.path.splitext(sourceFile)
        i = 1
        while True:
            new_filename = f"{base}-{i}{ext}"
            destPath = os.path.join(destDir, new_filename)
            if not os.path.exists(destPath):
                break
            i += 1
    try:
        # Copy the file with the unique name
        shutil.copy(sourcePath, destPath)
        print(f"File '{sourcePath}' copied to '{destPath}'")
    except Exception as e:
        print(f"Error: {e}")
    

if __name__ == "__main__": 
        sample={'params':['bananas/fruit/baconisfruit.txt','bananas/meat/baconisfruit.txt']}
        cp(**sample)