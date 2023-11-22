#!/usr/bin/env python

#
# This file is used for the history command. It is responsible for reading and
# writing to the history file. It is also responsible for printing the history
# to the terminal.
#

history_file = '.history.txt'

class History:
    def __init__(self):
        self.load_history()

    def load_history(self):
        """Loads the history file into memory"""
        with open(history_file, 'r') as f:
            self.content=f.readlines()
            self.length = len(self.content)
            self.pos = self.length - 1
    def get_n_hist(self, n):
        """Returns the nth command from history"""
        return self.content[n].strip()
    def get_prev_hist(self):
        if self.pos > 1:
            self.pos -= 1
            return self.content[self.pos+1].strip()
        else:
            return ""
    
    def get_next_hist(self):
        if self.pos < self.length - 1:
            self.pos += 1
        return self.content[self.pos].strip()
    
    def add_history(self,cmd):
        with open(history_file, 'a') as f:
            f.write('\n'+str(cmd))
        self.load_history()

    def clear_history(self):
        with open(history_file, 'w') as f:
            f.write(' ')
        print("\nHistory cleared")
        self.load_history()


def history(**kwargs):
    """
    Usage: history [OPTION]... [FILE]...
        Returns the last 10 commands entered or the last n commands entered
    Options:
        -n, number all output lines
    Examples:
        history             Output last 10 commands entered
        history -n 5        Output last 5 commands entered
    """
    with open(history_file, 'r') as f:
        content=f.readlines()
        length = len(content)
        flag = kwargs.get('flags', None)
        if 'n' in flag:
            try:
                pos = int(kwargs['params'][0])
            except:
                pos = 10
            return content[-pos:]
        else:
            for i in range(len(content)):
                print(f'{i}. {content[i].strip()}')
            return content   

    print('\n'.join([str(readline.get_history_item(i + 1)) for i in range(readline.get_current_history_length())]))



if __name__=='__main__':
    print("\n")
    print("This is the history module")
    h = History()
    print(h.get_prev_hist())