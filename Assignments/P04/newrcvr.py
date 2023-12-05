
import sys
import json
import requests
from rich import print



RegD={"R1":0,"R2":0,"R3":0,"R4":0,"R5":0,"R6":0}

def getAPIroute():
    
    r = requests.get("http://sendmessage.live:8001/grayscale?num=100")
    data=r.json()
    return data

   
def writereg(loc,val):
    RegD[loc]=val

def processMessage():
        messageData = getAPIroute()

        outfile="messagedata.dat"
        with open(outfile, 'a',) as outfile: #Append new messages to existing file. 
            for instructionBlock in messageData:
                for line in instructionBlock:
                    print(f'instruction line in messageData: {line}')
                    # for line in instructblock:
                    #     print(line)
                    outfile.write(str(line)+'\n')

        for i in messageData:
            print(f'this is i:{i}')
            for t in range(len(i[0])):
                print(f'this is t: {t}')
                single=i[t].split()
                print(f'this is single: {single}')
            #     if single[0]=="LOAD":
            #         writereg(single[1],single[2])
            #     if single[0]=="ADD":
            #         #print(single[1])
            #         #print(RegD[single[1]])
            #         writereg(single[1],int(RegD[single[1]]) + int(RegD[single[2]]))
            #     if single[0]=="DIV":
            #         writereg(single[1],int(RegD[single[1]]) / int(RegD[single[2]]))
            #     if single[0]=="SUB":
            #         writereg(single[1],abs(int(RegD[single[1]]) - int(RegD[single[2]])))
            #     if single[0]=="MUL":
            #         writereg(single[1],int(RegD[single[1]]) * int(RegD[single[2]]))
            #     if single[0]=="STORE":
            #         rgb=single[1]
            #         rgb2=rgb.replace('(','').replace(')','')
            #         rgb3=rgb2.split(',')
            #         # print("This print= ",rgb3)
            #         # print("this print 1= ",rgb3[0])
            #         # print("this print 2= ",rgb3[1])
            #         # print("this print 3= ",rgb3[2])
            #         xy=single[2]
            #         #print(xy)
            #         xy2=xy.replace('(','').replace(')','')
            #         xy3=xy2.split(',')
            #         # print("this is x ",xy3[0])
            #         # print("this is y ",xy3[1])
            #         print(f'"STORE" : [{RegD[rgb3[0]]},{RegD[rgb3[1]]},{RegD[rgb3[2]]}],"xy": [ {RegD[xy3[0]]},{RegD[xy3[1]]} ]   ')
            #         #print(RegD[rgb3[0]])for instructblock in data:
                    
            # print(RegD)
            # print("\n")  

if __name__ == "__main__":
    processMessage()