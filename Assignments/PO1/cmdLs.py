##!/usr/bin/env python
"""
    Name
       cmdLs.py
       function: ls
    Synopsis
        lists the contents of a directory
    Examples    
        ls
        ls -l
        ls -a
        ls -h
"""
import os, sys, stat, datetime, pwd,grp

def ls(**kwargs):
    """
        ls command  : lists the contents of a directory 
        flags       : -l (long format)
                      -a (all files)
                      -h (human readable)
    """
    output = ""
    # Check for flags
    flags = kwargs.get('flags', ' ')
    
    long_format = False
    all_files = False
    human_readable = False

    try:
        for flag in flags:
            long_format = 'l' in flag
            if long_format:
                break
        for flag in flags:
            all_files = 'a' in flag
            if all_files:
                break
        for flag in flags:
            human_readable = 'h' in flag
            if human_readable:
                break
    except:
        pass
    # Get the current working directory
    current_directory = os.getcwd()
    # Get the contents of the directory
    if all_files:
        directory_contents = os.listdir(current_directory)
    else:
        directory_contents = [item for item in os.listdir(current_directory) if not item.startswith('.')]
    
    # Sort the directory contents for consistent output
    directory_contents.sort()
    # this only works when just an -l flag is given, but doesn't runn with -lah is given
    if long_format:
        for item in directory_contents:
            item_path = os.path.join(current_directory, item)
            item_stat = os.stat(item_path)
            permissions = stat.filemode(item_stat.st_mode)
            nlink = item_stat.st_nlink
            gid=os.getgid()
            group=grp.getgrgid(gid).gr_name
            uid = os.getuid()
            user=pwd.getpwuid(uid).pw_name
            size = item_stat.st_size
            
            if human_readable:
                size = _human_readable_size(size)
            if permissions[0] == 'd':
                color = "\033[34m"      # blue
            else:
                color = "\033[0m"       # white
            reset = "\033[0m"           # white
            modified_time = datetime.datetime.fromtimestamp(item_stat.st_mtime).strftime("%B %d, %Y %H:%M")
            modified_time = modified_time.split()
            modified_month = modified_time[0][:3]
            modified_day = modified_time[1].strip(',')
            modified_year = modified_time[2]
            modified_hour = modified_time[3].split(':')[0]
            modified_minute = modified_time[3].split(':')[1]
            
            output += f"{permissions:10} {nlink:4} {group:8} {user:8} {size:8} {modified_month:3} {modified_day:2} {modified_year:4} {modified_hour:2}:{modified_minute:2} {color}{item}{reset}\n"
            #output.append(f"{color} {permissions:10} {nlink:4} {group:8} {user:8} {size:8} {modified_month:3} {modified_day:2} {modified_year:4} {modified_hour:2}:{modified_minute:2} {item} {reset}")           
    else:
        for item in directory_contents:
            item_path = os.path.join(current_directory, item)
            item_stat = os.stat(item_path)
            permissions = stat.filemode(item_stat.st_mode)
            if permissions[0] == 'd':
                color = "\033[34m"      # blue
            else:
                color = "\033[0m"       # white
            output += f"{color} {item}\n"


    if not kwargs['stdin']:
        print(output.strip())
    return output.strip()

def _human_readable_size(size):
    # Convert size to human-readable format (e.g., 1.23MB)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            break
        size /= 1024.0

    return f"{int(size):6d} {unit:2}"

if __name__ == '__main__':
    sample = {'name': 'ls', 'flags': ['la'], 'params': [], 'stdin': False}
    output=ls(**sample)