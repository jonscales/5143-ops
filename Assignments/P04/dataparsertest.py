data1=[[
    'LOAD R1 814',
    'LOAD R2 591',
    'LOAD R3 255',
    'LOAD R4 73',
    'LOAD R5 118',
    'LOAD R6 35',
    'SUB  R4 R3',
    'SUB  R5 R3',
    'SUB  R6 R3',
    'STORE (R4,R5,R6) (R1,R2)'
],[
    'LOAD R1 914',
    'LOAD R2 691',
    'LOAD R3 255',
    'LOAD R4 50',
    'LOAD R5 100',
    'LOAD R6 75',
    'SUB  R4 R3',
    'SUB  R5 R3',
    'SUB  R6 R3',
    'STORE (R4,R5,R6) (R1,R2)'
],[
    'LOAD R1 714',
    'LOAD R2 491',
    'LOAD R3 255',
    'LOAD R4 75',
    'LOAD R5 80',
    'LOAD R6 25',
    'SUB  R4 R3',
    'SUB  R5 R3',
    'SUB  R6 R3',
    'STORE (R4,R5,R6) (R1,R2)'
]]
[
    'LOAD R1 814',
    'LOAD R2 591',
    'LOAD R3 255',
    'LOAD R4 73',
    'LOAD R5 118',
    'LOAD R6 35',
    'SUB  R4 R3',
    'SUB  R5 R3',
    'SUB  R6 R3',
    'STORE (R4,R5,R6) (R1,R2)'
]
def processBlock(self, instructblock):
    dataline=[]
    blockList=[]
    for line in instructblock:
        dataline.append(line.split())
        print(dataline)
        blockList.append(dataline)
        print(blockList)
        # if dataline[0]=="LOAD":
        #     register=dataline[1]


        # elif dataline[0]=="ADD":


        # elif dataline[0]=="SUB":

        # elif dataline[0]=="ADD":

        # elif dataline[0]=="ADD":        
    
        # else    
    
outfile1="messagedata.dat"
outfile2='linedata.dat'
with open(outfile1, 'w',) as outfile1:
    for instructblock in data1:
        print(instructblock)
        outfile1.write(instructblock + '\n')
        with open(outfile2, 'w') as outfile2:
            for line in instructblock:
                print(line)
                outfile2.write(line +'\n')
            
        processBlock(instructblock)

        