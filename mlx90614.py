#!/bin/bash

''' This scipt is designed o red the values fom the MLX9061 IR 
temperature senso
'''
#from future import division has to be done atthe top of the value
from __future__ import division
import sys
from smbus import SMBus
import time
import logging
from loggingfile import Logging_File as Log_File

from control_variable import Control_Variable as control_variable
from linux_cmd_setup import Linux_Command as linux_cmd

#Setting up various log files

Log_File('tobj_jump_up') 
Log_File('tobj_jump_down') 
Log_File('tobj_limit_up', ) 
Log_File('tobj_limit_down') 

Log_File('tamb_jump_up') 
Log_File('tamb_jump_down') 
Log_File('tamb_limit_up') 
Log_File('tamb_limit_down') 




class MLX90614_IR_sensor():
	'''This class will read the IR temperatue values from the sensor'''
	def __init__(self, scalar=0.5, limit=10):
		'''Initalizing all variables primarily the address variables for ONE sensor
		for now'''
		
		#note that the default slave address is 0x00
		#TODO: how to detect several different addresses at once 
		self.address = 0x5a 
		#Objec temperature address
		self.tobj_address = 0x07
		#ambien temperature address
		self.tamb_address = 0x06
		
				
		#smbus command setup
		self.bus = SMBus(1) 
		
		self.init_tamb_value = 0.0
		self.init_tobj_value = 0.0
		
		#ambient temperature
		self.tamb_num = 0.0
		#object temperature
		self.tobj_num = 0.0
		
		self.tamb_final = 0.0
		self.tobj_final = 0.0
		
		self.tobj_limit = 0.0
		self.tamb_limit = 0.0
		
		self.control_class = control_variable()
		

		
		
		
		self.logger1 = logging.getLogger('tobj_jump_up')
		self.logger2 = logging.getLogger('tobj_jump_down')
		self.logger3 = logging.getLogger('tobj_limit_up')
		self.logger4 = logging.getLogger('tobj_limit_down')
		
		self.logger5 = logging.getLogger('tamb_jump_up')
		self.logger6 = logging.getLogger('tamb_jump_down')
		self.logger7 = logging.getLogger('tamb_limit_up')
		self.logger8 = logging.getLogger('tamb_limit_down')
		
		
	def read(self):
		'''getting the values from the IR device sensor'''
		self.init_tobj_value = self.bus.read_word_data(self.address, self.tobj_address)
		#sleep for 200 ms the time for the sensor is at least 144 ms
		time.sleep(0.2)
		
		self.init_tamb_value = self.bus.read_word_data(self.address, self.tamb_address)
		#sleep for 200 ms the timer for the sensor is at least 144 ms 
		time.sleep(0.2)
	
	def object_temp_analysis(self):
		'''this function converts the temperature from kelvin to celsius values'''
		#converting values from long bits into degrees celsius
		#using fomula in sensor datasheet manual
		#pg ?????
		#convert temperatures from kelvin to celsius
		tobj_ans = ( self.init_tobj_value*0.02 ) - 273.15
		#print tobj_ans
		#calculate jump value 
		jump_value = self.tobj_num - tobj_ans
		#print jump_value
		if jump_value >= 0.5:
			#assuming the value is + 
			#print 'yes tobj increase'
			#reinitalize varialbes 
			self.tobj_num = tobj_ans
			#print 'num up: ', self.tobj_num
			#calculate percent limit 
			tobj_percent_limit_up = self.tobj_num*self.control_class.limit_value
			#print 'limit up: ', tobj_percent_limit_up
			
			self.logger1.debug('object temperature value: '+ repr(self.tobj_num) + 'jump up value: ' + repr(jump_value) )
			self.logger3.debug( 'object temperature value: '+ repr(self.tobj_num)+ 'temp up limit: ' + repr(tobj_percent_limit_up) )
			
			print 'tobj up'
		
		elif jump_value <= (-0.5):
			#print 'yes temp object decreased'
			self.tobj_num = tobj_ans
			#print 'num: ', self.tobj_num
			tobj_percent_limit_down = self.tobj_num*self.control_class.limit_value
			#print 'limit down: ', tobj_percent_limit_down
			
			self.logger2.debug('object temperature value: '+ repr(self.tobj_num) + 'jump down value: ' + repr(jump_value) )
			self.logger4.debug('object temperature value: '+ repr(self.tobj_num) + 'temp down limit: ' + repr(tobj_percent_limit_down) )
			
			print 'tobj down'
			
		else:
			print 'no change'
	
	def ambient_temp_analysis(self):
		tamb_ans = ( self.init_tamb_value*0.02 ) - 273.15
		#print tobj_ans
		#calculate jump value 
		jump_value = self.tamb_num - tamb_ans
		#print jump_value
		if jump_value >= 0.5:
			#assuming the value is + 
			#reinitalize varialbes 
			self.tamb_num = tamb_ans
			
			#calculate percent limit 
			tamb_percent_limit_up = self.tamb_num*self.control_class.limit_value
			
			self.logger5.debug('ambient temperature value: '+ repr(self.tamb_num) )
			self.logger7.debug('jump value: ' + repr(jump_value) + 'temp limit: ' + repr(tamb_percent_limit_up) )
			
			print 'tamb up'
			
		elif jump_value <=(-0.5):
			#print 'yes temp object decreased'
			self.tamb_num = tamb_ans
			#print 'num: ', self.tobj_num
			tamb_percent_limit_down = self.tamb_num*self.control_class.limit_value
			#print 'limit down: ', tobj_percent_limit_down
			self.logger6.debug('ambient temperature value: '+ repr(self.tamb_num) )
			self.logger8.debug('jump value: ' + repr(jump_value) + 'temp limit: ' + repr(tamb_percent_limit_down) )
			
			print 'tamb down'
			
			
		else:
			print 'no change'
		
	def run(self):		
		''''Function which runs the value'''
		cycle=0
		while True:
			cycle+=1
			print 'cycle: ', cycle
			self.read()
			self.object_temp_analysis()
			self.ambient_temp_analysis()
			print 'tobject: %s -- tambient: %s'%(self.tobj_num, self.tamb_num) 
	

class Main():
	def __init__(self):
		self.linux_cmd_setup = linux_cmd()
		
		self.myfile = MLX90614_IR_sensor( )
		self.myfile.control_class.__init__(1, 0.5)
		
	
	def linux_setup(self):
		'''running the linux_cmd_setup Main.run() function to activate
		command transaction commands
		'''
		self.linux_cmd_setup.run()
		
	def run(self):
		self.linux_setup()
		try:
			self.myfile.run( )
		except (KeyboardInterrupt, SystemExit):
			print 'clsoing program thank you and have a good day'
			sys.exit()

##################################################################
if __name__ == '__main__':
	myfile = Main()
	myfile.run()
	
	#Main()


