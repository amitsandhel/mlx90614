#!/usr/bin/python

'''Copyright Amit Sandhel
This software is the mian software that runs everyone else

main.py

'''
#REFERENCE FILES
#https://docs.python.org/2/library/unittest.html
#https://docs.python.org/2/tutorial/modules.html#packages
#http://mikegrouchy.com/blog/2012/05/be-pythonic-__init__py.html
#https://docs.python.org/2/library/os.html#os.curdir

import sys
import os
import argparse
import subprocess
import logging
import logging.handlers

#import testing files
import unittest 
import tests.control_variable_test
import tests.sensor_setupconfig_test
import tests.mlx90614_sim_test

import config.config

import sim.mlx90614_sim
#from sim.mlx90614_sim import Main as myMain

import wxmain

#catching import error on library
try:
    import mlx.mlx90614
    #Instantate the MyMain class of the real class
    MYMAIN2 = mlx.mlx90614.Main()
except ImportError:
    print 'error the mlx90614.py library does not exist'
    #set the MYMAIN variable to none (there is no library)
    MYMAIN2 = None


'''
Developing the log files
log file size is to be 109 K (100 kilobytes) and is about 2 "backups"
NOTE: SEE mlx90614_sim test10() for ERRORS associated with rotating file handlers
'''
#os.path.relpath("\logs", os.curdir ) # if you have python 2.6

#LOG_FILENAME = os.path.relpath(".\logs\main.log") #, os.curdir ) #os.path.abspath("E:\Raspberry Pi Project\hot_spot\logs\main.log")
#formatter = logging.Formatter('%(asctime)s, %(levelname)s, %(message)s')

# Set up a specific logger with our desired output level
#mylog = logging.getLogger('MyLogger')
#mylog.setLevel(logging.DEBUG)

# Add the log message handler to the logger
#handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=100000, backupCount=2)
#handler.setFormatter(formatter)

#mylog.addHandler(handler)

logging.basicConfig(filename='main.log', filemode='a', level=logging.DEBUG, format='%(asctime)s, %(levelname)s, %(message)s')
logging.info(" ---------------------- root --------------------------------")
mylog = logging.getLogger('main')


def setup_parser():
    '''parser arguments '''
    parser = argparse.ArgumentParser(description='Mlx90614 sensor.')
    parser.add_argument('-sim', '-s', help='run simulator', action="store_true")
    parser.add_argument('-test', '-t',  help='Run unit tests', action="store_true")
    parser.add_argument('-gui', '-g', help='run the program via a Graphical User Interface (GUI)', action='store_true')
    return parser
    

class Main():
    def __init__(self, parser):
        '''initalize all variables as needed including those passed in from the parser'''
        #partial parsing being done makes a tuple
        self.args = parser.parse_args()  
        #default value initalized
        self.args.sim = self.args.sim #False
        self.args.gui = self.args.gui #False
        self.args.test = self.args.test #False
        
        #sim file 
        self.simfile = sim.mlx90614_sim.Main()  
        #store and instantiate memory address
        self.gui_file = wxmain.MyApp
        #real file
        self.myfile = MYMAIN2
        #OPENING CONFIG FILE
        self.configfile = config.config.Config()
        #run the file 
        #self.configfile.run()
        
        #INITALIZING LOG FILES
        mylog.info('***************Info*****************')
    
    def run_setup(self):
        '''Function that setups the classes and runs them based on the needs
        Note that the setting is only used once
        '''
        #is the Gui going to be used or not
        if self.args.gui == True:
            #if it is then run the gui
            #run the gui loop 
            app = self.gui_file(0)
            app.MainLoop()
        else:
            #the gui is not going to be used
            #if the sim parameter is set to True
            if self.args.sim == True:
                #run the main function
                self.simfile.run()
            else:
                #run the Main.run() function of the real class
                self.myfile.run()
    
    def run_test_suite(self):
        '''Function that setups the test suite and runs it'''
        '''If tests is true then we run the test scripts note we are suing TextTestRunner to run all the classes at once
        '''
        #WE have removed the weird subprocess.call() function for testing purposes 
        #combining the test cases and loading them into suites:
        #control_variable_test      
        suite1 = unittest.TestLoader().loadTestsFromTestCase(tests.control_variable_test.Control_Variable_Test)
        #sensor_setupconfig_test
        suite2 = unittest.TestLoader().loadTestsFromTestCase(tests.sensor_setupconfig_test.Sensor_setupconfig_Test)
        #mlx90614_sim_test
        suite3 = unittest.TestLoader().loadTestsFromTestCase(tests.mlx90614_sim_test.MLX90614_Test)
        #combine all the suites into a list
        alltests = unittest.TestSuite([suite1, suite2, suite3])
        
        #Use TestRunner to run the test package
        unittest.TextTestRunner(verbosity=1).run(alltests)
    
    def run(self):
        ''''Execute the Main() class with various settings'''        
        try:
            #run the test suite if the test suite is real
            if self.args.test==True: 
                print 'Running Tests'
                self.run_test_suite() 
                
            #run the configfile
            #self.configfile.run()
            
            #run the setup feature
            self.run_setup()
            
        except (KeyboardInterrupt, SystemExit):
            print 'software closing thank you and have a good day'
            sys.exit()
        
#######################################################################
if __name__ == '__main__':
    print "Welcome to Mlx90614 Hot Spot Sensor Software"
    parser = setup_parser()
    b = Main(parser)
    b.run()
