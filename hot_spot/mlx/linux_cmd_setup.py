#!/usr/bin/python

#linux_cmd_setup.py

import sys
import os
import subprocess
import logging 
from loggingfile import Logging_File as Log_File

#LOG_FILENAME = os.path.relpath(".\logs\main.log")
#formatter = logging.Formatter('%(asctime)s, %(levelname)s, %(message)s')

# Set up a specific logger with our desired output level
#mylog4 = logging.getLogger('MyLogger2')
#mylog4.setLevel(logging.DEBUG)

# Add the log message handler to the logger
#handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=100000, backupCount=2)
#handler.setFormatter(formatter)

#mylog4.addHandler(handler)

logging.basicConfig(filename='main.log', filemode='a', level=logging.DEBUG, format='%(asctime)s, %(levelname)s, %(message)s')
logging.info(" ---------------------- root --------------------------------")
mylog4 = logging.getLogger('main')


'''
THis script is designed to run all the linux commands we need to run our main script 
the commands we need is to set the combined parameter to yes
and to give super user access to the script 
though if we do an auto on the srcript we may not need to 

auto on log in is the most safest proecudre you log in first and then check it out
'''

class Linux_Command():
	def __init__(self):
		'''This class is designed to use subprocess to run all the linux commands needed'''
		#find the slave addresst to all the sensors attached
		self.i2cdetect_command = 'sudo i2cdetect -y 1'
		
		#usb command activation deprecated functoion as usb can be run in auto mode too
		#TOD: may or may not be used and needed
		self.ls_command = 'sudo ls -l /dev/disk/by-uuid/'
		self.chown_command = 'sudo chown -R pi:pi usb'
		self.mount_command = 'sudo mount /dev/sda1 usb -o uid=pi,gid=pi'
		#possible values we will ignore when parsing the address string table
		self.possible_values = ['--', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f',
				'00:', '10:', '20:', '30:', '40:', '50:', '60:', '70:']
		
		#the intermediary self.address list 
		self.address_list = []
		#all the useless variables that are not needed coming from sudo i2cdetect parse
		self.useless_list = []
		# this is the final address list that is sent to the mlx script for address
		self.final_address_list = []
		#this list is passed to the simulator 
		self.simulator_list = [0x5a, 0x5b]
		
		#self.logger = logging.getLogger('Linux_Commands.log')
		mylog4.info("************ROOT-Linux-CMd-Setup**************")
	
	def i2c_detect_cmd(self):
		'''this function sets the i2cdetect and parses the address to obtain the adress cal
		Note: 
		'''
		subprocess.call(self.i2cdetect_command, shell=True)
		ans = subprocess.check_output(self.i2cdetect_command, shell=True)
		parse_string =  ans.strip().split('\n')
		for item in parse_string:
		    b=item.strip().split()
		    for value in b:
			if value in self.possible_values:
			    self.useless_list.append(value)
			else:
			    self.address_list.append(value)
		print 'address list: ', self.address_list
		
		mylog4.debug('address string: ' + repr(ans) ) 
		mylog4.debug('address_list: ' + repr(self.address_list) )
		mylog4.debug('useless_list: ' + repr(self.useless_list) )
	
	def address_setup(self):
		'''this function sets the i2cdetect and parses the address to obtain the adress cal
		Note: 
		'''
		for item in self.address_list:
			ans = '0x' + item
			print ans
			value = int(ans, 16) 
			print value
			self.final_address_list.append(value)
		print 'add: ', self.final_address_list
		
	def usb_setup(self):
		'''this function sets up the usb and allows the usb to be read
		TODo: it is possible to automate this componet in linux and hence this is 
		a deprecated and useless function
		'''
		subprocess.call(self.ls_command, shell=True)
		subprocess.call(self.chown_command, shell = True)
		subprocess.call(self.mount_command, shell=True)
		
	def run(self):
		'''this function will run the self commands using the subprocess call'''
		self.usb_setup()
		self.i2c_detect_cmd()
		self.address_setup()
		


    
class Main():
	def __init__(self):
		self.linux_setup = Linux_Command()
	
	def run(self):
		self.linux_setup.run()

#######################################################################
if __name__ == '__main__':
    myfile = Main()
    myfile.run()
    

        
        
        