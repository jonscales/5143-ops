# CPU Schecule Simulation
"""
This program simulates a CPU scheduler
The program can be run with different flags to simulate a FCFS or Round Robin algorithm
"""
import os
from rich import print
from rich.text import Text
import time
import csv
import shutil
from rich.table import Table
from rich.live import Live
from rich.progress import SpinnerColumn
from rich.console import Console

console = Console()
terminal_width = console.width

class PCB:
    """
    This class generates a process control block (PCB) from information read in from 
    a data file. The attributes are passed to PCB as the pcb is
    generated in by the readData method of the Simulator class. 
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
        self.currBurstIndex = 0
        self.currCpuBurst = cpubursts[0]
        self.currIoBurst =iobursts[0]
        self.waitTime = 0
        self.readyTime = 0
        self.timeEnter = 0
        self.timeExit = 0
        self.TAT = 0
        self.sliceTimer = 0
        self.initCPUTime =0
        self.initIOTime =0
        self.cpuTime = self.getTotCpuTime()
        self.ioTime = self.getTotIoTime()
        self.numCpuBursts =len(cpubursts)
        self.numIoBursts =len(iobursts)
        self.remainingCPUTime = int(cpubursts[0])
        self.remainingIOTime = int(iobursts[0])
        self.runTime = self.getTotalTime()
   
    def setTimeEnter(self,clock):
        self.timeEnter = clock.currentTime()
        return self.timeEnter
    
    def setTimeExit(self,clock):
        self.timeExit = clock.currentTime()
        return self.timeExit
    
    def setTAT(self):
        self.TAT = self.timeExit - self.timeEnter
        return self.TAT
    
    def getSliceTimer(self):
        """
        returns the sliceTimer variable
        """
        return self.sliceTimer
    
    def incrementSliceTimer(self):
        """
        increments the sliceTimer variable
        """
        self.sliceTimer +=1
        
    def resetSliceTimer(self):
        """
        resets the sliceTimer variable
        """
        self.sliceTimer = 0

    def upPriority(self):
        """
        increases the priority +1 of a process after it has remained in the ready queue 
        longer than the the sum of its CPU bursts
        """
        Simulator.getProcesses()
        for pcb in self.processes:
            if pcb.waitTime >= pcb.CPUTime:
                pcb.priority +=1

    def getPriority(self):
        """
        returns the PCB's priority
        """
        return self.priority
    
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

    def changeBurstType(self,BT):
        """not used"""
        self.currBurstType = BT
    
    def getCurrBurstType(self):
        """not used"""
        return self.currBurstIs
    
    def getCurrBurst(self):
        """ returns the current burst for the PCB"""
        if self.currBurstType =='CPU':
            return self.cpubursts[self.currBurstIndex]
        elif self.currBurstType =='IO':
            return self.iobursts[self.currBurstIndex]
        
    def decrementCpuBurst(self):
        """not used"""
        self.bursts[self.currBurstIndex] -= 1

    def decrementIoBurst(self):
        """not used"""
        self.bursts[self.currBurstIndex] -= 1

    def incrementBurstIndex(self):
        """not used"""
        self.currBurstIndex += 1
    
    def getCurrentBurstTime(self):
        return self.bursts[self.currBurstIndex]
        
    def getTotCpuTime(self):
        """
        returns the total CPU time by adding all cpu bursts
        """
        for i in range(len(self.cpubursts)):
            self.initCPUTime += int(self.cpubursts[i])
        self.cpuTime = self.initCPUTime
        return self.cpuTime
    
    def getTotIoTime(self):
        """
        returns the total IO time by adding all io bursts
        """
        for i in range(len(self.iobursts)):
            self.initIOTime += int(self.iobursts[i])
        self.ioTime = self.initIOTime
        return self.ioTime 
    
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
        returns the ratio of run (CPU + IO ) time to idle (wait + ready) time
        """
        return round((self.cpuTime + self.ioTime)/(self.readyTime + self.waitTime),2)

    def getcpu_util(self):
            """
            returns the cpu utilization ( % of time spent in CPU)
            """
            return round((self.initCPUTime/self.getTotalTime()*100),2)
    
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
    The class will display the stats associated with the movement of PCB
    through the schedular.  It will also output this information as a .csv file
    for use in other applications. 
    """    
    def __init__(self, processes, clock, num_cpus, num_ios, input, num_timeslice=10):
        """
        Stats initialization
        """
        self.processes = processes
        self.simType = 'Priority Based First Come, First Served'
        self.num_timeslice=num_timeslice
        self.input = input
        self.num_cpus = num_cpus
        self.num_ios = num_ios
        self.clock = clock
        self.statTable(clock)
        self.summaryTable(clock)
        self.statFileWriter(clock, self.simType)
    
    def statTable(self,clock):
        """
        generates & displays a table showing the total clock time for completing all PCBs
        generates & displays a table with various stats from each PCB
        """
        #build a rich table
        # Create the table        
        sClock=str(self.clock.currentTime())
        sortedProcesses = sorted(self.processes.items(), key=lambda x: x[1][0].getTotalTime())
        statTable = Table(show_header=True, width=int(terminal_width*.9)) # uses the add_column information to create column headings. 
        statTable.add_column(f'[bold blue]PID[/bold blue]', width=int(terminal_width*.1),justify='center')
        statTable.add_column(f'[bold][red]Priority[/red][/bold]',  width=int(terminal_width*.1),justify='center')
        statTable.add_column(f'[bold][cyan]Total Time[/cyan][/bold]',  width=int(terminal_width*.1),justify='center')
        statTable.add_column(f'[bold][magenta]Ready Time[/magenta][/bold]',  width=int(terminal_width*.1),justify='center')
        statTable.add_column(f'[bold][green]CPU Time[/green][/bold]',  width=int(terminal_width*.1),justify='center')
        statTable.add_column(f'[bold][magenta]Wait Time[/magenta][/bold]',  width=int(terminal_width*.1),justify='center')
        statTable.add_column(f'[bold][green]IO Time[/green][/bold]',  width=int(terminal_width*.1),justify='center')
        statTable.add_column(f'[bold][red]CPU Util[/red][/bold]',  width=int(terminal_width*.1),justify='center')
        statTable.add_column(f'[bold blue]CPU/IO[/bold blue]', width=int(terminal_width*.1),justify='center')
        statTable.add_column(f'[bold cyan]Run/Idle[/bold cyan]', width=int(terminal_width*.1),justify='center')
                             
        #statTable.add_row(f'Total Processes Run Time: [bold][yellow]{sClock}[/yellow][/bold]')
        for pid, pcb_instances in sortedProcesses:
            for pcb in pcb_instances:
                statTable.add_row(
                    str(pcb.pid),
                    str(pcb.priority),
                    str(pcb.getTotalTime()),
                    str(pcb.getReadyTime()),
                    str(pcb.getTotCpuTime()),
                    str(pcb.getWaitTime()),
                    str(pcb.getTotIoTime()),
                    str(pcb.getcpu_util()),
                    str(pcb.cpu_ioRatio()),
                    str(pcb.run_idleRatio())
                    )
        print(f'[bold green]Process Run Attribute Data[/bold green]')    
        print(statTable)
        return statTable
    
    def statFileWriter(self, clock, simType='none'):
        """
        generates a .csv outfile of the scheduler data
        Keyed to various simulation data types: 
        SCPU = short CPU bursts
        SIO = short IO bursts
        LCPU = long CPU bursts
        LIO = long IO bursts
        HBCt = high burst count
        LBCt = low burst count 
        """ 
        # dictionary to match output filename to simulation run type
        sim_type_to_fname = {
            'SCPU': 'SCPU_stat_data.csv',
            'SIO': 'SIO_stat_data.csv',
            'LCPU': 'LCPU_stat_data.csv',
            'LIO': 'LIO_stat_data.csv',
            'HBCt':'HBCt_stat_data.csv',
            'LBCt':'LBCt_stat_data.csv',                
            }
        if simType=='None':
            outFileName ='SimStatsData.csv'
        else:
            outFileName=sim_type_to_fname.get(self.simType, 'SimStatsData.csv')
       
        with open(outFileName, 'w', newline='') as csvfile:
            fieldnames = ["Clock Time","Process ID", "Total Time", "Ready Time", "CPU Time", "IO Time", "Wait Time","CPU Util", "CPU/IO", "Run/Idle"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            #first_row = {"Clock Time": clock.currentTime()}
            #writer.writerow(first_row)
            # Write the header row to the CSV file
            writer.writeheader()

            # Write data for each PCB
            for pid, pcb_instances in self.processes.items():
                for pcb in pcb_instances:
                    data = {
                        'Clock Time': clock.currentTime(),
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
    def summaryTable(self, clock) -> Table:
        """
        generates & displays a table summarizing the various stats from the stats Table
        """
        #stats calcs
        simType=str(self.simType)
        slice=str(self.num_timeslice)
        input=str(self.input)
        total_cpu_time = 0
        total_wait_time =0
        total_ready_time=0
        total_tat_time = 0
        aveCpuUtil=''
        aveWaitTime=''
        aveReadyTime=''
        aveTat=''
        for pcb, pcb_instances in self.processes.items():
            for pcb in pcb_instances:
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
        
        input_to_type = {
            'SCPUInt': '20 jobs, Long CPU burst, short IO bursts',
            'SIOInt': '20 jobs, Short CPU burst, long IO bursts',
            'MCPUInt': '50 jobs, Long CPU burst, short IO bursts',
            'MIOInt': '50 jobs, Short CPU burst, long IO bursts',
            'LCPUInt': '100 jobs, Long CPU burst, short IO bursts',
            'LIOInt': '100 jobs, Short CPU burst, long IO bursts',
            'SEven': '20 jobs, CPU -IO bursts equal lengths',
            'MEven': '50 jobs, CPU -IO bursts equal lengths',
            'LEven': '100 jobs, CPU -IO bursts equal lengths',            
            }
        if input == 'None':
            inputType ='20 jobs, CPU -IO bursts equal lengths'
        else:
            inputType =input_to_type.get(self.input, '20 jobs, CPU -IO bursts equal lengths')

        summaryTable  = Table(show_header=True) # uses the add_column information to create column headings.
        summaryTable.add_column(f'[bold][green]Summary Statistics Table[/bold][/green]',width=int(terminal_width*.8),justify='center') 
        summaryTable.add_row(f'Algorithm Type : {simType}')
        summaryTable.add_row(f'Time Slice : {slice}')
        summaryTable.add_row(f'Proccess Characteristics : {inputType}')
        summaryTable.add_row(f'Number of CPUs : {cpus}')
        summaryTable.add_row(f'Number of I/O Devices : {ios}')
        summaryTable.add_row(f"CPU Utilization: {aveCpuUtil} %")
        summaryTable.add_row(f"Avg Wait Time: {aveWaitTime}")
        summaryTable.add_row(f"Avg Ready Time: {aveReadyTime}")
        summaryTable.add_row(f"Avg TAT: {aveTat}")
        print(summaryTable)
        return summaryTable
    
    def statFileWriter(self, clock, simType='none'):
        """
        writes the stats information to a .csv file
        """ 
        # dictionary to match output filename to simulation run type
        sim_type_to_fname = {
            'SCPU': 'SCPU_stat_data.csv',
            'SIO': 'SIO_stat_data.csv',
            'LCPU': 'LCPU_stat_data.csv',
            'LIO': 'LIO_stat_data.csv',
            'HBCt':'HBCt_stat_data.csv',
            'LBCt':'LBCt_stat_data.csv',                
            }
        if simType=='None':
            outFileName ='SimStatsData.csv'
        else:
            outFileName=sim_type_to_fname.get(self.simType, 'SimStatsData.csv')
       
        with open(outFileName, 'w', newline='') as csvfile:
            fieldnames = ["Clock Time", "Arrival Time", "Process ID", "Total Time", "Ready Time", "CPU Time", "CPU Util", "IO Time", "Wait Time","CPU/IO", "Run/Idle"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            first_row = {"Clock Time": clock.currentTime()}
            writer.writerow(first_row)
            
            # Write the header row to the CSV file
            writer.writeheader()

            # Write data for each PCB
            for pid, pcb_instances in self.processes.items():
                for pcb in pcb_instances:
                    data = {
                        'Process ID': pcb.pid,
                        'Arrival Time': pcb.arrivalTime,
                        'Total Time': pcb.getTotalTime(),
                        'Ready Time':pcb.getReadyTime(),
                        'CPU Time': pcb.cpuTime,
                        'CPU Util': pcb.getcpu_util(),
                        'Wait Time' : pcb.waitTime,
                        'IO Time' : pcb.ioTime,
                        'CPU/IO': pcb.cpu_ioRatio(),
                        'Run/Idle': pcb.run_idleRatio()                    
                            }
                    writer.writerow(data) 
                          


class Simulator:
    """
    This class is the main simulator operator
    methods to:
      read in the data from a file
      run the simulation loop
    """
    def __init__(self, input, num_cpus, num_ios, ts, sleep):
        """
        Simulator initialization
        """
        #self.timeSlice=int(TS)
        self.datfile = input
        self.num_cpus =int(num_cpus)
        self.num_ios = int(num_ios)
        self.sleepTime = float(sleep)
        self.processes = {}
        self.readData()
        self.newQueue = []
        self.readyQueue =[]
        self.CPUQueue =[]
        self.IOQueue = []
        self.waitQueue = []
        self.finishedQueue =[]
        self.clock = SysClock()   
        self.simLoop(self.processes, self.num_cpus, self.num_ios, self.sleepTime)
    
    def getProcesses(self):
        """
        returns the processes dictionary to other classes' methods
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
                parts = process.split(' ')
                arrival = parts[0]
                pid = parts[1]
                priority = int(parts[2][1:])
                bursts = parts[3:]
                cpubursts=[] 
                iobursts=[]
                # parse bursts into CPU & IO
                for i in range(len(bursts)):
                    if i%2==0:
                        cpubursts.append(bursts[i])
                    else:
                        iobursts.append(bursts[i])

                #create dictionary of all processes with PID as key and values are PCBs        
                pcb_key=f'PID-{pid}' # use pid to be key for each PCB
                self.processes[pcb_key] = [PCB(pid, arrival, priority, cpubursts, iobursts)]
                
        return self.processes  
         
    def simLoop(self, processes, num_cpus, num_ios, sleepTime): 
        """ 
        SIMULATION LOOP
        This method runs the Schedular Simulation
        """
        complete = False
        loopIteration = 0
        
        #BEGINNING of SIMLOOP
       
        while not complete: #loop until all processes are in finished[]  
        
        # 1. increment times for readyQueue & waitQueue PCBs
            if self.readyQueue:
                for pcb in self.readyQueue:
                    pcb.changeState('Ready')
                    self.readyQueue = sorted(self.readyQueue, key=lambda pcb: (pcb.priority), reverse=True)
                    pcb.incrementReadyTime() 
            else:
                pass
            
            if self.waitQueue:
                for pcb in self.waitQueue:
                    pcb.changeState('Wait')
                    pcb.incrementWaitTime()
                    if pcb.waitTime > pcb.cpuTime:   #increment priority if wait time > cpu time
                        pcb.priority +=1
            else:
                pass       
                    
        #2. move anything in new to ready
            if self.newQueue:
                self.readyQueue.extend(self.newQueue)
                for pcb in self.readyQueue:
                    pcb.changeState('Ready')
                    print(f'PID {pcb.pid} --> Ready')
                self.readyQueue = sorted(self.readyQueue, key=lambda pcb: (pcb.priority), reverse=True)
                self.newQueue.clear()
           
        # 3. check for new processes if pcb arrival time == time, add pcb to new
            for pid, PCBs in processes.items():
                for pid in PCBs: 
                    if pid.arrivalTime == self.clock.currentTime():
                        self.newQueue.append(pid)
                        pid.changeState('New')
                        print(f'PID {pid.pid} --> New')
            else:
                pass 
        
        # 4. decrement current CPU and IO processes bursts values
            if self.CPUQueue:
                for pcb in self.CPUQueue:
                    if pcb.cpubursts:
                        pcb.cpubursts[0] -= 1
                        pcb.remainingCPUTime = pcb.cpubursts[0]
                    else:
                        pass
            
            if self.IOQueue:
                for pcb in self.IOQueue:
                    if pcb.iobursts:
                        pcb.iobursts[0] -=1
                        pcb.remainingIOTime = pcb.iobursts[0] 
                    else:
                        pass
            else:    
                pass              
                    
        # 5A. sort readyQueue by priority then AT, then CPU shortest burst length  
            self.readyQueue = sorted(self.readyQueue, key=lambda pcb: (pcb.priority), reverse=True)
        
        # 5B check if process in CPU and if any are finished
            if self.CPUQueue:                                #is process in the CPU
                lowestCPU = min(self.CPUQueue, key=lambda pcb:pcb.priority)
                print(f'Lowest priority PCB in CPU = {lowestCPU.pid}')
                for pcb in self.CPUQueue: 
                    if pcb.cpubursts[0] == 0:                #is process in CPU finished?
                        if len(pcb.cpubursts) <= 1:          # was this last CPU bursts for process?
                            print(f'PCB {pcb.pid} DONE')
                            pcb.changeState('Finished')      # move process to finished queue
                            self.finishedQueue.append(pcb)   
                            pcb.cpubursts.pop(0)             # remove finished burst from cpu bursts list
                        else:                                   # not last CPU bursts so move to wait
                            print(f'PCB {pcb.pid} CPU burst finished, moved to Wait')
                            self.waitQueue.append(pcb)        # move completed process to wait
                            pcb.changeState('Wait')
                                      
                            if pcb.cpubursts:
                                pcb.cpubursts.pop(0) 
                            # print(f'Wait queue = ')
                            # for pcb in self.waitQueue:
                            #     print(f'PID {pcb.pid}')
                    else:
                        pass
                self.CPUQueue = [pcb for pcb in self.CPUQueue if pcb.state == 'CPU']  # update CPU 
                self.readyQueue = sorted(self.readyQueue, key=lambda pcb: (pcb.priority), reverse=True)
                
        #5C check if any ready processes have higher priority & swap with lower CPU processes - loop till all swapped
                while loopIteration >= 3 and self.readyQueue and (self.readyQueue[0].priority > lowestCPU.priority) and self.readyQueue[0].readyTime >=1:
                    #print(f'1st process in sorted ready queue: {self.readyQueue[0].pid}')
                    highestReady = self.readyQueue[0]
                    #print(f'highest priority in sorted ready queue: {highestReady.pid}')
                
                    try:
                        self.CPUQueue.remove(lowestCPU)
                        print(f'PCB {lowestCPU.pid} removed from CPU, returned to ready')
                    except ValueError:
                        pass
                    lowestCPU.changeState('Ready')
                    self.readyQueue.append(lowestCPU)
                    self.CPUQueue.append(highestReady)
                    print(f'PCB {highestReady.pid} added to CPU')
                    highestReady.changeState('CPU')
                    self.readyQueue.pop(0) 
                    #print(f'Ready contains: ')
                    # for pcb in self.readyQueue:
                    #     print(f'PCB {pcb.pid}')      
                
                self.readyQueue = [pcb for pcb in self.readyQueue if pcb.state =='Ready']  # update ready 
                self.CPUQueue = [pcb for pcb in self.CPUQueue if pcb.state =='CPU']  # update CPU 
                self.readyQueue = sorted(self.readyQueue, key=lambda pcb: (pcb.priority),reverse=True)
        #5D
                if self.readyQueue and loopIteration >= 1 and (not self.CPUQueue or len(self.CPUQueue) < self.num_cpus): # are processes in readyqueue & is CPU not full
                    num_to_assign = min(self.num_cpus - len(self.CPUQueue), len(self.readyQueue))
                    next_processes = self.readyQueue[:num_to_assign] # get # of process from ready queue needed to fill CPU
                    self.CPUQueue.extend(next_processes)  # move next processes to the CPU 
                    for pcb in next_processes:
                        pcb.changeState('CPU')
                    self.readyQueue = self.readyQueue[num_to_assign:] 
                elif self.CPUQueue and self.IOQueue and not self.readyQueue: # if ready is empty, but IO still has processes continue
                    pass
                else:
                    if loopIteration > 1 and not self.readyQueue and not self.IOQueue and not self.CPUQueue and not self.waitQueue:
                        complete=True        
                    else: # running process has remaining CPU time, keep PCB in CPU,
                        pass   
            else:      # if cpu is empty add something, 1st loop only    
                self.readyQueue = sorted(self.readyQueue, key=lambda pcb: (pcb.priority),reverse=True)
                
                if loopIteration >=2 and self.readyQueue and (not self.CPUQueue or len(self.CPUQueue) < self.num_cpus): # are processes in readyqueue & is CPU not full
                    num_to_assign =min(self.num_cpus - len(self.CPUQueue), len(self.readyQueue))
                    next_processes = self.readyQueue[:num_to_assign] # get # of process from ready queue needed to fill CPU
                    self.CPUQueue.extend(next_processes)  # move next processes to the CPU 
                    for pcb in next_processes:
                        pcb.changeState('CPU')
                    self.readyQueue = self.readyQueue[num_to_assign:] 
                elif not self.readyQueue and self.IOQueue: # if ready is empty, but IO still has processes continue
                    pass
                else:
                    if loopIteration > 1 and not self.CPUQueue and not self.readyQueue and not self.IOQueue and not self.waitQueue:
                        complete=True                      
        
        # 6. check if any PCBs' in IO have current IO burst value == 0,  
            if self.IOQueue:
                next_IOprocesses =[] #container for next processes 
                
                # make  temp list of complete processes
                completeIOprocesses = [pcb for pcb in self.IOQueue if pcb.iobursts[0] == 0]
                    
                # update IO queue with only incomplete processes
                self.IOQueue = [pcb for pcb in self.IOQueue if pcb.iobursts[0] != 0]
                for pcb in self.IOQueue: # just to print the IO burst remaining time
                    pcb.remainingTime = pcb.iobursts[0]
                
                # add the IO complete process back to ready queue
                for pcb in completeIOprocesses:
                    pcb.changeState('Ready')
                self.readyQueue.extend(completeIOprocesses)
                self.readyQueue = [pcb for pcb in self.readyQueue if pcb.state =='Ready']  # update ready
                self.readyQueue = sorted(self.readyQueue, key=lambda pcb: (pcb.priority),reverse=True) # resort ready queue
                self.IOQueue = [pcb for pcb in self.IOQueue if pcb.state =='IO']  # update IO 
                # remove the io burst from the iobursts list in PCB
                for pcb in completeIOprocesses:
                    if pcb.iobursts[0] <= 0:
                       pcb.iobursts.pop(0)
                # clear the temp complete IO processes list
                completeIOprocesses.clear()  
               
                #Add processes to IO if IO already exists
                if self.waitQueue and (not self.IOQueue or len(self.IOQueue) < self.num_ios): # are processes in waitqueue & is IO not full
                    num_to_assignIO = min(self.num_ios - len(self.IOQueue), len(self.waitQueue)) # get # of process from wait queue needed to fill IO
                    potentialIOprocesses = self.waitQueue[:num_to_assignIO] 
                    for pcb in potentialIOprocesses:
                        # print(f'Potential next IO processes')
                        # print(f'PID {pcb.pid}')
                        if pcb.waitTime >=1:# move next processes to the IO if they have been in wait 1 tick
                            next_IOprocesses.append(pcb) 
                            pcb.changeState('IO')
                    
                    if next_IOprocesses:
                        for pcb in next_IOprocesses:
                            print(f'Processes moved to IO')
                            print(f'PID {pcb.pid}')
                            pcb.changeState('IO') 
                        self.IOQueue.extend(next_IOprocesses)
                        next_IOprocesses.clear()
                       
                    self.waitQueue = self.waitQueue[num_to_assignIO:] # update wait
                    self.waitQueue =[pcb for pcb in self.waitQueue if pcb.state == 'Wait']
                    potentialIOprocesses = [pcb for pcb in potentialIOprocesses if pcb.state == 'Wait'] # keep processes not moved to IO
                    self.waitQueue.extend(potentialIOprocesses) # add  processes back that had not been in wait >=1 tick  
                    self.IOQueue = [pcb for pcb in self.IOQueue if pcb.state =='IO']  # update IO 
                    potentialIOprocesses.clear()
                    next_IOprocesses.clear()                                               
                    
                    
            else: # add processes to IO if IO currently empty
                next_IOprocesses =[]
                if self.waitQueue and (not self.IOQueue or len(self.IOQueue) < self.num_ios): # are processes in waitqueue & is IO empty or not full
                    num_to_assignIO = min(self.num_ios - len(self.IOQueue), len(self.waitQueue))# get # of process from wait queue needed to fill IO
                    potentialIOprocesses = self.waitQueue[:num_to_assignIO] #get processes that could be moved to io
                    for pcb in potentialIOprocesses:
                        print(f'Potential next IO processes')
                        print(f'PID {pcb.pid}')
                        if pcb.waitTime >=1:
                            next_IOprocesses.append(pcb) # actual next processes are those that have been in ready >1 tick
                            pcb.changeState('IO') 
                    
                    if next_IOprocesses:
                        for pcb in next_IOprocesses:
                            print(f'Actual next processes are')
                            print(f'PID {pcb.pid}')
                           
                        self.IOQueue.extend(next_IOprocesses)  # move next processes to the IO 
                        next_IOprocesses.clear()
                
                    self.waitQueue = self.waitQueue[num_to_assignIO:] #update the wait queue
                    self.waitQueue =[pcb for pcb in self.waitQueue if pcb.state == 'Wait']
                    potentialIOprocesses = [pcb for pcb in potentialIOprocesses if pcb.state == 'Wait'] # keeps pcb not moved to IO
                    self.waitQueue.extend(potentialIOprocesses)
                    self.IOQueue = [pcb for pcb in self.IOQueue if pcb.state == 'IO']  # update IO   self.waitQueue.extend(potentialIOprocesses) # add those processes back that had not been in wait >=1 tick 
                    potentialIOprocesses.clear()
                    next_IOprocesses.clear()
                     
                else:
                    pass

            time.sleep(self.sleepTime)
            loopIteration += 1
            clock=self.clock.currentTime()
            # Update the table contents
            os.system('cls' if os.name == 'nt' else 'clear')
            
            #print(f'[bold][green]Process Progress Table[/bold][/green]')

            with Live(self.headTable(self.datfile, self.num_cpus, self.num_ios)) as live:
                live.update(self.headTable(self.datfile, self.num_cpus, self.num_ios))
                      
            with Live(self.generateTable(clock)) as live:
                live.update(self.generateTable(clock))
           
            self.clock.advanceClock(1)
            #END of SIMLOOP
                
    # Methods for output visualization
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
        """
        returns a header table showing algorithm type, cpu #, IO #, and time slice informaiton
        """
        cpus=str(num_cpus)
        ios=str(num_ios)
        input=str(input)

        headTable = Table(show_header=True, width=int(terminal_width*.9), )
        headTable.add_column(f'[bold green]Process Progress Table[/bold green]', justify = "center")
        
        headTable.add_row(f'[bold blue]Algorithm Type: [/][bold cyan] Priority Based First Come, First Served[/]')
        headTable.add_row(f'[bold red]CPUs: [/][bold magenta] {cpus}[/]')
        headTable.add_row(f'[bold dark_red]IO devices: [/][bold purple4] {ios}[/]')
        headTable.add_row(f'[bold blue1]Input File Type:[/][bold deep_sky_blue1]{input}[/]')
        return headTable
    
    def generateTable(self,clock) -> Table:
        """ 
            returns a rich table that displays all the queue contents.
            make_row returns a list of processes in each queue. 
        """  
        # Create the tables
        qClock=str(self.clock.currentTime())

        table = Table(show_header=True, width=int(terminal_width*.9)) # uses the add_column information to create column headings. 
        table.add_column(f'[bold][yellow]Clock[/yellow][/bold]', width=int(terminal_width*.1))
        table.add_column(f'[bold][cyan]Queue[/cyan][/bold]',  width=int(terminal_width*.1))
        table.add_column(f'[bold blue]Process[/bold blue], [bold red]Priority[/bold red], [bold green]Burst Time[/bold green]/[bold magenta]Idle Time[/bold magenta]', width=int(terminal_width*.8))
        
        table.add_row('','New',*self.make_row("New"), end_section=True)
        table.add_row('','Ready',*self.make_row("Ready"), end_section=True)
        table.add_row(qClock,'CPU',*self.make_row("CPU"), end_section=True)
        table.add_row('','Wait',*self.make_row("Wait"), end_section=True)
        table.add_row('','IO',*self.make_row("IO"), end_section=True)
        table.add_row('','Done',*self.make_row("Finished"), end_section=True)
        return table
        
    
    
        
def fcfs_prio(input, num_cpus, num_ios, sleep):
    """
    This method runs the Priority Based First Come First Serve (PBFCFS) algorithm
    """
    sim = Simulator(input, num_cpus, num_ios, 3, sleep)
    print(f'\n[bold][red] All processes have terminated[/red][/bold]\n')
    Stats(sim.getProcesses(),sim.clock, sim.num_cpus, sim.num_ios, sim.datfile )


if __name__=='__main__':
    fcfs_prio('small.dat', 2, 2, .1)
   
   
    
