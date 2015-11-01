#!/bin/bash

''' This scipt is designed to read the values fom the MLX9061 IR 
temperature sensor
'''

#http://www.tutorialspoint.com/python/python_dictionary.htm
#http://stackoverflow.com/questions/1024847/add-key-to-a-dictionary-in-python

#from future import division has to be done atthe top of the value
from __future__ import division
import sys
import os
from smbus import SMBus
import time
import logging
import logging.handlers

import threading
import Queue

import mlx.control_variable

from mlx.linux_cmd_setup import Linux_Command as linux_command

import config.config

#REFERENCES
#https://docs.python.org/2/library/random.html

'''
Developing the log files
log file size is to be 109 K (100 kilobytes) and is about 2 "backups"
NOTE: SEE mlx90614_sim test10() for ERRORS associated with rotating file handlers
'''

logging.basicConfig(filename='mlx_sim.log', filemode='a', level=logging.DEBUG, format='%(asctime)s, %(levelname)s, %(message)s')
logging.info(" ---------------------- root --------------------------------")
mylog2= logging.getLogger('mlx_sim')


# SETTING UP CSV FILE
FILENAME = "MLX-Sensor-Data-combo.csv"
NEWLINE = "\n"


class MLX90614_IR_sensor():
	'''This class will read the IR temperatue values from the sensor'''
	def __init__(self, address):
		'''Initalizing all variables 
		'''
		#address working at 
		self.address = address
		
		
		#note that the default slave address is 0x00
		#TODO: how to detect several different addresses at once 
		#self.address = 0x5a 
		
		#Objec temperature address
		self.tobj_address = 0x07 #0x27
		
		#ambien temperature address
		self.tamb_address = 0x06 #0x26
				
		#smbus command setup
		self.bus = SMBus(1) 
		
		#inital ambient and object temperatures
		self.init_tamb_value = 0.0
		self.init_tobj_value = 0.0
		
		#inital tamb and tobj values converted to Celsius 
		self.tamb_ans= 0.0
		self.tobj_ans= 0.0
		
		#ambient temperature
		self.tamb_num = 0.0
		#object temperature
		self.tobj_num = 0.0
		
		self.tobj_percent_limit_up=0.0
		self.tobj_percent_limit_down=0.0
		self.tamb_percent_limit_up=0.0
		self.tamb_percent_limit_down=0.0
		
		#importing the control_variable() class to obtain the jump and limit values
		self.control_class = mlx.control_variable.Control_Variable()
		self.control_class.run() #1,0.5)
		
		self.tobj_jump_value = 1.0 #0.0
		self.tamb_jump_value = 1.0 #0.0
		
		self.cycle = 0
		self.counter = 0
		
		self.tamb_data_analysis_list = []
		self.tobj_data_analysis_list = []
		
		self.tobj_data_analysis_result = []
		self.tamb_data_analysis_result = []
		
		#this is the record_list which is the varible passed to the gui 
		#note that we are initalizing all variables with 0 are the six variables are there
		#the appended list data is being stored to the log files, the gui will only show a subaspect of the data
		self.record_list = [0,0,0,0,0,0]
		self.record_dict = {self.address: []} #, 'cycle':self.cycle }
	'''	
	def read(self):
		#''getting the values from the IR device sensor''
		if self.address == 90:
			self.init_tobj_value = self.bus.read_word_data(self.address, self.tobj_address)
			#sleep for 200 ms the time for the sensor is at least 144 ms
			time.sleep(0.2)
			
			self.init_tamb_value = self.bus.read_word_data(self.address, self.tamb_address)
			#sleep for 200 ms the timer for the sensor is at least 144 ms 
			time.sleep(0.2)
			
		elif self.address == 91:
			self.init_tobj_value = self.bus.read_word_data(self.address, 0x27)
			#sleep for 200 ms the time for the sensor is at least 144 ms
			time.sleep(0.2)
			
			self.init_tamb_value = self.bus.read_word_data(self.address, 0x26)
			#sleep for 200 ms the timer for the sensor is at least 144 ms 
			time.sleep(0.2)
		else:
			print 'pass something is wrong'
	'''
	def read(self):
		'''getting the values from the IR device sensor'''
		self.init_tobj_value = self.bus.read_word_data(self.address, self.tobj_address)
		#sleep for 200 ms the time for the sensor is at least 144 ms
		time.sleep(0.2)
			
		self.init_tamb_value = self.bus.read_word_data(self.address, self.tamb_address)
		#sleep for 200 ms the timer for the sensor is at least 144 ms 
		time.sleep(0.2)
	
	def object_temp_analysis(self):
		'''this function converts the object temperature from kelvin to celsius values'''
		#converting values from long bits into degrees celsius
		#using fomula in sensor datasheet manual
		#pg ?????
		
		#convert temperatures from kelvin to celsius
		tobj_ans = ( self.init_tobj_value*0.02 ) - 273.15
		#print tobj_ans
		self.tobj_ans = tobj_ans
		#mylog2.debug('Tobj: ' + repr(tobj_ans) )
		
		#calculate jump value 
		jump_value = tobj_ans - self.tobj_num #- tobj_ans
		#save calculated jump value to self value
		self.tobj_jump_value = jump_value
		
		#print 'obj jump: ', jump_value
		mylog2.debug('obj jump value: ' + repr(jump_value) )
		
		#comparing jump value to control jump value set by user
		if jump_value >= self.control_class.jump_value: 
			#reinitalize variables 
			self.tobj_num = tobj_ans
			#calculate percent limit 
			self.tobj_percent_limit_up = self.tobj_num*self.control_class.limit_value
			print '*****TOBJ UP*****'
			#mylog2.debug('*****UP*****')
			mylog2.debug('UP VALUE-Tobj:--> ' + 'object temperature value: '+ repr(self.tobj_num) + 
			'jump up value: ' + repr(jump_value) +'temp limit value: ' + repr(self.tobj_percent_limit_up)
			+ 'jump value: ' + repr(self.control_class.jump_value) )
			
		elif jump_value <= -(self.control_class.jump_value): 
			#reinitalize variables
			self.tobj_num = tobj_ans
			#calculating percent limit
			self.tobj_percent_limit_down = self.tobj_num*self.control_class.limit_value
			print '******TOBJ DOWN*****'
			#mylog2.debug('*****DOWN*****')
			mylog2.debug('DOWN VALUE-Tobj:--> ' + 'object temperature value: '+ repr(self.tobj_num) 
			+ 'jump up value: ' + repr(jump_value) +'temp limit value: ' + repr(self.tobj_percent_limit_down) 
			+'jump value: ' + repr(self.control_class.jump_value))
			
		else:
			print 'no change'
		
	def ambient_temp_analysis(self):
		'''this function records the ambient temperatuer and converts the value to degrees celsisus
		'''
		tamb_ans = ( self.init_tamb_value*0.02 ) - 273.15
		#print tamb_ans
		#mylog2.debug('tamb ans: ' + repr(tamb_ans) )
		self.tamb_ans = tamb_ans
		
		#calculate jump value 
		jump_value = tamb_ans - self.tamb_num #- tamb_ans
		#print 'amb jump: ', jump_value
		
		if jump_value >= self.control_class.jump_value: 
			#assuming the value is + 
			#reinitalize varialbes 
			self.tamb_num = tamb_ans
			
			#calculate percent limit 
			tamb_percent_limit_up = self.tamb_num*self.control_class.limit_value
			
			print '*********TAMB UP***********'
			
			mylog2.debug('UP VALUE-Tamb:-->' + 'Ambient temperature value: '+ repr(self.tamb_num) 
			+ 'jump up value: ' + repr(jump_value) +'temp limit value: ' 
			+ repr(self.tamb_percent_limit_up) + 'jump value: ' + repr(self.control_class.jump_value))
		
		elif jump_value <= -(self.control_class.jump_value): 
			#reinitalize variables
			self.tamb_num = tamb_ans
			#calculate percent limit 
			tamb_percent_limit_down = self.tamb_num*self.control_class.limit_value
			
			print '*********TAMB DOWN***********'
			
			mylog2.debug('DOWN VALUE-Tamb' + 'Ambient temperature value: '+ repr(self.tamb_num) 
			+ 'jump up value: ' + repr(jump_value) +'temp limit value: ' 
			+ repr(self.tamb_percent_limit_down) + 'jump value: ' + repr(self.control_class.jump_value))
		
		else:
			print 'no change'
	
	def data_analysis(self):
		'''This function does the data analysis for the data
		'''
		#appending items to list 
		self.tobj_data_analysis_list.append(self.tobj_ans) #_num)
		self.tamb_data_analysis_list.append(self.tamb_ans) #num)
		
		#doing tobject calculations
		tobj_min = min(self.tobj_data_analysis_list)
		tobj_max = max(self.tobj_data_analysis_list)
		tobj_sum = sum(self.tobj_data_analysis_list)
		tobj_len = len(self.tobj_data_analysis_list)
		tobj_avg = tobj_sum/tobj_len
		 
		#doign tambient claculations 
		tamb_min = min(self.tamb_data_analysis_list)
		tamb_max = max(self.tamb_data_analysis_list)
		tamb_sum = sum(self.tamb_data_analysis_list)
		tamb_len = len(self.tamb_data_analysis_list)
		tamb_avg = tamb_sum/tobj_len
		
		self.record_list=[tobj_min, tobj_max, tobj_avg, tamb_min, tamb_max, tamb_avg]
		
		#appending data to more scenes
		self.tobj_data_analysis_result.append( [self.address, time.strftime('%H:%M:%S,'), tobj_min, tobj_max, tobj_avg, tobj_len ] )
		self.tamb_data_analysis_result.append( [self.address, time.strftime('%H:%M:%S,'), tamb_min, tamb_max, tamb_avg, tamb_len] )
		
		#print 'tobj : ', self.tobj_data_analysis_result #[tobj_min, tobj_max, tobj_avg, tobj_len]
		#print 'tamb: ', self.tamb_data_analysis_result #[tamb_min, tamb_max, tamb_avg, tamb_len]
		mylog2.debug('tobj data analysis: ' + repr(self.tobj_data_analysis_result)  )
		mylog2.debug('tamb data analysis: ' + repr(self.tamb_data_analysis_result)  )
	
	def data_reset(self):
		'''this function resets the data analysis for the data analysis to zero, the list 
		#TODO: on the case the list gets too big, then the value should be notified to be reset
		'''
		#resetting the tobj and tamb lists to zero
		self.tobj_data_analysis = []
		self.tamb_data_analysis = []
		
		
		
	
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
		#runt the control class to ensure the varaibles are set right and can be changed as needed
		#self.control_class.run()
		mylog2.debug('control variable values: ' + repr(self.control_class.jump_value) + 
							"--" + repr(self.control_class.limit_value) )
		self.cycle+=1
		print 
		
		print 'cycle: ', self.cycle
		
		self.read()
		self.object_temp_analysis()
		self.ambient_temp_analysis()
		self.data_analysis()
		
		#commenting out function that is not needed
		#self.record_data()
		#self.record_list.append([self.address, self.tobj_num])
		#self.record_list.append(self.tobj_num)
		#self.record_dict[self.address].append(self.tobj_num)
		#self.record_dict['cycle']=self.cycle
		print 'Address: %s -- tobject: %s -- tambient: %s'%(self.address, self.tobj_num, self.tamb_num)
		#print 'dict: ', self.record_dict
		#print 'xxx: ', self.record_list
		#print len(self.record_list)
		#print 'limit up: %s -- limit down: %s '%(self.tobj_percent_limit_up, self.tobj_percent_limit_down )		
		mylog2.debug('tamb data analysis: ' + repr(self.tamb_data_analysis_result)  )


class Main(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.q = Queue.Queue()
		#initalizing the linux command to get the address list to iterate over
		self.sensorfile = linux_command()
		#this opens th control variable class 
		self.controlvariable = mlx.control_variable.Control_Variable() #Main() #control_variable()
		
		self.config = config.config.Config()
		self.config.readconfig() #self.config.run()
		
		
		
		#append the classes into the list
		self.class_list = []
		
		#flag value to end the thread
		self.end = False
		
		self.templimit = float(self.config.dict['limit_value']) #1
		self.jumplimit = float(self.config.dict['jump_value']) #0.5
		
		mylog2.debug("Main self.temp limit: " + repr(self.templimit) )
		mylog2.debug('Main self.jump limit: ' + repr(self.jumplimit) )

	def function_setup(self, temp, jump):
		'''This function instantiates the number of classesequal to the 
		number of sensors added or needed
		'''
		#iterating over the simulator list 
		for item in self.sensorfile.simulator_list:
			#self.controlvariable.run(temp, jump) #self.templimit, self.jumplimit)
			#call the class with the address
			IR_class = MLX90614_IR_sensor(item)
			#set the control varaible 
			
			#this value makes no set this does not set the control variable at all
			#IR_class.control_class.run(temp, jump) #(self.templimit, self.jumplimit) #2, 2)
			
			self.controlvariable.control_setpoint(self.templimit, self.jumplimit) #.run(self.templimit, self.jumplimit)#temp, jump) #self.templimit, self.jumplimit)
			
			self.class_list.append(IR_class)
		
		mylog2.debug('Class lists: ' + repr(self.class_list) )

	def read(self):
		"""This function reads the queue for new incoming data and sets parameters
		accordingly
		"""
		if self.q.qsize()>0:
			value =self.q.get()
			#print 'value: ', value
			if value[0] == 'end':
				self.end = value[1]
			if value[0] == 'temp':
				self.templimit = value[1]
			if value[0] == 'jump':
				self.jumplimit = value[1]
			#print 'self.end: ', self.end
			self.q.task_done()
			
		#f len(self.class_list) > 0:
		for item in self.class_list:
			item.control_class.control_setpoint(self.templimit, self.jumplimit)

	def run(self):
		myfile = open(FILENAME, "a")
		myfile.write("Time,Cycle, address, Tobject, Tambient, jumpvalue" + NEWLINE)
		myfile.close()
		
		self.read()
		
		self.function_setup(self.templimit, self.jumplimit)
		
		#print 'temp and jump limits: ', self.templimit, self.jumplimit
		
		try:
			timerx = time.clock()
			while True:
				timery = time.clock()
				ans = timery - timerx
				if ans >= 3.0:
					for item in self.class_list:
						#running the classes 
						item.run()
						mylog2.debug("Main.read self.temp limit: " + repr(self.templimit) + " - " + repr((self.jumplimit) ) )
						
					#redoing the timer
					timerx = time.clock()
					
				self.read()
				
				#reappending the new control variables 
				#self.controlvariable.run(self.templimit, self.jumplimit)
				
				#self.controlvariable.limit_value = self.templimit
				#self.controlvariable.jump_value = self.jumplimit
				
				#for item in self.class_list.append:
				#	item.controlvariable.control_setpoint(self.templimit, self.jumplimit)
				#self.controlvariable.control_setpoint(self.templimit, self.jumplimit)

				
				if self.end == 'end':
					print 'break is true: ', self.end
					break
					sys.exit(0)
					
		except (KeyboardInterrupt, SystemExit):
			print 'clsoing program thank you and have a good day'
			sys.exit()


############################################################################
if __name__ == '__main__':
	myfile = Main()
	myfile.run()
