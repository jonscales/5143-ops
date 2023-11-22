#!/usr/bin/env python
"""
    Name
       cmdMv.py
       function mv
    Synopsis
        will move a specified file to a specified directory
    Description
        required parameters:
            filename 
            destination directory 
            destination filename (may be a new name)
        filename can contain an entire path
        destination directory can also be an entire path
        a new filename can be specified
        if the destination directory does not exist, it will be created

    Examples
        mv /somedir/anotherdir/somefile   anewdir
        mv /somedir/anotherdir/somefile   anewdir/anewname
        mv somefile.ext anewdir
        mv bacon.txt test               
"""
import os, sys

def mv(**kwargs):
    """
    Name
       cmdMv.py
       function mv
    Synopsis
        will move a specified file to a specified directory
    Description
        required parameters:
            filename 
            destination directory 
            destination filename (may be a new name)
        filename can contain an entire path
        destination directory can also be an entire path
        a new filename can be specified
        if the destination directory does not exist, it will be created

    Examples
        mv /somedir/anotherdir/somefile   anewdir
        mv /somedir/anotherdir/somefile   anewdir/anewname
        mv somefile.ext anewdir
        mv bacon.txt test               
"""
    current_directory = os.getcwd()      
    sourcePath = kwargs['params'][0]
    newPath = kwargs['params'][1]
    try:
        if len(kwargs["params"]) <2:
            print("Usage: mv <file_name> or </path/filename> and </newpath/file_name> or </newpath/new_file_name>")
        else:
            madenew=False
            #parse out kwargs params
            curPath, fileName = os.path.split(sourcePath)
            if curPath =='':
                curPath = os.getcwd()  
            
            destPath, newFileName = os.path.split(newPath)
            if newFileName =='':
                newFileName = fileName
            # check if filename exits
            if not os.path.exists(sourcePath):
                print(f"Source file '{sourcePath}' does not exist.")
                return
            #check if current path exists
            if not os.path.exists(curPath):
                print(f"Source directory '{curPath}' does not exist.")
                return
            #check if newFileName already exists
            if os.path.exists(newPath):
                print(f"A file with that same name already exists in the destination directory")
                return          
            #check if destination path exists
            
            if not os.path.exists(destPath):
                #if destination directory doesn't exist, create it
                try:
                    madenew=True
                    os.makedirs(destPath)
                except Exception as e:
                    print(f"Error creating destination directory '{destPath}'.")
                    return
            else:
                madenew=False
            # move the file in this round about way
            
            try:
                os.rename(sourcePath,newPath)
                if madenew==True:
                    print(f"Created new directory '{destPath}'.")
                    print(f"Moved '{fileName}' to '{destPath}'.")
                else:
                    print(f"Moved '{fileName}' to '{destPath}'.")
            except Exception as e:
                print(f"Error moving file {e}")
    except Exception as e:
        print(f"An error occurred: {e}")




if __name__ == "__main__":
    sample={'params':['bananas/meat/baconisfruit.txt','bananas/fruit/baconisfruit.txt']}
    mv(**sample)

