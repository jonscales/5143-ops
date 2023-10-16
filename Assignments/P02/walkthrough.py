"""
walkthrough.py provides a coded sequence of command line calls
that will do the following :
list with long, all, human readable flags
mkdir 
cd with dir name
cd .. to parent dir
pwd 
mv 
cp
rm with rf flags to remove dir
chmmod 
history
"""

import time
from rich import print
from rich.table import Table
from rich.box import SIMPLE
from sqliteCRUD import SQLiteCrud
from random import randint

class FileSys(SQLiteCrud):
    """
        This class represents a filesystem
        and uses the SQLiteCrud class to
        perform CRUD operations on the
        filesystem database.
    """
    def __init__(self, database, table, csv=None):
        super().__init__(database, table, csv)
        self.current_directory_name = '~'
        self.current_directory_id = [0]
        self.history={}  # initialized dictionary
        self.counter=1   # initialize counter
    
    def add_history(self, command):#WORKS
        """
        records a history of each command run
        this is recorded as a dictionary where each keyword corresponds to the 
        sequential use of the command
        
        This method will be called from within each command function and append an instance
        of that command function being called onto the dictionary. the method running along with 
        what ever file/directory names involved will be passed into the history_add method as a parameter

        a counter within the history_add method is used to autoincrement the keyword value
        
        A subsequent method, history() will print out the history dictionary
        """
        self.history[self.counter] = command  # append command to 
        self.counter += 1  

    def hist(self):#WORKS
        """ 
          prints out the history 
        """
        for key,value in self.history.items():
            print(f"{key}  {value}")
    
    def format_add(self,cmdname,cmdparams):#WORKS
       """ 
       creates a list of the params passed into any given function call so
       that they can be added the history listing
       i.e. 
       cd bananas
       
       in history
       
       10   cd bananas
       
       """
       return f"{cmdname}: {' '.join(cmdparams)}"
    
    def display_ls(self, long=False, hidden=False, readable=False):#WORKS
        """
            Displays the contents of the current directory

            Parameters:
                long (bool): Display the long format
                hidden (bool): Display hidden files
                readable (bool): Display file size in human readable format
        """
        
        table = Table(show_header=True, header_style="bold blue", box=SIMPLE)
        data  = self.read_data(self.table_name, condition_column="pid", condition_value=f"{self.current_directory_id[-1]}", order_by="Type, Filename")
        cmdparams=[" "]
        if not long:
            table = ""
            for row in data:
                if not row['Hidden']:
                    table += f"{row['Filename']:20}"
                cmdparams=[" "]
        else:
            cmdparams=[" -l"]
            table.add_column("Permissions", style="dim", width=12, justify="right")
            table.add_column("Owner", justify="center")
            table.add_column("_Group", justify="center")
            table.add_column("Size", justify="right")
            table.add_column("Created", justify="center")
            table.add_column("Modified", justify="center")
            table.add_column("Filename")
            if readable:
                for row in data:
                    row['Size'] = convert_size(row['Size'])
                    cmdparams=[" -lh"]
            if hidden:
                try:
                    dot = self.read_data(self.table, condition_column="id", condition_value=self.current_directory_id[-1], )
                    table.add_row(
                        dot[0]["Permissions"],
                        dot[0]["Owner"],
                        dot[0]["_Group"],
                        str(dot[0]["Size"]) if not readable else convert_size(dot[0]["Size"]),
                        dot[0]["Created_date"],
                        dot[0]["Modified_date"],
                        "."
                    )
                    double_dot = self.read_data(self.table, condition_column="id", condition_value=dot[0]["pid"])
                    table.add_row(
                        double_dot[0]["Permissions"],
                        double_dot[0]["Owner"],
                        double_dot[0]["_Group"],
                        str(double_dot[0]["Size"]) if not readable else convert_size(double_dot[0]["Size"]),
                        double_dot[0]["Created"],
                        double_dot[0]["Modified"],
                        ".."
                    )
                    cmdparams=[" -lah"]
                except:
                    pass
                for row in data:
                    if row['Hidden']:
                        table.add_row(
                            row["Permissions"],
                            row["Owner"],
                            row["_Group"],
                            str(row["Size"]),
                            row["Created_date"],
                            row["Modified_date"],
                            row["Filename"]
                        )
            for row in data:
                if not row['Hidden']:
                    table.add_row(
                        row["Permissions"],
                        row["Owner"],
                        row["_Group"],
                        str(row["Size"]),
                        row["Created_date"],
                        row["Modified_date"],
                        row["Filename"]
                    )

        #to record event in history
        cmdname='ls' 
        self.add_history(self.format_add(cmdname,cmdparams))
        
        print(table)
        self.display_pwd()
        time.sleep(5)

    def mkdir(self, directory, folder_name="New Folder"): #WORKS
        """
            Creates a new folder in the specified directory

            Parameters:
                directory (str): The current directory
                folder_name (str): The name of the new folder
        """
        current_directory = self.read_data(self.table_name, condition_column="pid", condition_value=self.current_directory_id)
        folder_exists = True if  self.read_data(self.table_name, condition_column="Filename", condition_value=folder_name) else False
        if folder_exists:
            #to record event in history
            cmdname='mkdir' 
            cmdparams=[directory, folder_name]
            self.add_history(self.format_add(cmdname,cmdparams))
            
            print("Folder already exists.")
            return
        else:
            data = {
                "pid": self.current_directory_id[-1],
                "Permissions": "drwxr-xr-x",
                "Owner": "Bob",
                "_Group": "Bob",
                "Size": 4096,
                "Type": "DIR",
                "Created_date":time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "Modified_date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "Filename": folder_name,
                "Hidden": 0, 
            }
            inserted_data = []
            for col in self.columns:
                if col == "id":
                    continue
                inserted_data.append(data[col])
            self.insert_data(self.table_name, tuple(inserted_data), tuple(self.columns[1:]))
            
            #to record event in history
            cmdname='mkdir' 
            cmdparams=[directory, folder_name]
            self.add_history(self.format_add(cmdname,cmdparams))
            print(f"Folder '{folder_name}' created.")
            time.sleep(1)

    def display_pwd(self): #WORKS
        """
        returns current working directory to the console
        """
        directory = self.current_directory_name
        #directory = self.get_path(self.parse_path(directory))

        #to record event in history
        cmdname='pwd'
        cmdparams=['']
        self.add_history(self.format_add(cmdname,cmdparams))
        
        print(f"[bold cyan]Current Directory:[/bold cyan] [green]{directory}[/green]")
        
        time.sleep(1)

    def chdir(self,new_directory): # WORKS
        """ 
        changes the current working directory to the new directory

        Params:
            directory: current working directory
            new_directory: new working directory
        """
        currdir=self.current_directory_id[-1]
        #print(f" current directory is {currdir}")
        # check if changing to subpaths
        
        newdirs = new_directory.split('/')
        newpath = newdirs[-1]  # this will be the last directory in the path we need the ID of
        for dir in newdirs:
            if dir=="":
                continue
            if '..' == dir:
                if len(self.current_directory_id)==1:
                    return
                self.current_directory_id.pop()
                temp=self.current_directory_name.split('/')
                temp.pop()
                self.current_directory_name="/".join(temp)
                continue
            
            verify = False

            dest_pid = db.get_id(self.table_name, self.current_directory_name.split("/")[-1])
            dir_data = db.read_data(self.table_name,"pid", dest_pid)
            for file in dir_data:
                if file["Filename"] == dir:
                    verify = True
            if verify:
                destpath=self.get_id(self.table_name, dir)

                #print(f"The new path is {destpath}")
                #print(f"Changing directories from {self.current_directory_name} id {currdir} to {dir} id {destpath}")
                #change current directory id
                self.current_directory_id.append(destpath)
                #print(f"The current directory is now {dir} with id {self.current_directory_id[-1]}")
                # somehow this needs to update a global parameter so all other commands now know what the current directory is
                #update the current path info for instance of db
                self.current_directory_name+=f"/{dir}"
            else:
                print(f"{new_directory} is not a valid directory")
                return
        #to record event in history
        cmdname='chdir'
        cmdparams=[new_directory]
        self.add_history(self.format_add(cmdname,cmdparams))
        time.sleep(2)

    def chmod(self,newperms, path_filename):
        """
        changes permissions of a specified file
        
        use triple number to specify desired permission
        7  sets rwx    
        6  sets rw-
        5  sets r-x
        4  sets r--
        3  sets -wx
        2  sets -w-
        1  sets --x
        0  sets ---        
        """ 
        dir=False
        # check if filename is a path or just filename
        if '/' in path_filename:
            dirs = path_filename.split('/')
            filename=dirs[-1]
            file_pid=dirs[-2]
            pid = self.get_id(self.table_name, file_pid)
        else:
            filename=path_filename
            pid = self.current_directory_id[-1]
 
        #get file data
        data = self.read_data(self.table_name,condition_column="Filename" ,condition_value=f"{filename}' AND pid = '{pid}")
        #print(f"Data is {data}")
          #check if filename exists
        if not data:
            print(f" Error:  File does not exist!")
            return
        
        verify = False
        for item in data:
            if data[0]['pid']==pid:
                verify=True        
        if not verify:
            print(f" Error:  File does not exist!")
            return

        #check if file is a directory  
        current_perms=data[0]["Permissions"]
        if current_perms[0]=='d':
            dir=True
            new_perms='d'
        else: 
            new_perms='-'

        permlist={
            '7': 'rwx',    
            '6':'rw-',
            '5':'r-x',
            '4':'r--',
            '3':'-wx',
            '2':'-w-',
            '1':'--x',
            '0':'---'   }
        for ch in newperms:
            new_perms+=permlist[ch]
        #print(f"New permissions are {new_perms}")    
        self.update_data(self.table_name,column="Permissions", new_value=new_perms,condition_column="id",condition_value=data[0]["id"])
        
        
        #to record event in history
        cmdname='chmod'
        cmdparams=[newperms, filename]
        self.add_history(self.format_add(cmdname,cmdparams))  

    def copy(self, path_filename=None, new_path_filename=None):#WORKS
        """
            copies the file to a new directory using the same filename or a new filename if given
            cp pictures /bananas
        """
        current_directory = self.current_directory_id[-1]
        # determine if path/filename or just filename
        #print(current_directory)
        if '/' in path_filename:
            dirs = path_filename.split('/')
            filename=dirs[-1]
            file_data = self.read_data(self.table_name, condition_column="Filename", condition_value=filename)  
            # Handle the case where the source file does not exist
            try:
                if file_data:
                    path = dirs[-2]  # this will be the last directory in the path we need the PID of
                    #get path PID 
                    path_id=self.get_id(self.table_name, path)
                    # print(path_id)
                    # current_directory = self.read_data(self.table_name, condition_column="pid", condition_value=path_id)
            except(FileNotFoundError):
                print(f"Error: Source file not found.")  
            
        else:
            filename = path_filename
            print(f"File to copy is: {filename}")
            file_data = self.read_data(self.table_name, condition_column="Filename", condition_value=filename) 
            print(f"{file_data}") 
            # Handle the case where the source file does not exist
            try:
                if file_data:
                   path = current_directory
            
            except(FileNotFoundError):
                print(f"Error: Source file not found.")          
    
        # determine new path and/or filename
        # should be specifying at least a new directory
        # is single directory, just directory name
        # if a path, there will be / in new path param
        # if giving a new filename, there will be a .ext
        # check if last term in new path have an extension? 
        # check for / in new path param
        if '/' in new_path_filename:
            newdirs = new_path_filename.split('/')
            if '.' in newdirs[-1]:
                newfilename=newdirs[-1]
                newpath = newdirs[-2]  # this will be the last directory in the path we need the PID of
            else:
                newpath = newdirs[-1]            
        else: 
            newpath = new_path_filename
            newfilename=filename 
            print(f"Copying {newfilename} to {newpath}")   
        # check to see if copying file into same directory - error
        try:
            if newpath != current_directory :     
                copy_pid=self.get_id(self.table_name, newpath)
                
                new_file_data = {
                    "pid": copy_pid, 
                    "Permissions": file_data[0]['Permissions'],
                    "Owner": file_data[0]['Owner'],
                    "_Group": file_data[0]['_Group'],
                    "Size": file_data[0]['Size'],
                    "Type": file_data[0]['Type'],
                    "Created_date":file_data[0]['Created_date'],
                    "Modified_date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    "Filename": newfilename,
                    "Hidden": 0                   
                }
                
                inserted_data = []
                for col in self.columns:
                    if col == "id":
                        continue
                    inserted_data.append(new_file_data[col])
                self.insert_data(self.table_name, tuple(inserted_data), tuple(self.columns[1:]))
        
        except(FileExistsError):
                print(f"File already exists. Can not copy file.")              

        #to record event in history
        
        cmdname='cp'
        cmdparams=[path_filename,new_path_filename]
        self.add_history(self.format_add(cmdname,cmdparams))
        time.sleep(2)
    
    def move(self,path_filename, new_directory):#WORKS
        """
        moves a file to a new directory
        """
        # get current pid 
        current_directory = self.current_directory_id[-1]
        # determine if path/filename or just filename 
        if '/' in path_filename:
            dirs = path_filename.split('/')
            filename=dirs[-1]
            file_data = self.read_data(self.table_name, condition_column="Filename", condition_value=filename)  
            # Handle source file does not exist
            try:
                if file_data:
                    currpath = dirs[-2]  # this will be the last directory in the path we need the PID of
                    #get path PID 
                    currpath_id=self.get_pid(self.table_name, currpath)
                    
                    #print(f"File to move is: {filename}")
                    #print(f"pid of file = {currpath_id}")
                    
            except(FileNotFoundError):
                print(f"Error: Source file not found.")  
            
        else:
            filename = path_filename
            #print(f"File to move is: {filename}")
            #print(f"file has pid = {current_directory}")
            file_data = self.read_data(self.table_name, condition_column="Filename", condition_value=filename) 
            #print(f"{file_data}") 
            # Handle the case where the source file does not exist
            try:
                if file_data:
                   currpath = current_directory
                   #print(f"File to move is: {filename}")
                   #print(f"file has pid = {currpath}")
            
            except(FileNotFoundError):
                print(f"Error: Source file not found.")

        # change current pid it to pid of new directory
        # check to see if multiple directories in path for move
        newdirs = new_directory.split('/')
        newpath = newdirs[-1]  # this will be the last directory in the path we need the PID of
        
        destpath=self.get_id(self.table_name, newpath)
        #print(f"{filename} will be moved to {new_directory} whose pid = {destpath}")

        # update table def update_data(self, table_name, column, new_value, condition_column, condition_value):
        self.update_data(self.table_name,"pid",destpath,condition_column="Filename",condition_value=filename)

        #to record event in history
        cmdname='mv'
        cmdparams=[path_filename,new_directory]
        self.add_history(self.format_add(cmdname,cmdparams))
        time.sleep(2)

    def remove(self, directory, filename, flag):
        """
            Removes a file or directory

            Parameters:
                directory (str): The current directory
                filename (str): The name of the file or directory to remove
                flag (bool): True if the directory should be removed recursively
        """

        # check if filename is a path or just filename
        if '/' in filename:
            dirs = filename.split('/')
            filename=dirs[-1]
            file_pid=dirs[-2]
        else:
            file_pid=self.current_directory_id[-1]

        if not flag:
            # check if file exists
            file_data = self.read_data(self.table_name, condition_column="Filename", condition_value=filename)
            if not file_data:
                print(f"Error: File '{filename}' does not exist.")
                return
            elif file_data[0]["Type"] == "DIR":
                    print(f"Error: '{filename}' is a directory. Use -r flag to remove.")
                    return
            else:
                # remove file
                self.delete_data(self.table_name, condition_column="Filename", condition_value=f"{filename}' AND pid = '{file_pid}")
                print(f"File '{filename}' removed.")

        else:
            # check if directory exists
            dir_data = self.read_data(self.table_name, condition_column="Filename", condition_value=filename)
            if not dir_data:
                print(f"Error: Directory '{filename}' does not exist.")
                return
            else:
                
                # check if directory
                if dir_data[0]["Type"] == "DIR":
                    files = self.read_data(self.table_name, condition_column="pid", condition_value=dir_data[0]["id"])
                    for files in files:
                        if files["Type"] == "DIR":
                            self.remove(directory, files["Filename"], True)
                        else:
                            self.remove(directory, files["Filename"], False)
                    # remove directory
                    self.delete_data(self.table_name, condition_column="Filename", condition_value=f"{filename}' AND pid = '{file_pid}")
                    print(f"Directory '{filename}' removed.")
                else:
                    print(f"Error: '{filename}' is not a directory.")
                    return

        #to record event in history
        cmdname='rm'
        cmdparams=[directory,filename]
        self.add_history(self.format_add(cmdname,cmdparams))

        pass

    def get_id(self, table, directory):#WORKS
        """
        returns the pid of the directory
        """
        id = self.read_data(table, condition_column="Filename", condition_value=directory)
        if not id:
            return None
        else:
            return id[0]['id']
    
    def get_directory(self, table, pid):#WORKS
        """
        returns the directory name of the pid
        """
        directory = self.read_data(table, condition_column="id", condition_value=pid)
        return directory[0]["Filename"]
    
    def parse_path(self, path):#WORKS
        """
            returns the directory and filename
        """
        dirs = path.split("/")
        pids = []
        for entry in dirs:
            if entry == "":
                continue
            else:
                pid =self.get_id(self.table_name, entry)
                if pid:
                    pids.append(pid)
                else:
                    print(f"Error: Directory '{entry}' not found.")
                    return
        return pids

    def get_path(self, arr):#WORKS
        """
            returns the path of the directory
        """
        path = ""
        pids = []
        for entry in arr:
            pid = self.read_data(self.table_name, condition_column="id", condition_value=entry)
            if pid:
                pids.append(pid[0]["pid"])
            else:
                print(f"Error: Directory '{entry}' not found.")
                return            
            path += "/" + self.get_directory(self.table_name, pid[0]["pid"])
        return path

def convert_size(size):#WORKS
    if size:
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                break
            size /= 1024.0
        return f"{size:.1f} {unit}"
    return size

    

if __name__ == "__main__":
    # Read in filesysdata.csv and make database
    csv = "filesysdata.csv"
    database = "project2.sqlite"
    table = "file_sys"
    
    db = FileSys(database, table, csv)
    timing = 3


    ####################################################################################
    ######  Final Test of all commands #################################################
    ####################################################################################
    
    # Test ls
    print("\n[bold blue]Command:[/bold blue] [green]ls[/green]")
    db.display_ls(long=False)


    # cd to linux/drivers/perfctr
    print("\n[bold blue]Command:[/bold blue] [green]cd linux/drivers/perfctr[/green]")
    db.chdir("linux/drivers/perfctr")
    print("\n[bold blue]Command:[/bold blue] [green]ls -l[/green]")
    db.display_ls(long=True)

    # long list with hidden files
    print("\n[bold blue]Command:[/bold blue] [green]ls -la[/green]")
    db.display_ls(long=True, hidden=True)

    # long list with human readable file size and hidden files
    print("\n[bold blue]Command:[/bold blue] [green]ls -lah[/green]")
    db.display_ls(long=True, hidden=True, readable=True)

    # make 'bananas' directory
    print("\n[bold blue]Command:[/bold blue] [green]mkdir bananas[/green]")
    db.mkdir("/", "bananas")
    time.sleep(timing)
    db.display_ls(long=True, hidden=True, readable=True)

    # make 'apples' directory
    print("\n[bold blue]Command:[/bold blue] [green]mkdir apples[/green]")
    db.mkdir("/", "apples")
    time.sleep(timing)
    db.display_ls(long=True, hidden=True, readable=True)

    # move 'somefile.txt' to 'bananas'
    print("\n[bold blue]Command:[/bold blue] [green]mv virtual_stub.c bananas[/green]")
    db.move("virtual_stub.c", "bananas")
    time.sleep(timing)

    # See that it is moved
    print("\n[bold blue]Command:[/bold blue] [green]ls -lah[/green]")
    time.sleep(timing)
    db.display_ls(long=True, hidden=True, readable=True)

    # change directory to 'bananas'
    print("\n[bold blue]Command:[/bold blue] [green]cd bananas[/green]")
    db.chdir("bananas")
    db.display_pwd()
    time.sleep(timing)
    db.display_ls(long=True, hidden=True, readable=True)

    # Go up one directory
    print("\n[bold blue]Command:[/bold blue] [green]cd ..[/green]")
    db.chdir("..")
    time.sleep(2)
    print("\n[bold blue]Command:[/bold blue] [green]pwd[/green]")
    db.display_pwd()
    time.sleep(timing)

    # copy 'bananas/virtual_stub.c' to 'otherfile.txt'
    print("\n[bold blue]Command:[/bold blue] [green]cp bananas/virtual_stub.c apples/new_file.txt[/green]")
    db.copy("bananas/virtual_stub.c", "apples/new_file.txt")
    time.sleep(timing)

    # Show new file
    print("\n[bold blue]Command:[/bold blue] [green]cd apples[/green]")
    db.chdir("apples")
    time.sleep(timing)
    db.display_ls(long=True, hidden=True, readable=True)

    # go up one directory
    print("\n[bold blue]Command:[/bold blue] [green]cd ..[/green]")
    db.chdir("..")
    db.display_pwd()
    time.sleep(timing)

    # remove 'bananas' directory
    print("\n[bold blue]Command:[/bold blue] [green]rm bananas[/green]")
    time.sleep(timing)
    db.remove("/", "bananas", False) 
    db.display_ls(long=True, hidden=True, readable=True)

    # remove 'bananas' directory
    print("\n[bold blue]Command:[/bold blue] [green]rm -r bananas[/green]")
    db.remove("/", "bananas", True)
    db.display_ls(long=True, hidden=True, readable=True)

    # show history
    print("\n[bold blue]Command:[/bold blue] [green]history[/green]")
    time.sleep(timing)
    db.hist()
    time.sleep(5)

    # change permissions of 'somefile.txt'
    print("\n[bold blue]Command:[/bold blue] [green]chmod 777 .global.c[/green]")
    db.chmod("666", ".global.c")
    db.display_ls(long=True, hidden=True, readable=True)

    # End of test
    #print("Walkthrough complete.")

    db.close_connection()
