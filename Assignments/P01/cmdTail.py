#!/usr/bin/env python
"""
    This file is used for the 'tail' command. It is responsible for printing the
    last 10 lines of a file, unless a different number is specified using the -n flag
"""
from io import StringIO
def tail(**kwargs):
    """
        tail command : prints the last 10 lines of a file
        flags        : -n (number of lines to print)
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
   
    for line in content[-line_num:]:                 # Print last n lines
        output.append(line)

    output = ''.join(output).strip()
    if not kwargs['stdin']:    
        print(output)
    else:
        return output
    
if __name__=='__main__':
    thing={'name':' ','params':['meat.txt', '3'],'flags':['n'], 'stdin':False}
    tail(**thing)
