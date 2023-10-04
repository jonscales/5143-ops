#!/usr/bin/env python
"""
    Name
       cmdHead.py
       function: head
    Synopsis
        Returns the first 10 lines of a file or the first n lines of a file
    Description
        Prints the first 10 lines of a file or the first n lines of a file
        Usage: head <filename> or head -n <number of lines> <filename>
                or head -n <number of lines> <filename> 
                or head <filename>
    Examples    
        head file1.txt
        head -n 5 file1.txt
        head file1.txt -n 5                       
"""
from io import StringIO
def head(**kwargs):
    """
        Name
        cmdHead.py
        function: head
        Synopsis
            Returns the first 10 lines of a file or the first n lines of a file
        Description
            Prints the first 10 lines of a file or the first n lines of a file
            Usage: head <filename> or head -n <number of lines> <filename>
                    or head -n <number of lines> <filename> 
                    or head <filename>
        Examples    
            head file1.txt
            head -n 5 file1.txt
            head file1.txt -n 5                       
    """
    # Check for flag
    output = []
            
    if 'n' in kwargs['flags']:
        try:
            line_num = int(kwargs['params'][1])
            file_name = kwargs['params'][0]
        except:
            line_num = int(kwargs['params'][0])
            file_name = kwargs['params'][1]
    else:
        line_num = 10
        file_name = kwargs['params'][0]

    try: 
        with open(file_name, 'r') as f:  
            content = f.readlines()                          # Read in file
    except:
        try:
            content = StringIO(file_name).readlines()        # Read in string
        except:
            print("File does not exist")
            return
    
    for line in content[:line_num]:                 # Print last n lines
        output.append(line)

    output = ''.join(output).strip()
    if not kwargs['stdin']:    
        print(output)
    else:
        return output

