#!/usr/bin/env python

class CmdParts:
    """
    This class is used to parse the command line arguments.
    """
    def __init__(self, cmd=None):
        self.cmd = ''
        self.params = []
        self.flags = []
        self.stdin = False #?? should this be stdout?  this is if the cmd action is being piped out??  should there be a self.stdin and self.stdout ?

    def asdict(self):                               # return a dictionary of the command parts
            return {'name':self.cmd,'params':self.params,'flags':self.flags,'stdin':self.stdin}

class ParseCmd:
    def __init__(self,cmd=None):
        self.cmd = cmd
        self.redirect = False
        self.fileName = None
        #self.cmd_list = self.cmd.split()
        #self.cmd_len = len(self.cmd_list)
        self.allCmds = []
        self.run()
    
    def run(self):
        if not self.cmd:
            print("No command entered")
            return
        self.checkRedirect(self.cmd)
        self.checkPipe(self.cmd)
        self.parse(self.cmd)
        return self.allCmds

    def checkRedirect(self, cmd=None):
        """
        This method checks if the command has a redirect symbol in it.
        """
        if not cmd:
            cmd = self.cmd.strip()
        if '>' in self.cmd:
            split_cmd = self.cmd.split('>')
            self.cmd = split_cmd[0]
            self.fileName = split_cmd[1]
            self.redirect = True
        return self.cmd
    
    def checkPipe(self, cmd=None):
        """
            This method checks if the command has a pipe symbol in it.
            It returns a list of commands.
            Ex: "ls -l /usr/bin | grep txt | wc | sort" returns
            ['ls -l /usr/bin','grep txt','wc','sort']
        """
        if not cmd:
            cmd = self.cmd
        if '|' in cmd:
            self.cmd = cmd.split('|')
            return self.cmd
        else:
            self.cmd = [cmd]
            return [cmd]
        
    def parse(self, cmd=None):
        """
            This method parses the command line arguments.
            It returns a list of dictionaries, each of which contains
            the command name, parameters, redirect information and flags.
        """
        allCmds = []                                    # list to hold all commands
        if not cmd:
            cmd = self.cmd
        length = len(self.cmd)

        for entry in self.cmd:                          # iterate over each command
            entry = entry.strip()                       # remove leading and trailing whitespace
            p = CmdParts() 
            p.cmd = entry.split()[0]                    # split the command into the command name and the rest
            c = entry.split()[1:]                       # split the rest into a list of words
            for words in c:
                if words.startswith('-'):               # if it is a flag
                    p.flags.append(words.lstrip('-'))   # add it to the flags list
                else:
                    p.params.append(words)              # otherwise add it to the params list
            if length > 1 and entry != self.cmd[-1]:        # if there is more than one command
                p.stdin = True                          # set stdin to True
            length -= 1                                 # decrement the length  
            
            allCmds.append(p.asdict())                  # add the command to the list
        
        if self.redirect:                               # if there is a redirect
            allCmds[-1]['stdin'] = True
        self.allCmds = allCmds

if __name__ == "__main__":
    from rich import print
    sample = "ls -l /usr/bin | mkdir banana.txt | wc | sort > file1.txt"
    print(ParseCmd(sample).allCmds)
