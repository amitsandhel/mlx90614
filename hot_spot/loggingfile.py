#!/usr/bin/python
#loggingfile.py

'''NOTE THIS IS A DEPRECATED CLASS MUST BE DELETED''' 
import sys
import os
import time
import logging
import glob
import logging.handlers

'''Logging class that handles the logging of all files 

'''

#https://docs.python.org/2/howto/logging-cookbook.html#using-file-rotation
#https://docs.python.org/2/library/logging.handlers.html#rotatingfilehandler

LOG_FILENAME = os.path.relpath(".\logs\main.log")
    
class Logging_File():
    def __init__(self, logger_name=LOG_FILENAME, level=logging.DEBUG): # log_file, level=logging.DEBUG):
        #self.log_file = log_file
        self.level = level
        self.name = logger_name
        self.l = logging.getLogger(logger_name)
        self.setup_logger()
        
    def setup_logger(self): #, logger_name, log_file, level=logging.DEBUG):
        """This function is designed for logging setup"""
        formatter = logging.Formatter('%(asctime)s, %(levelname)s, %(message)s')
        
        #fileHandler = logging.FileHandler(self.log_file, mode='a')
        #fileHandler.setFormatter(formatter)
        
        rotateHandler = logging.handlers.RotatingFileHandler(self.name, mode='a', maxBytes=0, backupCount=2, encoding='utf-8', delay=0) # backupCount=2, encoding=None, delay=0)
        rotateHandler.setFormatter(formatter)
        
        rotateHandler.doRollover()
        
        #streamHandler = logging.StreamHandler()
        #streamHandler.setFormatter(formatter)
        
        
        self.l.setLevel(self.level)
        #self.l.addHandler(fileHandler)
        self.l.addHandler(rotateHandler)
        
        #rotateHandler.doRollover()
        
        
        #uncommenting this line below allows you to print all the logs to the dos terminal
        #self.l.addHandler(streamHandler)  
    
    def run(self):
        self.setup_logger()
        
        

###############################################################################
if __name__ == '__main__':
    myfile = Logging_File()
    myfile.setup_logger()

