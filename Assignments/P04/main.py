""" Distributed Instructions Simulation Program"""
import os
from rich import print
from rich.table import Table
from rich.console import Console
from rich.layout import Layout
import argparse
from receiver  import *
from sender import * 
from comms import *


class MessageHandler:

    def receiver(self):
        """get message from core"""
        pass

    def passer(self):
        """ pass hex message to CPU"""
        pass
    
    def sender(self):
        """ send answer back to core"""
        pass

class CPU:
    
    def __init__(self):
        pass

    def parser(self):
        pass

    def passToALU(self):
        pass

    def passToRegister(self):
        pass

    def returnToMessageHandler(self):
        """create a packet with answer to return to messageHandler to be returned to core"""
        pass


class ALU:
    """
    Class methods handle only execution of operations
    """
    def __init__(self, register0, register1, register2, register3):
        self.operation = register0
        self.operand1 = register1
        self.operand2 = register2
        self.answer = register3


    def execute(self, operation, operand1, operand2, register3):
        """
        returns the value of the operation on the two operands passed into the function
        """
        # if/else conditions to match operation - pass to separate methods in ALU to carry out specific operation

        if self.operation =='add':
            register3 = self.add(self.operand1, self.operand2)
            return register3
        elif self.operation =='subtract':
            register3 = self.subtract(self.operand1, self.operand2)
            return register3 
        elif self.operation =='multiply':
            register3 = self.multiply(self.operand1, self.operand2)
            return register3
        elif self.operation =='divide':
            register3 = self.divide(self.operand1, self.operand2)
            return register3
        elif self.operation =='modulo':
            register3 = self.modulo(self.operand1, self.operand2)
            return register3
        
    def add(self, operand1, operand2):
        result = operand1 + operand2
        return result
             
    def subtract(self, operand1, operand2):
        result = operand1 - operand2
        return result

    def multiply(self, operand1, operand2):
        result = operand1 * operand2
        return result

    def divide(self, operand1, operand2):
        result = operand1 / operand2
        return result
    
    def modulo(self, operand1, operand2):
        result = operand1 % operand2
        return result



class Registers:
    pass


if __name__ == "__main__":
    exit


