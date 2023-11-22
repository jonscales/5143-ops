# Sort for shell
"""
Usage:
    sort filename

    Sorts filename by line in alphabetic order. Uppercases are treated as lowercase

    
"""
from io import StringIO
def sort(**kwargs):
    """
    Usage:
        sort filename
        Sorts filename by line in alphabetic order. Uppercases are treated as lowercase   
"""
    try:
        with open(kwargs['params'][0],'r') as f:
            content=f.read()  
    except:
        with StringIO(kwargs['params'][0]) as f:
            content=f.read()

    data=content.split('\n')
    #print(data)
    slist=sorted(data, key=str.lower)
    
    output = ""
    for i in slist:
        output += i + '\n'

    if not kwargs['stdin']:
        print(output.strip())
    else:
        return output

if __name__=='__main__':
    thing={'name':' ','params':['meat.txt'],'flags':[' '], 'stdin':False}
    sort(**thing)    