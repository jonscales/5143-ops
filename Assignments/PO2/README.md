# File System
---

#### 16 Oct 2023
#### 5143 File System Project 

#### Group Members

- Marcos Lopez
- Patrick Mitchell
- Jon Scales

### Overview:
This is a project written in python that simulates a file system using a sqlite database. 

### Required Packages
- PrettyTable
- Rich
- SQLlite3

### Shell Program Files ###
|                  Program                   |            Description             |        Author         |
| :----------------------------------------: | :--------------------------------: | :-------------------: |
| [walkthrough.py](./walkthroughthewoods.py) |         main demo program          |   Jon, Marcos, Pat    |
|      [sqliteCRUD.py](./sqliteCRUD.py)      | methods to interface with database |   Marcos , Griffin    |
|    [filesysdata.csv](./filesysdata.csv)    |      data for database table       | Modified from Griffin |
|  [filesystem.sqlite](./filesystem.sqlite)  | sqlite table containing filesystem |           -           |
 
#### Instructions

- Run [walkthrough.py](./walkthrough.py) program, and various commands from the list below is executed with a variety of flags and parameters. 
                                     
### Commands List: ###
These commands are demonstrated in the walkthrough.py program

| Command |       Description        |       Notes       |
| :-----: | :----------------------: | :---------------: |
|   ls    |    directory listing     | flags -l, -a, -h  |
|  chmod  |    change permissions    | use triplet (777) |
|   pwd   |    working directory     |                   |
|   cd    |     change directory     |       cd ..       |
|  mkdir  |      make directory      |                   |
|   mv    |    move a file or dir    |                   |
|   cp    |       copy a file        |                   |
|   rm    |    remove file or dir    |     flags -r      |
| history | list history of commands |                   |

### References
- Dr. Giffin's code was a helpful starting point.
- Various authors made use of either ChatGPT or CoPilot for formatting, comments, or direction