from comms import Receiver
from comms import mykwargs
import sys
import json

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
def usage():
    print("Usage: receiver.py <host> <port> <exchange> <routing_keys> ")
    print("Usage: receiver.py 164.90.134.137 5672 cpuproject 'sports,news' ")
    sys.exit()

def processMessage(ch, method, properties, body):
        #print(f"I will not beat off any more")
        data = json.loads(body.decode())
        outfile="messagedata.dat"
        with open(outfile, 'w',) as outfile:
            for instructblock in data1:
                for line in instructblock:
                    print(line)
                    outfile.write(line +'\n')
                
               




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
