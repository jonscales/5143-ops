#!/usr/bin/env python
"""
    Name
       cmdGrep.py
       function: grepme
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
def grep(**kwargs): 
    """
    Name
       cmdGrep.py
       function: grepme
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
    
    #check to see if the file exists OR if search content is being piped from previous cmd
    # try:
    #     search_file = kwargs['params'][1]       # file to search for parameter text
    # except FileNotFoundError:
    #     if not os.path.exists(kwargs['params'][1]):
    #         print(f"search file does not exist.")
       # return
    line_list = []     # create a list to contain all the lines containing the search param word
    toPipe=False       #  if the grep  output needs to be piped to another cmd, default is no piping
    if kwargs['stdin']: # if stdin = true, output should be piped to next cmd
        toPipe=True
   
    if kwargs['params'][-1] == '' and len(kwargs['params']) <3: # check to see if search source is coming from upstream piped command
        piped_input = kwargs['params'][-1].strip().split('\n')
        for line in piped_input:
            if search_param in line:
                print(line) # for testing
                line_list.append(line)

    else:   # run grep on specified file using specified flag of either -l (lines) or -w (words) ( is words even an option??)
        try:
            search_file = kwargs['params'][1]      # see if search file is an actual file
            with open(search_file, 'r') as search_file:     # open the search file                         
                if 'l' in flag:                             # read in lines from file                               
                    for line in search_file:
                     if search_param in line:
                        line_list.append(line)          # add each line containing search param to the list                      
        except FileNotFoundError:
            print(f"File '{search_file}' not found")
    
    if len(line_list) <1:                           # give feedback if term not found in file
            print(f"Search term not found")                              
    out_file=''
    if len(kwargs['params']) >3:
        out_file=kwargs['params'][2]
    try:                              
        if out_file:                                    # if needs to save to a new file
            with open(out_file,'w') as out_file:
                out_file.writelines(line_list)
        elif toPipe:                                    #if needs to be piped  stdin = true
            out_file+=''.join(line_list)
            print(out_file) #just to test test 4
            return out_file.strip()
        else:                                           #if just needs to print to screen test 5
            for line in line_list:
                format_out = ''.join(line_list)
            print(format_out.strip())
               
    except FileNotFoundError:
        print(f"Filename {search_file} not found. Check diretory path and spelling")     
       
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


   
