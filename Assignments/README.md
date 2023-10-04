# Shell 
---

#### 28 Sep 2023
#### 5143 Shell Project 

#### Group Members

- Marcos Lopez
- Patrick Mitchell
- Jon Scales

#### Overview:
This is a project written in python that implements a basic shell ......


#### Instructions

- Run the shell_loop.py program
- at the command prompt, enter any of the commands listed below
- to run multiple commands in sequence from the command prompt
    enter each command separate by a pipe ' | '
- output of sequential commands can be redirected into an output file
    by using a ' > ' after the last command.

#### Example Commands

$ ```any command --help``` -> gives the usage of the command

$ ```ls -lah```  -> gives a long listing of the curent directory showing 
                all files & directories in human readable format

$ ```ls -lah | grep bacon```  -> lists only those files with "bacon" in it somewhere

$ ```chmod 777 filename``` -> changes the permissions of the file 'filename' to 
                            all true  'rwxrwxrwx' 

$ ```up arrow```-> shows previous command typed at the prompt, multiple presses scrolls 
                back through command history

$ ```down arrow``` -> shows next command typed at the prompt if the up arrow had been used
                    to scroll back into the command history.  Down arrow scrolls forward 
                    through the command  history                                           


### Commands List: ###
Only these commands are supported by this Shell Program (shell_loop.py)

| command |    description    | Author | Notes |
| :-----: | :---------------: | :----: | :---: |
|   ls    | directory listing |    Marcos    |   usable flags -l, -a, -h   |
| chmod | change permissions | Jon Marcos |  |
|   pwd   | working directory |   Pat     |       |
|  cd  |     change directory      |  Jon, ChatGPT & Bourbon       |       |
| mkdir | make directory  | Jon, ChatGPT & Bourbon   |   |
| mv |  move a file or dir | Jon, ChatGPT & Bourbon   |   |
| cp | copy a file |   Jon, ChatGPT & Bourbon |   |
| rm | remove file or  dir  | Marcos  | usable flags -r  |
| wc | word or line count  | Pat  | usable flags  -l, -wc  |
| sort | alphabetize by line  | Pat  |   |
| cat | join 2 files  | Pat   |   |
| head | list 1st n lines of file  | Marcos  | usable flags   |
| tail | list last n lines of file  | Marcos  | usable flags  |
| less | list screen worth of lines  |  Jon, ChatGPT & Bourbon |   |
| history | list history of commands  | Marcos  |   |
| !x | run a specified cmd from history|Marcos  |  |
| grep | find a given string  | Jon, ChatGPT & Bourbon  | usable flags -l  |

### Shell Program Files ###
| Program | Description | Author |
| :-----: | :---------: | :----: |
| shell_loop.py | main shell program | Marcos | 
| parse.py | parses command | Marcos |
| commandHelper.py| help file for each command| Marcos|
| __init__.py| makes funct files available to shell_loop.py | Marcos|
| .history.py | contains cmd history| Marcos |
| cmdCat.py | concatenate function| Pat |
| cmdCd.py | change directory function | Jon |
| cmdChmod.py | modify permission function | Jon |
| cmdCp.py | copy function | Jon |
| cmdGrep.py | grep function | Marcos|
| cmdHead.py | head function | Marcos |
| cmdHist.py | history function | Marcos |
| cmdLess.py | less function | Jon |
| cmdLs.py | list directory function  | Marcos |
| cmdMkdir.py | make directory function | Jon |
| cmdMv.py | move function | Jon |
| cmdPwd.py | print working dir function | Pat |
| cmdRm.py | remove file function | Marcos |
| cmdSort.py | sort function | Pat |
| cmdTail.py | tail function | Marcos |
| cmdWc.py | word count function | Pat |

***References***
