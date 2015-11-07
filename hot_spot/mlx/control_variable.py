#!/bin/bash

#from future import division has to be done atthe top of the value
from __future__ import division
import sys
import os
import logging
import logging.handlers
import config.config

'''
Developing the log files
log file size is to be 109 K (100 kilobytes) and is about 2 "backups"
NOTE: SEE mlx90614_sim test10() for ERRORS associated with rotating file handlers
'''

#LOG_FILENAME = os.path.relpath(".\logs\main.log")
#formatter = logging.Formatter('%(asctime)s, %(levelname)s, %(message)s')

# Set up a specific logger with our desired output level
#mylog3 = logging.getLogger('MyLogger3')
#mylog3.setLevel(logging.DEBUG)

# Add the log message handler to the logger
#handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=100000, backupCount=2)
#handler.setFormatter(formatter)

#mylog3.addHandler(handler)

logging.basicConfig(filename='main.log', filemode='a', level=logging.DEBUG, format='%(asctime)s, %(levelname)s, %(message)s')
logging.info(" ---------------------- root --------------------------------")
mylog3 = logging.getLogger('main')

#import loggingfile


class Control_Variable():
	'''This class controls the output and the variable setting of the 4 control settings the temperature limit
	and the jump limit 
	'''
	def __init__(self):
		"""instantiating value """
		#opening the  config file 
		self.config = config.config.Config()
		#self.config.run()
		
		self.jump_value = float(self.config.dict['jump_value'])
		self.limit_value =  float(self.config.dict['limit_value'])
		
		#tuple for answer output
		self.answer = ()
		
		#run the run() function during class initalization 
		self.run()
		mylog3.info(" ---------------------- root --------------------------------")
		
	def control_setpoint(self, limit, jump):
		'''THis function takes in the limit and the jump parameter you wish to change'''
		#reintializing the values
		#using a try and except loop to catch incorrect parameters and errors 
		try:
			self.limit_value = abs(limit/100)
			self.jump_value = abs(jump)
		except TypeError:
			#changing to default values 
			print 'incorrect paramters passed using default values'
			self.limit_limit_value = 0.01
			self.jump_value = 0.5
			mylog3.debug('incorrect parameters passed')
			
	def report_control(self):
		'''report the control setting values'''
		#store the answer as a tuple and report the value back as a tuple
		self.answer = (self.limit_value, self.jump_value)
		
		#logging the result
		#mylog3.debug('(Limit Value, Jump Value) tuple: ' + repr(self.answer) )
	
	def run(self): #, limitvalue=1, jumpvalue=0.5):  #does this need any default values as safety precaution
		'''function which runs the above commands
		'''
		#setting teh config setting files 
		self.config.run()
		
		self.jump_value = float(self.config.dict['jump_value'])
		self.limit_value = float(self.config.dict['limit_value'])
		
		#setting and running the insanting values 
		self.control_setpoint(limit=self.limit_value, jump=self.jump_value) #limit=limitvalue, jump=jumpvalue)
		self.report_control()
		
		#this was knocked out becuase the log file went crazy
		#mylog3.debug('Limit Value: ' + repr(self.limit_value) )
		#mylog3.debug('Jump Value: ' + repr(self.jump_value) )

class Main():
	def __init__(self):
		self.myfile = Control_Variable()
		#opening the config class to get the dictionary we need out to set our parameters
		#running it here too like in Main 
		self.config = config.config.Config()
		#self.config.readconfig() 
		
	def run(self):
		jumpvalue = float(self.config.dict['jump_value'])
		limitvalue = float(self.config.dict['limit_value'])
		
		self.myfile.run(limitvalue, jumpvalue)

##################################################################
if __name__ == '__main__':
	b = Main()
	b.run()


