#!/usr/bin/python
import sys
import argparse
import subprocess
import logging

'''main.py
'''

logging.basicConfig(filename='main.log', filemode='a', level=logging.DEBUG, format='%(asctime)s, %(levelname)s, %(message)s')
logging.info(" ---------------------- root --------------------------------")


def setup_parser():
    '''parser arguments '''
    parser = argparse.ArgumentParser(description='Mlx90614 sensor.')
    parser.add_argument('-sim', '-s', help='run simulator', action="store_true")
    parser.add_argument('-test', '-t',  help='Run unit tests', action="store_true")
    parser.add_argument('-debug', '-d', help='more verbose debug', action='store_true')
    return parser

class Main():
    def __init__(self, parser):
        '''initalize all variables as needed including those passed in from the parser'''
        #partial parsing being done makes a tuple
        self.args = parser.parse_args()  
        self.logging = logging.getLogger('main.log')
        self.logging.debug("self.arg parser values: " + repr(self.args) )
    
    def get_command(self):
        '''using a conditional expression to run the command'''
        COMMAND = 'python mlx90614_sim.py' if self.args.sim == True else 'python mlx90614.py'
        return COMMAND
        
    def run_sub(self, command):
        '''Function that runs the subprocess command to determine which subprocess to run'''
        #first test to see if test is True
        if self.args.test == True:
            subprocess.call ('python control_variable_test.py', shell=True)
            subprocess.call ('python mlx90614_sim_test.py', shell=True)
            subprocess.call ('python sensor_setupconfig_test.py', shell=True)
        else:
            #run the real code with or without simulator
            subprocess.call(command, shell = True)
    
    def run(self):
        ''''Execute the Main() class with various settings'''
        try:
            default_command = self.get_command()
            self.run_sub(default_command)
            
            self.logging.debug("Main.py Main().run() function successful" )
            self.logging.debug("Main.py Main().run() default_command COMMAND value: "  + repr(default_command) )
        except (KeyboardInterrupt, SystemExit):
            print 'software closing thank you and have a good day'
            sys.exit()
        
        
#######################################################################
if __name__ == '__main__':
    print "Welcome to Mlx90614 Hot Spot Sensor Software"
    parser = setup_parser()
    b = Main(parser)
    b.run()
