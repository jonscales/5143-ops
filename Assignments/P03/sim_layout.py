import os
from rich import print
from rich.text import Text
import time
import csv
import argparse
from rich.table import Table
from rich.live import Live
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel




class PCB:
    """
    This class generates a process control block (PCB) from information read in from 
    a data file. The attributes are passed to PCB as the pcb is
    generated by the readData method of the Simulator class. 
    """
    def __init__(self,pid,at,priority,cpubursts,iobursts):
        """
        Initializes a PCB instance
        """
        self.pid = pid     
        self.priority = priority     
        self.arrivalTime = int(at)
        self.cpubursts = [int(burst) for burst in cpubursts]   
        self.iobursts = [int(burst) for burst in iobursts]
        self.currBurstType = 'CPU'
        self.state='New'
        self.waitTime = 0
        self.readyTime = 0
        self.cpuTime = sum(self.cpubursts)
        self.ioTime = sum(self.iobursts)
        self.sliceTimer = 0
        self.remainingCPUTime = 0
        self.remainingIOTime = 0
        self.TAT = self.getTotalTime()

    def setTimeEnter(self,clock):
        self.timeEnter = clock.currentTime()
        return self.timeEnter
    
    def setTimeExit(self,clock):
        self.timeExit = clock.currentTime()
        return self.timeExit
    
    def setTAT(self):
        self.TAT = self.timeExit - self.timeEnter
        return self.TAT

    def incrementReadyTime(self):
        """
        increments the readyTime variable.  
        readyTime is the time PCB spends in the ready queue prior to entering CPU
        """
        self.readyTime += 1 

    def incrementWaitTime(self):
        """
        increments the waitTime variable.   
        readyTime is the time PCB spends in the wait queue prior to entering IO
        """
        self.waitTime += 1       
   
    
    def changeState(self, new_state):
        """
        changes state attribute which is the current queue location of the PCB
        """
        self.state = new_state

    def getCurrBurst(self):
        """ returns the current burst for the PCB"""
        if self.currBurstIs=='CPU':
            return self.cpubursts[self.currBurstIndex]
        elif self.currBurstIs =='IO':
            return self.iobursts[self.currBurstIndex]

    def getCurrentBurstTime(self):
        return self.bursts[self.currBurstIndex]
        
    def getTotalTime(self):
        """
        returns the total time the PCB spends in the system
        cpu time + io time + wait time + ready time + new time (1)
        """
        total = self.cpuTime + self.ioTime + self.readyTime + self.waitTime + 1
        self.TAT = total
        return total
    
    def getWaitTime(self):
        """
        returns the total time PCB spend in the wait queue
        """
        return self.waitTime  
    
    def getReadyTime(self):
        """
        returns the total time PCB spend in the ready (wait) queue
        """
        return self.readyTime  
    
    def cpu_ioRatio(self):
        """
        returns the ratio of CPU to IO times
        """
        return round((self.cpuTime/self.ioTime),2)
    
    def run_idleRatio(self):
        """
        returns the ratio of run (CPU + IO ) time to (wait + ready) time
        """
        if self.waitTime + self.readyTime == 0:
            return 0
        else:
            return round((self.cpuTime + self.ioTime)/(self.readyTime + self.waitTime),2)
    
    def getcpu_util(self):
            """
            returns the cpu utilization ( % of time spent in CPU)
            """
            return round((self.cpuTime /self.getTotalTime()*100),2)
    
    def __str__(self):
        """
        Used only for initial testing
        Will print each PCB in the processes dictionary on a line as :
        PID # : process information.  Can do this as either a simple list of 
        information or an itemized list of all burst times. 
        """
        # simple return list
        #return f"[red]AT:[/red] {self.arrivalTime}, [blue]PID:[/blue] {self.pid}, [green]Priority:[/green] {self.priority:2}, [yellow]# CPU bursts:[/yellow] {self.noCpuBursts}, [yellow]CPU Time =[/yellow] {self.getTotCpuTime()} [magenta]# IO Bursts:[/magenta] {self.noIoBursts} [magenta]IO Time=[/magenta] {self.getTotIoTime()}"
        #burst itemized list
        return f"[red]AT:[/red] {self.arrivalTime}, [green]Priority:[/green] {self.priority:2}, [yellow]CPU:[/yellow] {self.cpubursts}, [magenta]IO:[/magenta] {self.iobursts}"
        
class SysClock:
    """
    This class creates a class-level variable called clock.
    The clock's value is used to drive the looping of the
    PCBs within the simulated scheduler.
    """
    _shared_state = {}
    def __init__(self):
        """
        creates the clock shared state variable
        """
        self.__dict__ = self._shared_state
        if not 'clock' in self.__dict__: 
            self.clock = 0

    def advanceClock(self, tick=1):
        """
        advances the clock +1
        """
        self.clock += tick
           
    def currentTime(self):
        """
        returns the currentTime (clock value)
        """
        return self.clock   
    
class Stats:
    """
    The class' methods display the stats associated with the movement of PCB
    through the schedular and generates a .csv output file.
    """    
    def __init__(self, processes, clock, num_cpus, num_ios, alg, output):
        """
        Stats initialization
        """
        statConsole = Console()
        self.terminal_width =statConsole.width
        self.processes = processes
        self.simType = alg
        self.clock = clock
        self.num_cpus = num_cpus
        self.num_ios = num_ios
        self.output = str(output)
        outputParts = output.split('.')
        outFileName= (f'{alg}_{outputParts[0]}_{num_cpus}_{num_ios}_{time.strftime("%m%d-%H%M")}.csv')
        self.statTable(clock)
        self.summaryTable(clock, outFileName)
        self.statFileWriter(clock, self.simType, outFileName)

    def statTable(self, clock)-> Table:
        """
        generates & displays a table showing the total clock time for completing all PCBs
        generates & displays a table with various stats from each PCB
        """
        #build a rich table
        # Create the table        
        sClock=str(self.clock.currentTime())
        sortedProcesses = sorted(self.processes, key=lambda pcb: pcb.TAT)
        statTable = Table(show_header=True,width=int(self.terminal_width*.8)) # uses the add_column information to create column headings. 
        statTable.add_column(f'[bold blue]PID[/bold blue]', width=int(self.terminal_width*.1),justify='center')
        statTable.add_column(f'[bold][red]Priority[/red][/bold]',  width=int(self.terminal_width*.1),justify='center')
        statTable.add_column(f'[bold][cyan]Total Time[/cyan][/bold]',  width=int(self.terminal_width*.1),justify='center')
        statTable.add_column(f'[bold][magenta]Ready Time[/magenta][/bold]',  width=int(self.terminal_width*.1),justify='center')
        statTable.add_column(f'[bold][green]CPU Time[/green][/bold]',  width=int(self.terminal_width*.1),justify='center')
        statTable.add_column(f'[bold][magenta]Wait Time[/magenta][/bold]',  width=int(self.terminal_width*.1),justify='center')
        statTable.add_column(f'[bold][green]IO Time[/green][/bold]',  width=int(self.terminal_width*.1),justify='center')
        statTable.add_column(f'[bold][red]CPU Util[/red][/bold]',  width=int(self.terminal_width*.1),justify='center')
        statTable.add_column(f'[bold blue]CPU/IO[/bold blue]', width=int(self.terminal_width*.1),justify='center')
        statTable.add_column(f'[bold cyan]Run/Idle[/bold cyan]', width=int(self.terminal_width*.1),justify='center')
                             
        #statTable.add_row(f'Total Processes Run Time: [bold][yellow]{sClock}[/yellow][/bold]')
        for pcb in sortedProcesses:
            statTable.add_row(
                str(pcb.pid),
                str(pcb.priority),
                str(pcb.getTotalTime()),
                str(pcb.getReadyTime()),
                str(pcb.cpuTime),
                str(pcb.getWaitTime()),
                str(pcb.ioTime),
                str(pcb.getcpu_util()),
                str(pcb.cpu_ioRatio()),
                str(pcb.run_idleRatio())
                )
        print(f'[bold green]Process Run Attribute Data[/bold green]')       
        print(statTable)
        return statTable
    
    def statFileWriter(self, clock, alg, outFileName):
        """
        Generates a .csv output file with a name based on the algorithim type 
        and the input filename. 
        """ 
        with open(os.path.join('outputs', outFileName), 'w', newline='') as csvfile:
            fieldnames = ['Input filename','Algorithm','Number of CPUs','Number of IOs',"Process ID", "Total Time", "Ready Time", "CPU Time", "IO Time", "Wait Time","CPU Util", "CPU/IO", "Run/Idle"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            first_row = {"Input filename": self.output,
                         'Algorithm': alg,
                         'Number of CPUs': self.num_cpus,
                         'Number of IOs':self.num_ios
                        }
            writer.writerow(first_row)
            
            # Write the header row to the CSV file
            writer.writeheader()

            # Write data for each PCB
            for pcb in self.processes:
                data = {
                    'Process ID': pcb.pid,
                    'Total Time': pcb.getTotalTime(),
                    'Ready Time':pcb.getReadyTime(),
                    'CPU Time': pcb.cpuTime,
                    'Wait Time' : pcb.waitTime,
                    'IO Time' : pcb.ioTime,
                    'CPU Util':pcb.getcpu_util(),
                    'CPU/IO': pcb.cpu_ioRatio(),
                    'Run/Idle': pcb.run_idleRatio()                  
                        }
                writer.writerow(data) 

    def summaryTable(self, clock, outFileName) -> Table:
        """
        generates & displays a table summarizing the various stats from the stats Table
        """
        #stats calcs
        total_cpu_time = 0
        total_wait_time =0
        total_ready_time=0
        total_tat_time = 0
        aveCpuUtil=''
        aveWaitTime=''
        aveReadyTime=''
        aveTat=''
        for pcb in self.processes:
            total_cpu_time += pcb.cpuTime
            total_wait_time += pcb.waitTime
            total_ready_time += pcb.readyTime
            total_tat_time += pcb.TAT
        cpus = str(self.num_cpus)
        ios=str(self.num_ios)
        aveCpuUtil = str(round(total_cpu_time/(self.num_cpus * clock.currentTime())*100,2))
        aveWaitTime = str(round((total_wait_time)/len(self.processes),2))
        aveReadyTime = str(round((total_ready_time)/len(self.processes),2))
        aveTat=str(round((total_tat_time)/len(self.processes),2))

        summaryTable  = Table(show_header=True) # uses the add_column information to create column headings.
        summaryTable.add_column(f'[bold][green]Summary Statistics Table[/bold][/green]',width=int(self.terminal_width*.8),justify='center') 
        summaryTable.add_row(f'Number of CPUs : [bold red]{cpus}[/]')
        summaryTable.add_row(f'Number of I/O Devices : [bold yellow] {ios}[/]')
        summaryTable.add_row(f"CPU Utilization: [bold green]{aveCpuUtil} %[/]")
        summaryTable.add_row(f"Avg Wait Time: [bold magenta]{aveWaitTime}[/]")
        summaryTable.add_row(f"Avg Ready Time: [bold bright_magenta]{aveReadyTime}[/]")
        summaryTable.add_row(f"Avg TAT: [bold deep_pink4]{aveTat}[/]")
        summaryTable.add_row(f'Run data saved as[bold orange3] {outFileName}[/]')
        print(summaryTable)
        return summaryTable

class Simulator:    
    """
        This class is the main simulator operator
        methods to:
        read in the data from a file
        run the simulation loop
    """
    def __init__(self, datfile, alg="FCFS", num_cpus=1, num_ios=1, ts=5, sleep=0.1, outputfile=f'Sim_{time.strftime("%Y%m%d-%H%M%S")}.csv'):
        """
        Simulator initialization
        """
        # Initialize the Parameters
        if alg == "RR":
            self.timeSlice=int(ts)
        self.datfile = datfile
        self.num_cpus =int(num_cpus)
        self.num_ios = int(num_ios)
        self.sleepTime = float(sleep)
        self.outputfile = outputfile
        self.alg = alg
        # Read in the data
        self.processes = []
        self.readData()

        # Initialize the Queues
        self.newQueue = []
        self.readyQueue =[]
        self.CPUQueue =[]
        self.IOQueue = []
        self.waitQueue = []
        self.finishedQueue =[]
        simconsole=Console()
        self.terminal_width = simconsole.width
        self.clock = SysClock()   
        self.simLoop()

    def getProcesses(self):
        """
        returns the processes dictionary
        """
        return self.processes
    
    def readData(self):
        """
        reads in data from a datafile containing PCB process parameters
        produces a dictionary named processes using the process ID number (pid)
        in each processes parameters as the key and instantiates an instance of a
        PCB class for each process, populating that PCB with the parameters for 
        arrival time, priority, cpu bursts list & io bursts list.
        """
        with open(self.datfile) as f:
            self.data = f.read().split("\n")

        for process in self.data:
            if len(process) > 0:
                parts = process.split()             # split the line into parts
                arrival = parts[0]                  # arrival time is the first part
                pid = parts[1]                      # pid is the second part
                priority = int(parts[2][1:])        # priority is the third part
                cpubursts = []                      # initialize the cpu burst list
                iobursts = []                       # initialize the io burst list
                
                # Split the remaining parts into cpu and io bursts
                for i in range(len(parts[3:])):
                    if i % 2 == 0:
                        cpubursts.append(parts[3:][i])
                    else:
                        iobursts.append(parts[3:][i])

                # Createa Dictionary of all processes with PID as key and values are PCBs
                self.processes.append(PCB(pid, arrival, priority, cpubursts, iobursts))
        return self.processes
    
    def simLoop(self):
        """
        This method runs the Schedular Simulation Loop
        """
        complete = False            # flag to indicate if the simulation is complete
        loopIteration = 0           # loop iteration counter
        # panel layout 
        layout = Layout()
        console = Console()
        terminal_width = console.width
        os.system('cls' if os.name == 'nt' else 'clear')
        header_panel = Panel(self.headTable(self.datfile, self.num_cpus, self.num_ios), expand=True, border_style="blue")
        progress_panel = Panel(self.generateTable(self.clock.currentTime()),expand=True, border_style="green")
        messages_panel= Panel(self.messagesTable([]), expand=True, border_style='red')
    
        layout.split_column(
            Layout(name="header",size=10),
            Layout(name="body",size=20)
                )
        layout["header"].update(header_panel)
        layout["body"].split_row(Layout(name="progress",ratio=2), Layout(name="messages",ratio=1))
        layout["body"]["progress"].update(progress_panel)
        layout["body"]["messages"].update(messages_panel)
        messages=[]
        #initiate a live display to show the processes
        with Live(layout, refresh_per_second=10) as live:
            #print(f'welcome to live')
            complete=False
            #time.sleep(self.sleepTime)
            
            # Begin Simulation Loop
            while not complete:         # loop until all processes are complete
                # Increment times for readyQueue and waitQueue PCBs
                if self.readyQueue:
                    for pcb in self.readyQueue:
                        pcb.changeState('Ready')
                        if self.alg == "PB":
                            self.readyQueue.sort(key=lambda pcb: pcb.priority, reverse=True)
                            if pcb.waitTime>=pcb.cpuTime:
                                pcb.priority+=1
                        pcb.incrementReadyTime()
                
                if self.waitQueue:
                    for pcb in self.waitQueue:
                        pcb.changeState('Wait')
                        pcb.incrementWaitTime()

                # Move anything from New Queue to Ready Queue
                if self.newQueue:
                    for pcb in self.newQueue:
                        pcb.changeState('Ready')
                        m0=f'At time[bold yellow] {self.clock.currentTime()}[/]: [bold blue]PCB {pcb.pid}[/] moved to [bold magenta]ready[/]'
                        messages.append(m0)
                        self.readyQueue.append(pcb)
                    self.newQueue = []

                # Check for new proccesses if pcb arrival time == clock time
                # Move any new processes to the newQueue
                for pcb in self.processes:
                    if pcb.arrivalTime == self.clock.currentTime():
                        self.newQueue.append(pcb)
                        # self.processes.remove(pcb)
                        pcb.changeState('New')
                        m1=f'At time[bold yellow] {self.clock.currentTime()}[/]: [bold blue]PCB {pcb.pid}[/] entered system'
                        messages.append(m1)

                # Decrement current CPU and IO processes bursts values
                if self.CPUQueue:
                    for pcb in self.CPUQueue:
                        if pcb.cpubursts:
                            pcb.cpubursts[0] -=1
                            pcb.remainingCPUTime = pcb.cpubursts[0]
                            if self.alg == "RR":
                                pcb.sliceTimer += 1

                if self.IOQueue:
                    for pcb in self.IOQueue:
                        if pcb.iobursts:
                            pcb.iobursts[0] -=1
                            pcb.remainingIOTime = pcb.iobursts[0]

                # Check processes in CPU (FCFS)
                if self.alg == "FCFS" or self.alg == "PB":
                    if self.CPUQueue:
                        for pcb in self.CPUQueue:
                            if pcb.cpubursts[0] <= 0:
                                if len(pcb.cpubursts) <= 1:
                                    pcb.changeState('Finished')
                                    self.finishedQueue.append(pcb)
                                    self.CPUQueue.remove(pcb)
                                    m2=f'At time[bold yellow] {self.clock.currentTime()}[/]: [bold blue]PCB {pcb.pid}[/] [bold red]terminated[/]'
                                    messages.append(m2)
                                else:
                                    self.waitQueue.append(pcb)
                                    pcb.changeState('Wait')
                                    m3=f'At time[bold yellow] {self.clock.currentTime()}[/]: [bold blue]PCB {pcb.pid}[/] moved to [bold magenta] wait[/]'
                                    messages.append(m3)
                                    if pcb.cpubursts:
                                        pcb.cpubursts.pop(0)

                        self.CPUQueue = [pcb for pcb in self.CPUQueue if pcb.state == "CPU"]

                        # Move Ready Queue to CPU Queue
                        if self.readyQueue and loopIteration >=1 and (not self.CPUQueue or len(self.CPUQueue)< self.num_cpus):
                            num_to_assign = min(self.num_cpus - len(self.CPUQueue), len(self.readyQueue))
                            next_processes = self.readyQueue[:num_to_assign]
                            self.CPUQueue.extend(next_processes)
                            for pcb in next_processes:
                                pcb.changeState('CPU')
                                m4=f'At time[bold yellow] {self.clock.currentTime()}[/]: [bold blue]PCB {pcb.pid}[/] entered [bold green]CPU[/]'
                                messages.append(m4)
                            self.readyQueue = self.readyQueue[num_to_assign:]
                        else:
                            if loopIteration >=1 and not self.readyQueue and not self.IOQueue and not self.CPUQueue and not self.waitQueue:
                                complete = True
                                break
                    else:
                        if self.readyQueue and (not self.CPUQueue or len(self.CPUQueue) < self.num_cpus):
                            num_to_assign = min(self.num_cpus - len(self.CPUQueue), len(self.readyQueue))
                            next_processes = self.readyQueue[:num_to_assign]
                            self.CPUQueue.extend(next_processes)
                            for pcb in next_processes:
                                pcb.changeState('CPU')
                                m5=f'At time[bold yellow] {self.clock.currentTime()}[/]: [bold blue]PCB {pcb.pid}[/] entered [bold green]CPU[/]'
                                messages.append(m5)
                            self.readyQueue = self.readyQueue[num_to_assign:]
                        else:
                            if loopIteration > 1 and not self.readyQueue and not self.IOQueue and not self.CPUQueue and not self.waitQueue:
                                complete = True
                                break

                elif self.alg == "RR":
                    if self.CPUQueue:
                        for pcb in self.CPUQueue:
                            if pcb.cpubursts[0] == 0:
                                if len(pcb.cpubursts) <= 1:
                                    pcb.changeState('Finished')
                                    m6=f'At time[bold yellow] {self.clock.currentTime()}[/]: [bold blue]PCB {pcb.pid}[/] [bold red]terminated[/]'
                                    messages.append(m6)
                                    pcb.setTimeExit(self.clock)
                                    pcb.getTotalTime()
                                    self.finishedQueue.append(pcb)
                                    pcb.cpubursts.pop(0)
                                else:
                                    self.waitQueue.append(pcb)
                                    pcb.changeState('Wait')
                                    m6a=f'At time[bold yellow] {self.clock.currentTime()}[/]: [bold blue]PCB {pcb.pid}[/] moved to [bold magenta] wait[/]'
                                    messages.append(m6a)
                                    if pcb.cpubursts:
                                        pcb.cpubursts.pop(0)
                            else:
                                if pcb.cpubursts:
                                    if pcb.cpubursts[0] != 0:
                                        if pcb.sliceTimer == self.timeSlice:
                                            self.readyQueue.append(pcb)
                                            pcb.changeState('Ready')
                                            m7=f'At [bold yellow]{self.clock.currentTime()}[/]: [bold blue] PCB {pcb.pid}[/] [bold orange_red1]timed out, moved to ready[/]'
                                            messages.append(m7)
                                            pcb.sliceTimer = 0
                                    else:
                                        self.waitQueue.append(pcb)
                                        pcb.changeState('Wait')
                                        m8=f'At time[bold yellow] {self.clock.currentTime()}[/]: [bold blue]PCB {pcb.pid}[/] moved to [bold magenta] wait[/]'
                                        messages.append(m8)
                                        if pcb.cpubursts:
                                            pcb.cpubursts.pop(0)
                        
                        self.CPUQueue = [pcb for pcb in self.CPUQueue if pcb.state == "CPU"]
                        
                        if self.readyQueue and (not self.CPUQueue or len(self.CPUQueue) < self.num_cpus):   # are processes in readyqueue & is CPU not full
                            num_to_assign = min(self.num_cpus - len(self.CPUQueue), len(self.readyQueue))
                            next_processes = self.readyQueue[:num_to_assign]                                # get # of process from ready queue needed to fill CPU
                            self.CPUQueue.extend(next_processes)                                            # move next processes to the CPU 
                            for pcb in next_processes:
                                pcb.changeState('CPU')
                                m9=f'At time[bold yellow] {self.clock.currentTime()}[/]: [bold blue]PCB {pcb.pid}[/] entered [bold green]CPU[/]'
                                messages.append(m9)
                            self.readyQueue = self.readyQueue[num_to_assign:] 
                        elif self.CPUQueue and self.IOQueue and not self.readyQueue:                        # if ready is empty, but IO still has processes continue
                            pass
                        else:
                            if loopIteration > 1 and not self.readyQueue and not self.IOQueue and not self.CPUQueue and not self.waitQueue:
                                complete=True
                                break     
                    else:
                        if self.readyQueue and (not self.CPUQueue or len(self.CPUQueue) < self.num_cpus):
                            num_to_assign = min(self.num_cpus - len(self.CPUQueue), len(self.readyQueue))
                            next_processes = self.readyQueue[:num_to_assign]
                            self.CPUQueue.extend(next_processes)
                            for pcb in next_processes:
                                pcb.changeState('CPU')
                                m10=f'At time[bold yellow] {self.clock.currentTime()}[/]: [bold blue]PCB {pcb.pid}[/] entered [bold green]CPU[/]'
                                messages.append(m10)
                            self.readyQueue = self.readyQueue[num_to_assign:]
                        elif loopIteration > 1 and not self.readyQueue and not self.IOQueue and not self.CPUQueue and not self.waitQueue:
                            complete=True
                            break 

                # Check if any PCBs in IO Queue are finished
                if self.IOQueue:
                    next_IOproccesses = []

                    completeIOprocessses = [pcb for pcb in self.IOQueue if pcb.iobursts[0] == 0]

                    self.IOQueue = [pcb for pcb in self.IOQueue if pcb.iobursts[0] != 0]
                    for pcb in self.IOQueue:
                        pcb.remainingIOTime = pcb.iobursts[0]
                    
                    for pcb in completeIOprocessses:
                        pcb.changeState('Ready')
                        m11=f'At time[bold yellow] {self.clock.currentTime()}[/]: [bold blue]PCB {pcb.pid}[/] moved to [bold magenta]ready[/]'
                        messages.append(m11)
                    self.readyQueue.extend(completeIOprocessses)
                    if self.alg == "PB":
                            self.readyQueue.sort(key=lambda x: x.priority, reverse=True)

                    for pcb in completeIOprocessses:
                        if pcb.iobursts[0] == 0:
                            pcb.iobursts.pop(0)
                    completeIOprocessses.clear()
                
                if self.waitQueue and (not self.IOQueue or len(self.IOQueue) < self.num_ios):
                    if self.alg == "PB":
                        self.waitQueue.sort(key=lambda x: x.priority, reverse=True)
                    num_to_assign = min(self.num_ios - len(self.IOQueue), len(self.waitQueue))
                    next_processes = self.waitQueue[:num_to_assign]
                    self.IOQueue.extend(next_processes)
                    for pcb in next_processes:
                        pcb.changeState('IO')
                        m12=f'At time[bold yellow] {self.clock.currentTime()}[/]: [bold blue]PCB {pcb.pid}[/] accessing [bold green] I/O[/]'
                        messages.append(m12)
                    self.waitQueue = self.waitQueue[num_to_assign:]

                time.sleep(self.sleepTime)
                loopIteration +=1
                clock = self.clock.currentTime()
                
                #print(f"end of loop {loopIteration}")
                # self.headTable(self.datfile,self.num_cpus,self.num_ios)
                # self.generateTable(clock)
                # self.messagesTable(messages)
                #layout['header'].update(Panel(self.headTable(self.datfile, self.num_cpus, self.num_ios)))
                layout['body']['progress'].update(Panel(self.generateTable(clock)))
                layout['body']['messages'].update(Panel(self.messagesTable(messages)))
                self.clock.advanceClock(1)    
                # if not self.CPUQueue and not self.IOQueue and not self.readyQueue and not self.waitQueue and not self.newQueue:
                #     complete==True
                    

        return complete
    
    # Methods for output visualization
    def messagesTable(self, messages) -> Table:
        
        messageTable=Table(show_header=True, width=int(self.terminal_width*.30) )
        messageTable.add_column(f'[bold green]System Event Log[/bold green]', justify = "left")
        
        messLog=messages[-14:] if len(messages) >=14 else messages

        for message in reversed(messLog):
            messageTable.add_row(message)
        
        return messageTable
    
    def make_row(self, queue):
        """ 
        Called by the generateTable method to build lists containing all proceses currently within a given queue columns. 
        Returns the jobs list to the generateTable method to be added as row in visualization table for processes. 
        """
        jobs =''
        if queue=='New'and self.newQueue:
            for pcb in self.newQueue:
                jobs += str(f"[bold][[/bold][bold blue]{pcb.pid}[/bold blue], [red]P{pcb.priority}[/red][bold]][/bold]")
            return [jobs]
        elif queue=='Ready' and self.readyQueue:
            for pcb in self.readyQueue:
                jobs += str(f"[bold][[/bold][bold blue]{pcb.pid}[/bold blue], [red]P{pcb.priority}[/red], [magenta]{pcb.readyTime}[/magenta][bold]][/bold]" )    
            return [jobs]
        elif queue=='Wait'and self.waitQueue:
            for self.pcb in self.waitQueue:
                jobs += str(f"[bold][[/bold][bold blue]{self.pcb.pid}[/bold blue], [red]P{self.pcb.priority}[/red], [magenta]{self.pcb.waitTime}[/magenta][bold]][/bold]" )    
            return [jobs]
        elif queue=='CPU' and self.CPUQueue:
            for pcb in self.CPUQueue:
                jobs += str(f"[bold][[/bold][bold blue]{pcb.pid}[/bold blue], [red]P{pcb.priority}[/red], [green]{pcb.remainingCPUTime}[/green][bold]][/bold]" )    
            return [jobs]
        elif queue=='IO' and self.IOQueue:
            for pcb in self.IOQueue:
                jobs += str(f"[bold][[/bold][bold blue]{pcb.pid}[/bold blue], [red]P{pcb.priority}[/red], [green]{pcb.remainingIOTime}[/green][bold]][/bold]" )    
            return [jobs]
        elif queue=='Finished'and self.finishedQueue:
            for pcb in self.finishedQueue:
                jobs += str(f"[bold][[/bold][bold blue]{pcb.pid}[/bold blue][bold]][/bold]")
            return [jobs] 
        else:
            return ['']
    
    def headTable(self, input, num_cpus, num_ios) -> Table:
        cpus=str(num_cpus)
        ios=str(num_ios)
        input=str(input)
        
        headTable = Table(show_header=True,width=int(self.terminal_width*.9))
        headTable.add_column(f'[bold green]Process Progress Table[/bold green]', justify = "center")
        
        if self.alg != "RR":
            self.timeSlice = -1
        algorithms = {
            "RR": f"Round Robin with Time Slice {self.timeSlice}",
            "FCFS": "First Come First Serve w/o Priority",
            "PB": "First Come First Serve with Priority "
        }
        headTable.add_row(f'[bold blue]Algorithm Type: [/][bold cyan]{algorithms[self.alg]}[/]')
        headTable.add_row(f'[bold red]CPUs: [/][bold magenta] {cpus}[/]')
        headTable.add_row(f'[bold dark_red]IO devices: [/][bold purple4] {ios}[/]')
        headTable.add_row(f'[bold blue1]Input File Name: [/][bold deep_sky_blue1]{input}[/]')
       
        return headTable

    def generateTable(self, clock) -> Table:
        """ 
            returns a rich table that displays all the queue contents.
            make_row returns a list of processes in each queue. 
        """  
        
        # Create the table
        qClock=f'[bold yellow]{str(self.clock.currentTime())}[/]'
        
        table = Table(show_header=True,width=int(self.terminal_width*.60)) # uses the add_column information to create column headings. 
        table.add_column(f'[bold][yellow]Clock[/yellow][/bold]')
        table.add_column(f'[bold][cyan]Queue[/cyan][/bold]')
        table.add_column(f'[bold blue]Process[/bold blue], [bold red]Priority[/bold red], [bold green]Burst Time[/bold green]/[bold magenta]Idle Time[/bold magenta]')
        
        table.add_row('','New',*self.make_row("New"), end_section=True)
        table.add_row('','Ready',*self.make_row("Ready"), end_section=True)
        table.add_row(qClock,'CPU',*self.make_row("CPU"), end_section=True)
        table.add_row('','Wait',*self.make_row("Wait"), end_section=True)
        table.add_row('','IO',*self.make_row("IO"), end_section=True)
        table.add_row('','Done',*self.make_row("Finished"), end_section=True)
        
        return table

def main(datafile, num_cpus=1, num_ios=1, alg="FCFS", ts=5, sleep=0.01, outputfile="SimStatsData.csv"):
    sim = Simulator(datafile, alg, num_cpus, num_ios, ts, sleep, outputfile)
    print(f'[bold][red] All processes have terminated[/red][/bold]\n')
    Stats(sim.getProcesses(), sim.clock, num_cpus, num_ios, alg, datafile)

if __name__ == '__main__':
    # Default values
    filename = "datafile.dat"
    algorithm = "FCFS"
    cpu = 1
    ios = 1
    ts = 10
    sleep = 0.1
    output = "output.dat"

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="The name of the file to read from")
    parser.add_argument("-a", "--algorithm", help="The algorithm to use for the simulation")
    parser.add_argument("-c", "--cpu", help="The number of CPUs to simulate", type=int)
    parser.add_argument("-i", "--ios", help="The number of I/O devices to simulate", type=int)
    parser.add_argument("-t", "--ts", help="The time slice to use for the Round Robin algorithm", type=int)
    parser.add_argument("-s", "--sleep", help="The amount of time to sleep between each cycle", type=float)
    parser.add_argument("-o", "--output", help="The name of the output file", type=str)

    args = parser.parse_args()
    
    filename = args.filename if args.filename else filename
    algorithm = args.algorithm if args.algorithm else algorithm
    cpu = args.cpu if args.cpu else cpu
    ios = args.ios if args.ios else ios
    ts = args.ts if args.ts else ts
    sleep = args.sleep if args.sleep else sleep
    output = args.output if args.output else output
    
    if algorithm not in ["FCFS", "RR", "PB"]:
        print("Invalid algorithm. Please choose from the following: FCFS, RR")
    else:
        if output:
            main(filename, cpu, ios, algorithm, ts, sleep, output)
        else:
            main(filename, cpu, ios, algorithm, ts, sleep)            
 
    