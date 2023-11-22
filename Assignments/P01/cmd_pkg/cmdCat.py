from io import StringIO
def cat(**kwargs):
    """
    Usage: cat [OPTION]... [FILE]...
    Concatenate FILE(s) to standard output.

    Options:
 
        -n                  number all output lines
  
    Examples:
        cat file1           Output file1 contents to standard output
        cat file1 file2     Output file1 contents to standard output, then file2 to standard output
        cat -n file1        Output file1 contents number all output lines    
    """
    output = ""
    if not kwargs['flags']:                             # if no flags are given, default to -n
        kwargs['flags'].append(' ')                     
    for t in range(len(kwargs['params'])):              # loop through all the files given
        try:                                            # try to open the file
            with open(kwargs['params'][t],'r') as f:    # if it is a file, read it
            #print(len(kwargs['params']))
                if t == 0:                              # if it is the first file, set content to the file contents
                    content=f.read()
                else :                                  # otherwise, append the file contents to the content list
                    content += f.read()
        except:                                         # if it is not a file, it is a string
            with StringIO(kwargs['params'][t]) as f:    # read the string
                if t == 0:
                    content=f.read()                    # if it is the first string, set content to the string contents
                else :
                    content += f.read()                 # otherwise, append the string contents to the content list
    content = content.split('\n')                       # split the content into a list of lines
    
    for i in range(len(content)):
        if 'n' in kwargs['flags'][0]:
            output += f"{i+1}. {content[i]}" + '\n'     # if the -n flag is given, print the line number and the line
        else:
            output+= content[i]  + '\n'                 # otherwise, just print the line
    
    if not kwargs['stdin']:
        print(output.strip())
    else:
        return output

if __name__=='__main__':
    thing={'name':' ','params':['pig.txt','meat.txt'],'flags':['n'], 'stdin':True}
    cat(**thing)