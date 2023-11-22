#!/usr/bin/env python
"""
    Name
       cmdGrep.py
       function: grep
    Synopsis
        searches a specified file for the specified text. 
        returns lines containing text to console or to output file is specified
    Description
        function parameters/variables
            flag '-l' - prints lines of file containing search term
            search term text string 
            search file - file to search line-by-line for the presence of the search term
            output file - optional - if given, creates & writes found lines to file
    Examples    
        grep -l bacon pig.txt baconforever.txt
                       
    """
import os, sys
from io import StringIO
from rich import print
from rich.console import Console

def grep(**kwargs): 
    """
    Name
       cmdGrep.py
       function: grep
    Synopsis
        searches a specified file for the specified text. 
        returns lines containing text to console or to output file is specified
    Description
        function parameters/variables
            flag '-l' - prints lines of file containing search term
            search term text string 
            search file - file to search line-by-line for the presence of the search term
            output file - optional - if given, creates & writes found lines to file
    Examples    
        grep -l bacon pig.txt baconforever.txt
        some cmd | grep -l bacon | some cmd  
                       
    """
    #print(kwargs)
    if kwargs['flags']:
        flag = kwargs['flags'][0]               # flag designator returns back lines or words that match the search term parameter
    else:
        flag = 'l'
    
    search_param = kwargs['params'][0]         # the search parameter text in file
     
    file_name = kwargs['params'][1]
    try: 
        with open(file_name, 'r') as f:  
            content = f.readlines()                          # Read in file
    except:
        try:
            content = StringIO(file_name).readlines()        # Read in string
        except:
            print("File does not exist")
            return
    console=Console()
    line_list = ""
    RED = '\033[91m'
    RESET = '\033[0m'
    for line in content:                 # Print last n lines
        if search_param in line:
            line_list+=line
    # add highlight to search term
    for line in line_list:
        line_with_highlight = line.replace(search_param, '[red]NOTBACON[/]')
        #print(line)
        console.print(line_with_highlight, end='')
        #f"{RED}{search_param}{RESET}".join(line.split(search_param))
        #print(line_with_highlight.strip())
    
    if not kwargs['stdin']:     
        #print(f'{line_with_highlight}')
        console.print(line_with_highlight, end='')
        #print(line_list.strip())
    else:
        return line_list.strip()
    
# for line in line_list:
#             # Highlight the search term in red
#             line_with_highlight = line.replace(search_param, f"[red]{search_param}[/red]")
#             print(line_with_highlight.strip())

    
if __name__ == "__main__":
    # test1 grep cmd alone with search term, search file, output file not being piped
    test1 = {'params': ['bacon','meat.txt','baconater.txt'],'flags':['l'],'stdin':False}
    # test2 grep cmd alone with search term, search file, output to screen not being piped
    test2 = {'params': ['bacon','meat.txt'],'flags':['l'],'stdin':False}
    # test3 grep cmd in cmd string with search term, search file, being piped
    test3 = {'params': ['bacon','meat.txt',''],'flags':['l'],'stdin':True}
    # test4 grep cmd last in cmd string with search term, search input from pipe, output to file/screen 
    test4 = {'params': ['bacon',''],'flags':[],'stdin':False}
    # test5 grep cmd in cmd string with search term, input from pipe , output to pipe
    test5 = {'params': ['bacon',''],'flags':[],'stdin':True}
   
    grep(**test2)


   
