#!/usr/bin/env python
"""
This file is the shell loop. It is responsible for capturing user input and
calling the appropriate functions. It also handles the arrow keys and backspace
key, history, and tab completion (maybe).
"""
import os
import sys
import getpass
from rich import print
from time import sleep
from cmd_pkg import *
from commandHelper import *


def main():
    cmdHelper = CommandsHelper()
    getch = Getch()                             # create instance of our getch class
    prompt = "$ "                               # set default prompt
    cmd = ""                                # empty cmd variable
    h = History()                           # create instance of our history class
    print_cmd(cmd)                          # print to terminal
    
    while True:                             # loop forever

        char = getch()                      # read a character (but don't print)

        if char == '\x03' or cmd == 'exit': # ctrl-c
            cmd = ""
            print_cmd(cmd)
            raise SystemExit("Goodbye.")
        
        # elif cmd == 'clear history':        # clear history
        #     print_cmd(str(cmd))                  
        #     sleep(0.5)    
        #     h.clear_history()
        #     cmd=""
        #     print_cmd("")    
        elif char == '\x7f':                # back space pressed
            cmd = cmd[:-1]
            print_cmd(cmd)
            
        elif char in '\x1b':                # arrow key pressed
            null = getch()                  # waste a character
            direction = getch()             # grab the direction
            
            if direction in 'A':            # up arrow pressed
                # get the PREVIOUS command from your history (if there is one)
                cmd =h.get_prev_hist()

                
            if direction in 'B':            # down arrow pressed
                # get the NEXT command from history (if there is one)
                cmd = h.get_next_hist()
            
            if direction in 'C':            # right arrow pressed    
                # move the cursor to the right on your command prompt line
                # prints out 'right' then erases it (just to show something)
                cmd += u"\u2192"
                print_cmd(cmd)
                sleep(0.1)
                cmd = cmd[:-1]

            if direction in 'D':            # left arrow pressed
                # moves the cursor to the left on your command prompt line
                # prints out 'left' then erases it (just to show something)
                cmd += u"\u2190"
                print_cmd(cmd)
                sleep(0.1)
                cmd = cmd[:-1]
            
            print_cmd(cmd)                  # print the command (again)

        elif char in '\r':                  # return pressed 
            print_cmd("")                   # print empty cmd prompt
            if cmd == '':
                print_cmd('\n')
                print_cmd('')
                continue
            elif cmd == 'clear history':        # clear history
                h.clear_history()
                print_cmd("")
                h.add_history(cmd)
                continue
            elif cmd.startswith('!'):                 # run a command from history
                    if cmd[1:].startswith('!'):         # if it starts with '!!'
                        cmd = h.get_n_hist(-2)
                        print_cmd(cmd)                 # run the second to last command
                        continue                                
                    else:
                        try:
                            cmd = h.get_n_hist(int(cmd[1:]))    # otherwise run the nth command
                            print_cmd(cmd)
                        except:
                            print_cmd(cmd)
                            print_cmd("Invalid history command")
                        continue
                
            print_cmd(str(cmd))                  
            sleep(0.5)    
            # Update history filepwd
            h.add_history(cmd)
            
            # Parse the command
            parsed_cmd = ParseCmd(cmd)
            allCmds = parsed_cmd.allCmds                     # parse the command
            print('')

            hold = ''                                           # initialize hold to empty string
            for cmd in allCmds:
                cmd['params'].append(hold)                      # add the hold to the params list
                if 'help' in cmd.get('flags',[]):               # if help is in the flags list
                    print(cmdHelper.help[cmd['name']])          # print the doc string
                    break                                       # break out of the loop                        
                
                if cmd['stdin'] :                               # if stdin is true
                    hold = cmdHelper.run(cmd)                   # save the output of the command to pass to the next command
                else:
                    cmdHelper.run(cmd)                   # otherwise just run the command
                    hold = ''
            if parsed_cmd.redirect:                             # if there is a redirect
                filename = "./" + parsed_cmd.fileName.strip()  # add the file name to the path
                with open(filename, 'w') as f:       # open the file
                    f.write(hold)                               # write the output to the file
            
            cmd = ""                                            # reset command to nothing (since we just executed it)
            
            #cmdHelper.run(cmd)

            print_cmd(cmd)                  # now print empty cmd prompt
        else:
            cmd += char                     # add typed character to our "cmd"
            print_cmd(cmd)                  # print the cmd out


def prompt():
    """
        This function returns the current working directory
        to be used as the prompt.
    """

    return "\033[92m" + "\u001b[1m" + getpass.getuser() + "\033[0m" + ": " + '\033[34m' + "\u001b[1m" + os.getcwd() + "\033[0m" + " $: " 


def print_cmd(cmd):
    """
        This function "cleans" off the command line, then prints
        whatever cmd that is passed to it to the bottom of the terminal.
    """
    padding = " " * 80
    sys.stdout.write("\r"+padding)
    sys.stdout.write("\r"+prompt()+ cmd)
    sys.stdout.flush()

if __name__ == '__main__':
    main()
