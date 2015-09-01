#!/bin/bash

#from future import division has to be done atthe top of the value
from __future__ import division
import logging
from loggingfile import Logging_File as Log_File

Log_File('Control_Variable().log') 


class Control_Variable():
	'''This class controls the output and the variable setting of the 4 control settings the temperature limit
	and the jump limit 
	'''
	def __init__(self):
		self.limit_value = 0.01 #1%  in decimal form
		self.jump_value = 0.5
		
		#tuple for answer output
		self.answer = ()
		
		
		self.logger = logging.getLogger('Control_Variable()')
		self.logger.info(" ---------------------- root --------------------------------")
		
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
			self.logger.debug('incorrect parameters passed')
	
	def report_control(self):
		'''report the control setting values'''
		#print 'a: ', self.limit_value
		#print 'b: ', self.jump_value
		
		#store the answer as a tuple and report the value back as a tuple
		self.answer = (self.limit_value, self.jump_value)
		self.logger.debug('control values: ' + repr(self.limit_value) + repr(self.jump_value) )
		self.logger.debug('control values: ' + repr(self.answer) )
		#return (self.limit_value, self.jump_value)
	
	def run(self, limitvalue=1, jumpvalue=0.5):
		'''function which runs the above commands
		'''
		self.control_setpoint(limit=limitvalue, jump=jumpvalue)
		self.report_control()
	


class Main():
	def __init__(self):
		self.myfile = Control_Variable()
		
	def run(self):
		self.myfile.run()
		#self.myfile.control_setpoint(limit=1, jump=0.5)
		#self.myfile.report_control()

##################################################################
if __name__ == '__main__':
	b = Main()
	b.run()


