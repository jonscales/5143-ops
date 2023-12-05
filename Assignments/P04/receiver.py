from comms import Receiver
from comms import mykwargs
import sys
import json
import requests

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
def getAPIroute(self):
    
    r = requests.get("http://sendmessage.live:8001/grayscale?num=100")
    data=[]
    data.append(r.json())
    return data
    #print(r.json())
    
   

def usage():
    print("Usage: receiver.py <host> <port> <exchange> <routing_keys> ")
    print("Usage: receiver.py 164.90.134.137 5672 cpuproject 'sports,news' ")
    sys.exit()

RegD={"R1":0,"R2":0,"R3":0,"R4":0,"R5":0,"R6":0}
def writereg(loc,val):
    RegD[loc]=val

def processMessage(ch, method, properties, body):
        #print(f"I will not beat off any more")
        data = json.loads(body.decode())
        outfile="messagedata.dat"
        with open(outfile, 'a',) as outfile: #Append new messages to existing file. 
            for instructblock in data:
                for line in instructblock:
                    print(line)
                    outfile.write(line +'\n')

        for i in data:
            for t in range(len(data[0])):
                single=i[t].split()
                if single[0]=="LOAD":
                    writereg(single[1],single[2])
                if single[0]=="ADD":
                    #print(single[1])
                    #print(RegD[single[1]])
                    writereg(single[1],int(RegD[single[1]]) + int(RegD[single[2]]))
                if single[0]=="DIV":
                    writereg(single[1],int(RegD[single[1]]) / int(RegD[single[2]]))
                if single[0]=="SUB":
                    writereg(single[1],abs(int(RegD[single[1]]) - int(RegD[single[2]])))
                if single[0]=="MUL":
                    writereg(single[1],int(RegD[single[1]]) * int(RegD[single[2]]))
                if single[0]=="STORE":
                    rgb=single[1]
                    rgb2=rgb.replace('(','').replace(')','')
                    rgb3=rgb2.split(',')
                    # print("This print= ",rgb3)
                    # print("this print 1= ",rgb3[0])
                    # print("this print 2= ",rgb3[1])
                    # print("this print 3= ",rgb3[2])
                    xy=single[2]
                    #print(xy)
                    xy2=xy.replace('(','').replace(')','')
                    xy3=xy2.split(',')
                    # print("this is x ",xy3[0])
                    # print("this is y ",xy3[1])
                    print(f'"STORE" : [{RegD[rgb3[0]]},{RegD[rgb3[1]]},{RegD[rgb3[2]]}],"xy": [ {RegD[xy3[0]]},{RegD[xy3[1]]} ]   ')
                    #print(RegD[rgb3[0]])for instructblock in data:
                    
            print(RegD)
            print("\n")  



class Decoder():
    def __init__(self, config="commsConfig.json", callback=processMessage):
        print(processMessage)
        self.receiver=Receiver(config=config,callback=processMessage)
        self.receiver.start_consuming()


    

if __name__ == "__main__":
    with open("commsConfig.json") as f:
        config = json.load(f)

    print(config)

    args, kwargs = mykwargs(sys.argv)
    keys = list(kwargs.keys())
    if "help" in kwargs:
        usage()

    else:
        host = kwargs.get("host", config["host"])
        port = kwargs.get("port", config["port"])
        exchange = kwargs.get("exchange", config["exchange"])
        user = kwargs.get("user", config["user"])
        pword = kwargs.get("pword", config["pword"])
        routing_keys = kwargs.get("routing_keys", config["routing_keys"])
        if not isinstance(routing_keys, list):
            routing_keys = routing_keys.split(",")

        #### Receiver Code Example
    
    # receiver = Receiver(
    #     host=host,
    #     port=port,
    #     exchange=exchange,
    #     user=user,
    #     pword=pword,
    #     routing_keys="hex2",
    # )
    # receiver=Receiver(config="commsConfig.json")
    # receiver.start_consuming()
    decoder=Decoder(config="commsConfig.json",callback=processMessage)
