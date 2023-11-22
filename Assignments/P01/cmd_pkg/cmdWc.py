# Word count program
from io import StringIO
"""
    Name
        wc - word count or line count of a file

    Synopsis
        wc [option] [filename]

    Description
        -l counts the number of lines in a file
        -w counts the number of words in a file

    Examples
        wd -l filename.txt
            counts the number of line in the file filename.txt

        wd -w filename.txt
            counts the number of words in the file filename.txt
                
    """
def wc(**kwarg):
    """
    Name
        wc - word count or line count of a file

    Synopsis
        wc [option] [filename]

    Description
        -l counts the number of lines in a file
        -w counts the number of words in a file

    Examples
        wd -l filename.txt
            counts the number of line in the file filename.txt

        wd -w filename.txt
            counts the number of words in the file filename.txt
                
    """
    #print(fname)
    #print(flags)
    try:
        with open(kwarg['params'][0],'r') as f:
            content=f.read()
        fileName = kwarg['params'][0]
    except:
        with StringIO(kwarg['params'][0]) as f:
            content=f.read()
        fileName = ''
    # find the number of lines, words, and characters
    nw=len(content.split())
    nl=len(content.split('\n'))
    nc=len(content)

    flags = kwarg.get('flags', '')

    # initialize output list
    output = ""

    # Default the output to empty strings
    nl_out = ''
    nw_out = ''
    nc_out = ''

    # Default the flags to False
    nl_flag = False
    nw_flag = False
    nc_flag = False

    try:
        for flag in flags:
            nl_flag = 'l' in flag
            if nl_flag:
                nl_out = nl
                break
        for flag in flags:
            nw_flag = 'w' in flag
            if nw_flag:
                nw_out = nw
                break
        for flag in flags:
            nc_flag = 'c' in flag
            if nc_flag:
                nc_out = nc
                break
    except:
        pass
    if not nl_flag and not nw_flag and not nc_flag:
        nl_out = nl
        nw_out = nw
        nc_out = nc

    output += f"{nl_out} {nw_out} {nc_out} {fileName}"
    
    #if no | or > then
    if not kwarg['stdin']: 
        print(output)
    return output
    
    
    
if __name__=='__main__':
    with open('pig.txt','r') as f:
        content=f.read()
    thing={'name':' ','params':[content],'flags':[' '], 'stdin':True}
    print(wc(**thing))