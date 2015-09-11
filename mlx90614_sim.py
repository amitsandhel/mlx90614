#!/bin/bash

''' This scipt is designed to read the values fom the MLX9061 IR 
temperature sensor
'''

#http://www.tutorialspoint.com/python/python_dictionary.htm

#from future import division has to be done atthe top of the value
from __future__ import division
import sys
import time
import random
import logging
from loggingfile import Logging_File as Log_File
from main import setup_parser as sp
from control_variable import Control_Variable as control_variable
from linux_cmd_setup import Linux_Command as linux_command


#REFERENCES
#https://docs.python.org/2/library/random.html


#logging.basicConfig(filename='mlx90614_sim.log', filemode='a', level=logging.DEBUG, format='%(asctime)s, %(levelname)s, %(message)s')
#logging.info(" ---------------------- root --------------------------------")
#Log_File('tobj_jump_up') 
#Log_File('tobj_jump_down')
#Log_File('tobj_limit_up', ) 
#Log_File('tobj_limit_down') 

#Log_File('tamb_jump_up') 
#Log_File('tamb_jump_down')
#Log_File('tamb_limit_up') 
#Log_File('tamb_limit_down') 

Log_File('XXX') 

# SETTING UP CSV FILE
FILENAME = "MLX-Sensor-Data.csv"
NEWLINE = "\n"


class MLX90614_IR_sensor():
	'''This class will read the IR temperatue values from the sensor 
	'''
	def __init__(self, address):
		'''Initalizing all variables 
		'''
		#address working at 
		self.address = address
		
		#inital ambient and object temperatures
		self.init_tamb_value = 0.0
		self.init_tobj_value = 0.0
		
		#ambient temperature
		self.tamb_num = 0.0
		#object temperature
		self.tobj_num = 0.0
		
		self.tobj_percent_limit_up=0.0
		self.tobj_percent_limit_down=0.0
		
		#importing the control_variable() class to obtain the jump and limit values
		self.control_class = control_variable()
		
		#various logging files
		self.logger1 = logging.getLogger('XXX')
		
		#self.logger1 = logging.getLogger('tobj_jump_up')
		#self.logger2 = logging.getLogger('tobj_jump_down')
		#self.logger3 = logging.getLogger('tobj_limit_up')
		#self.logger4 = logging.getLogger('tobj_limit_down')
		
		#self.logger5 = logging.getLogger('tamb_jump_up')
		#self.logger6 = logging.getLogger('tamb_jump_down')
		#self.logger7 = logging.getLogger('tamb_limit_up')
		#self.logger8 = logging.getLogger('tamb_limit_down')
		
		self.jump_value = 0.0
		self.cycle = 0
		
	def read(self):
		'''getting the values from the IR device sensor
		Note: In this case we are using a random number generator '''
		#generating object value from random number generator
		self.init_tobj_value = random.randrange(14657, 15000) 
		
		#sleep for 200 ms the time for the sensor is at least 144 ms
		time.sleep(0.2)
		
		#generating ambient temperature from randon number generator
		self.init_tamb_value = random.randrange(14657, 16657)
		#time delay of 200 ms 
		time.sleep(0.2)
		
	def object_temp_analysis(self):
		'''this function converts the object temperature from kelvin to celsius values'''
		#converting values from long bits into degrees celsius
		#using fomula in sensor datasheet manual
		#pg ?????
		
		#convert temperatures from kelvin to celsius
		tobj_ans = ( self.init_tobj_value*0.02 ) - 273.15
		
		self.logger1.debug('tobj ' + repr(tobj_ans) )
		
		#calculate jump value 
		jump_value = self.tobj_num - tobj_ans
		
		self.jump_value = jump_value
		
		#comparing jump value to control jump value set by user
		if jump_value >= self.control_class.jump_value: #0.5:
			#reinitalize variables 
			self.tobj_num = tobj_ans
			#calculate percent limit 
			self.tobj_percent_limit_up = self.tobj_num*self.control_class.limit_value
			
			self.logger1.debug('object temperature value: '+ repr(self.tobj_num) + 'jump up value: ' + repr(jump_value) )
			#self.logger3.debug( 'object temperature value: '+ repr(self.tobj_num)+ 'temp up limit: ' + repr(self.tobj_percent_limit_up) )
			self.logger1.debug( 'object temperature value: '+ repr(self.tobj_num)+ 'temp up limit: ' + repr(self.tobj_percent_limit_up) )
			
		elif jump_value <= self.control_class.jump_value: #(-0.5):
			#reinitalize variables
			self.tobj_num = tobj_ans
			#calculating percent limit
			self.tobj_percent_limit_down = self.tobj_num*self.control_class.limit_value
			
			self.logger1.debug('object temperature value: '+ repr(self.tobj_num) + 'jump down value: ' + repr(jump_value) )
			self.logger1.debug('object temperature value: '+ repr(self.tobj_num) + 'temp down limit: ' + repr(self.tobj_percent_limit_down) )
			
			#self.logger2.debug('object temperature value: '+ repr(self.tobj_num) + 'jump down value: ' + repr(jump_value) )
			#self.logger4.debug('object temperature value: '+ repr(self.tobj_num) + 'temp down limit: ' + repr(self.tobj_percent_limit_down) )
		
		else:
			print 'no change'
		
	def ambient_temp_analysis(self):
		'''this function records the ambient temperatuer and converts the value to degrees celsisus
		'''
		tamb_ans = ( self.init_tamb_value*0.02 ) - 273.15
		
		self.logger1.debug('tamb ans: ' + repr(tamb_ans) )
		
		#calculate jump value 
		jump_value = self.tamb_num - tamb_ans

		if jump_value >= self.control_class.jump_value: #0.5:
			#assuming the value is + 
			#reinitalize varialbes 
			self.tamb_num = tamb_ans
			
			#calculate percent limit 
			tamb_percent_limit_up = self.tamb_num*self.control_class.limit_value
			
			self.logger1.debug('ambient temperature value: '+ repr(self.tamb_num) )
			self.logger1.debug('jump value: ' + repr(jump_value) + 'temp limit: ' + repr(tamb_percent_limit_up) )
			
			#self.logger5.debug('ambient temperature value: '+ repr(self.tamb_num) )
			#self.logger7.debug('jump value: ' + repr(jump_value) + 'temp limit: ' + repr(tamb_percent_limit_up) )
		
		elif jump_value <=self.control_class.jump_value: #(-0.5):
			#reinitalize variables
			self.tamb_num = tamb_ans
			
			#calculate percent limit 
			tamb_percent_limit_down = self.tamb_num*self.control_class.limit_value
			
			self.logger1.debug('ambient temperature value: '+ repr(self.tamb_num) )
			self.logger1.debug('jump value: ' + repr(jump_value) + 'temp limit: ' + repr(tamb_percent_limit_down) )
			
			#self.logger6.debug('ambient temperature value: '+ repr(self.tamb_num) )
			#self.logger8.debug('jump value: ' + repr(jump_value) + 'temp limit: ' + repr(tamb_percent_limit_down) )
		
		else:
			print 'no change'
	
	def record_data(self):
		'''this function saves the data to csv files note that this data is not needed and necessary
		TODO: Deprecated function '''
		myfile = open(FILENAME, 'a')
		newrow = time.strftime('%H:%M:%S,')
		newrow += str(self.cycle) + ","
		newrow += str(self.address) + ","  
		newrow += str(self.tobj_num) + ","  
		newrow += str(self.tamb_num) + ","  
		newrow += str(self.jump_value)		
		newrow += NEWLINE
		myfile.write(newrow)
		myfile.close()
		
	def run(self):
		''''Function which runs the value'''
		self.cycle+=1
		print 'cycle: ', self.cycle
		
		self.read()
		self.object_temp_analysis()
		self.ambient_temp_analysis()
		self.record_data()
		
		print 'Address: %s -- tobject: %s -- tambient: %s'%(self.address, self.tobj_num, self.tamb_num)
		print 'limit up: %s -- limit down: %s '%(self.tobj_percent_limit_up, self.tobj_percent_limit_down )		


class Main():
	def __init__(self):
		#self.myfile = MLX90614_IR_sensor( )
		#self.myfile.control_class.control_setpoint(2, 1)
		
		self.sensorfile = linux_command()
		self.class_list = []
	
	def function_setup(self):
		for item in self.sensorfile.simulator_list:
			IR_class = MLX90614_IR_sensor(item)
			IR_class.control_class.control_setpoint(2, 1)
			self.class_list.append(IR_class)
					
	def run(self):
		myfile = open(FILENAME, "a")
		myfile.write("Time,Cycle, address, Tobject, Tambient, jumpvalue" + NEWLINE)
		myfile.close()
		
		self.function_setup()
		try:
			while True:
				for item in self.class_list:
					item.run()
		except (KeyboardInterrupt, SystemExit):
			print 'clsoing program thank you and have a good day'
			sys.exit()


############################################################################
if __name__ == '__main__':
	myfile = Main()
	myfile.run()
	
	#Main()

