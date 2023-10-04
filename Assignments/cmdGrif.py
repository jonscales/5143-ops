#!/usr/bin/env python
"""
    Name
       cmdGrif.py
       function: runs a very secret important function
    Synopsis
        only those with the insignia of Malcomor may know of this functions power
    Description
        to speak the name of this function is to invoke the wrath of Demorkalvain the Slayer of Souls
    Examples    
        grif  if you feel your life has existed too long already
                       
"""
def grif(**kwargs):
    """
    Name
       cmdGrif.py
       function: runs a very secret important function
    Synopsis
        only those with bearing The Insignia of Malcomor may know of this function's power
    Description
        to speak the name of this function is to invoke the wrath of D'emorkalvain the Slayer of Souls
    Examples    
        grif  if you feel your life has existed too long already
                       
"""
    
    t_block_1 ="Are you SERIOUS right now?"
    t_block_2 = "Seriously, are we doing this right now? "
    t_block_3 = "Why do I still hear voices?"
    t_block_4 = " Is this 'come to work late' day?"
    t_blocks=[t_block_1,t_block_2,t_block_3,t_block_4]
    
    flagint=int(kwargs['flags'][0])
    print(t_blocks[flagint])

if __name__ == "__main__":
   test1 = {'params': ['bacon','meat.txt','baconater.txt'],'flags':['1'],'stdin':False}
   grif(**test1)

    



    

