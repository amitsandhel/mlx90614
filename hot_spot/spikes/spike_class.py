#!/bin/bash

''' This scipt are the spike tests we developed
This script contains Rought Work and algorithms developed to run the software
'''

#http://www.tutorialspoint.com/python/python_dictionary.htm

#from future import division has to be done atthe top of the value
from __future__ import division
import sys
import os
import time
import random
import logging
import logging.handlers
#import main
#from main import setup_parser as sp
from mlx.control_variable import Control_Variable as control_variable
from mlx.linux_cmd_setup import Linux_Command as linux_command

class Spike_Class(self):
    '''This class contains spike/concept classes we developed for the software 
    Note it is simply rough work but will help future users understand though process of how system was 
    developed
    NOte that Rough work is also included in Here
    '''
    def test01(self):
        '''testing the ability to parse the i2cdetect line to find new addresses
        Note need to use the subprocess.check_call() method to see the data you will get/receive        
        '''
        #for item in self.text:
        a = self.text.strip().split('\n')
        #print b
        #print len(b)
        #print type(b)
        list1=[]
        list2=[]
        possible = ['--', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f',
                        '00:', '10:', '20:', '30:', '40:', '50:', '60:', '70:']
        for item in a:
            #print 'item: ', repr(item)
            #print type(item)
            #print '%%%%'
            #print item
            b=item.strip().split()
            #print b
            #print len(b)
            #print type(b)
            
            #print repr(b)
            for value in b:
                if value in possible:
                    list1.append(value)
                else:
                    list2.append(value)
                    
        #print '%%%%%%%%%%5'
        #print 'list1: ', list1
        #print '&&&&&&&&&&&&7'
        #print 'list2: ', list2
        #print '$$$$$$$$$$$$$$$$$'
        #print repr(self.text)
    
    def test02(self):
        '''this function is turning test01 into a function so it makes and work robustly and properly
        '''
        def parse_address():
            global list2
            address_str = self.text.strip().split('\n')
            list1=[]
            list2=[]

            #possible list combinations that need to be removed
            possible = ['--', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f',
                            '00:', '10:', '20:', '30:', '40:', '50:', '60:', '70:']
            for item in address_str:
                address=item.strip().split()
                
                for value in address:
                    if value in possible:
                        list1.append(value)
                    else:
                        list2.append(value)
            return list2
        
        parse_address()
        self.assertEqual('5a', list2[0])
        #print '%%%%%%%%%%5'
        #print 'list1: ', list1
        #print '&&&&&&&&&&&&7'
        #print 'list2: ', list2
        #print '$$$$$$$$$$$$$$$$$'
        #print repr(self.text)
    
    def test03(self):
        '''this function is designed to take the addresses for the sensors and do stuff with it 
        '''
        def parse_address():
            global list2
            address_str = self.text.strip().split('\n')
            list1=[]
            list2=[]

            #possible list combinations that need to be removed
            possible = ['--', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f',
                            '00:', '10:', '20:', '30:', '40:', '50:', '60:', '70:']
            for item in address_str:
                address=item.strip().split()
                
                for value in address:
                    if value in possible:
                        list1.append(value)
                    else:
                        list2.append(value)
            add_hex(list2)
            #return list2
            
        def add_hex(list):
            global list3
            global list4
            list3=[]
            list4=[]
            for item in list:
                new_val = '0x'+ str(item)
                intval = int(new_val, 16)
                hexval=hex(intval)
                list3.append(new_val)
                list4.append(hexval)
                #print 'list3: ', list3
            
        parse_address()
        self.assertEqual('5a', list2[0])
        self.assertEqual('0x5a', list3[0] )
        self.assertEqual('0x5a', list4[0] )
    
    def test05(self):
        '''physcially testing our tobj if loop to ensure that the if loop does truly work
        and the parameters due change based on the jump value and limit value
        Note no self.assert tests done here 
        SPIKE/CONCEPT TEST
        '''
        #TODO: Remove the elif statement a simple IF ELSE is REQUIRED ONLY
        
        self.m.control_class.run()
        
        self.m.read()
        
        def object_temp_analysis():
            tobj_ans = ( self.m.init_tobj_value*0.02 ) - 273.15
            jump_value = self.m.tobj_num - tobj_ans
            #print 'jump: ',  jump_value
            if jump_value >= self.m.control_class.jump_value: #0.5:
                self.m.tobj_num = tobj_ans
                #calculate percent limit 
                tobj_percent_limit_up = self.m.tobj_num*self.m.control_class.limit_value
            else: # elif jump_value <= self.m.control_class.jump_value: #(-0.5):
                #reinitalize variab
                self.m.tobj_num = tobj_ans
                #calculating percent limit
                tobj_percent_limit_down = self.m.tobj_num*self.m.control_class.limit_value
            #print 'obt: ', self.m.tobj_num
            #else:
            #    print 'no change'
        
        def object_temp_analysis_v2():
            #tobj_ans = ( self.m.init_tobj_value*0.02 ) - 273.15
            tobj_ans = random.uniform(25,26)
            jump_value = self.m.tobj_num - tobj_ans
            #print self.m.control_class.jump_value
            #print 'jump: ',  jump_value, tobj_ans
            if jump_value >= self.m.control_class.jump_value: #0.5:
                self.m.tobj_num = tobj_ans
                #calculate percent limit 
                tobj_percent_limit_up = self.m.tobj_num*self.m.control_class.limit_value
            elif jump_value < self.m.control_class.jump_value: #(-0.5):
                #reinitalize variab
                self.m.tobj_num = tobj_ans
                #calculating percent limit
                tobj_percent_limit_down = self.m.tobj_num*self.m.control_class.limit_value
            #print 'obt: ', self.m.tobj_num
            else:
                print 'no change'
            
        for x in range(10):
            #mimicking a while loop generating a random number
            #each iteration
            self.m.read()
            object_temp_analysis()
        
        for x in range(10):
            self.m.read()
            object_temp_analysis_v2()
            
    def test07(self):
        ''' testing an exit flag idea here
        SPIKE/CONCEPT TEST
        '''
        
        def run():
            process = True
            while (process):
                #print 'yes'
                if some_quit():
                    process=False
                break
            
        def some_quit():
            print 'yes exit while loop'
            
        #run()
    def test08(self):
        '''testing with several sensors 
        here we are using 4 ir sensors connected
        '''
        address = [0x5a, 0x5b, 0x5c]
        
        class Read_Stuff():
            def __init__(self, adds):
                self.address = adds
                self.init_tobj_value = 0
                self.init_tamb_value = 0
                self.tobj_num = 0
                
                self.tobj_percent_limit_up=0.0
                self.tobj_percent_limit_down=0.0
                
            def read(sellf):
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
                
                #print self.init_tobj_value
                #print self.init_tamb_value
                #self.object_temp_analysis()
            
            def object_temp_analysis(self):
                tobj_ans = (self.init_tobj_value*0.02 ) - 273.15
                jump_value = self.tobj_num - tobj_ans
                #print 'tobjans: ', tobj_ans
                #print 'jump: ',  jump_value
                if jump_value >= 0.5:
                    self.tobj_num = tobj_ans
                    #calculate percent limit 
                    self.tobj_percent_limit_up = self.tobj_num*0.01
                elif jump_value < 0.5: 
                    #reinitalize variab
                    self.tobj_num = tobj_ans
                    #calculating percent limit
                    self.tobj_percent_limit_down = self.tobj_num*0.01
                else:
                    #print 'no change'
                    self.tobj_num = tobj_ans
                #print (self.tobj_num, tobj_ans, jump_value, self.tobj_percent_limit_up, self.tobj_percent_limit_down)
            
            def run(self):
                #print self.address
                #for item in self.address:
                #    addr=item
                #    print 'addr: ', addr
                #    if item == addr:
                for x in range(5):
                    #self.__init__(90)
                    self.read()
                    self.object_temp_analysis()
                    
                    
        #each one needs to iterate each function on its own therefore at least
        sensor_list=[]
        #print address
        for adr in address:
            sensor_list.append(Read_Stuff(adr) ) #adr))
            #ans = Read_Stuff(address)
            #ans.run()
        #sensor_list[0].run()
            
        #print sensor_list
        #print type(sensor_list)
        #print sensor_list[0]
        #print repr(sensor_list[0])
        
        self.assertEqual(90, sensor_list[0].address)
        self.assertEqual(91, sensor_list[1].address)
        self.assertEqual(92, sensor_list[2].address)

        

        
    def test09(self):
        '''testing the case of a more refined random number generator 
        NOTE THIS IS A SPIKE/CONCEPT TEST
        '''
        for x in range(12):
            value = random.uniform(25, 26)
            #print value
            if x ==10:
                value = random.random()
                #print value
            if x == 11:
                value = random.randrange(30,35)
                #print value
        
        def cycle_counter():
            value = random.uniform(25, 26)
            #print value
        def cycle_count_down():
            value = random.random()
            #print value
        def cycle_count_up():
            value = random.randrange(30,35)
            #print value
                
        
        def Main():
            cycle=0
            for x in range(36):
                cycle+=1
                #print 'cycle: ',  cycle
                cycle_counter()
                if cycle == 10:
                    cycle_count_down()
                elif cycle == 11:
                    cycle_count_up()
                    cycle=0
                    
        Main()

    def test10(self):
        '''the objective of this test is to test the size of the logger file
        NOTE: This is a spike/ Concept Test to determine and make sure we can use a simplier log file
        NOte that the maxBytes is the number of Bytes size and the backup count is the number of files we have as backup
        once all of them are finished it rotates throug the log files and deletes the old logs
        The log files are designed to be used for debugging purposes only there is no important data that is supposed to go there
        only for debugging purposes 
        '''
        '''NOTE: Thats correct.  The rotating log handles lets you keep the last "x" bytes Times "#" of files of log data. 
        And handles aging out your old data - renaming the log files.
        '''
        """NOTE: size of file should be about 10kB and no more then 4 maybe one"""
        """
        NOTE: THERE IS AN ISSUE OF USING ROTATING FILE IN WINDOWS IN WINDOWS BECAUE OF THE OS IT WILL ONLY 
        ROTATE THE FILES FROM WITHIN THE SAME SCRIPT IF SEVERAL SCRIPTS ARE WRITTING TO THE SAME LOGGER
        THIS WILL CRASH WITH A WINDOWS 32 ERROR 
        """
        
        #https://docs.python.org/2/howto/logging-cookbook.html#using-file-rotation
        #https://docs.python.org/2/howto/logging-cookbook.html#using-file-rotation
        #https://docs.python.org/2/howto/logging.html#logging-from-multiple-modules
        #https://docs.python.org/2/howto/logging-cookbook.html#logging-to-multiple-destinations
        #https://pypi.python.org/pypi/ConcurrentLogHandler/0.9.1#downloads
        import glob
        import logging.handlers
        
        LOG_FILENAME = 'logging_rotatingfile_example.out'

        # Set up a specific logger with our desired output level
        my_logger = logging.getLogger('MyLogger')
        my_logger.setLevel(logging.DEBUG)

        # Add the log message handler to the logger
        handler = logging.handlers.RotatingFileHandler(
                      #maxBytes = Byte size right now at 150 Bytes and backup count is # of files to create 
                      #LOG_FILENAME, mode='a',  maxBytes=75, backupCount=4)
                      LOG_FILENAME, mode='a',  maxBytes=150, backupCount=4)

        my_logger.addHandler(handler)
        
        # Log some messages
        for i in range(50):
            #print i 
            my_logger.debug('i = ' + repr(i) )

        # See what files are created
        #logfiles = glob.glob('%s*' % LOG_FILENAME)

        #for filename in logfiles:
        #    print(filename)
    
    def test11(self):
        """This function is designed to refine the number generator instead of being too random it will be more controlled
        the current random generator is too eratic and causing problems
        hmm a sine wave could be interesting 
        """
        '''
        #x=random.randrange(26,30,1)
        a = random.randrange(10, 25) 
        for item in range(25):
            x=random.randrange(14951, 14970)
            ans = (x*0.02)-273
            #print init_tobj_value
            print ans
            if item >= 13 and item <= 16:
                print 'x'
                y=random.randrange(15100,15300)
                ans = (y*0.02)-273
                print ans
        '''
        '''
        for item in range(50):
            #x = random.randrange(14950, 15250)
            #self.m.init_tobj_value = random.randrange(14657, x, 1) 
            #self.m.read()
            #self.m.object_temp_analysis()
            #self.m.ambient_temp_analysis()
            self.m.control_class.run(2, 2)
            self.m.run()
        '''
        pass
    
    def test12(self):
        '''This function is designed to add in a timer in the while loop to prevent data being extracted every time we 
        are not doing a system performance
        the default time is 5 minutes but for testing purposes we will use 5 seconds
        NOTE: This is a SPIKE/CONCEPT Test
        '''
        '''
        #https://docs.python.org/2/library/time.html
        NOTE: time.clock() returns the CPU current processor time as a flioating point number in terms is the processor time 
        used for benchmarking python or timing algorithms 
        resolution is typically better then one microsecond (1 us)
        time.time() has resolution of only 1 second (1 s) and is less accurat then time.clock()
        time.sleep( is in seconds) 
        '''
        #rough work
        #timerx = time.clock()
        #time.sleep(5)
        #for x in range(5):
            #time.sleep(5)
        #    b=time.clock() - timerx
        #print b
        
        def run():
            #here we are using a time,sleep() to mimick 2 seconds
            #however by using a time.sleep we can't do anything else
            timerx = time.clock()
            for x in range(50):
                timerx = time.clock()
                self.m.read()
                self.m.object_temp_analysis()
                self.m.ambient_temp_analysis()
                print x
                print timerx
                print 'Address: %s -- tobject: %s -- tambient: %s'%(self.m.address, self.m.tobj_num, self.m.tamb_num)
                time.sleep(2)
            
        def run2():
            #here we are using a timer.clock to clock to 2 seconds and "relabel"
            #this way thigns can be done within the timer
            
            try:
                cycle=0
                timerx = time.clock()
                while True: #for x in range(100):
                    #time.sleep(0.5)
                    cycle+=1
                    timery = time.clock()
                    ans = timery - timerx
                    #print timery
                    #print timerx
                    if ans >= 2.0:
                        #print 'cycle: ', x
                        self.m.read()
                        self.m.object_temp_analysis()
                        self.m.ambient_temp_analysis()
                        print ans
                        print 'Address: %s -- tobject: %s -- tambient: %s'%(self.m.address, self.m.tobj_num, self.m.tamb_num)
                        timerx = time.clock()
                    if cycle == 20:
                        break
            except (KeyboardInterrupt, SystemExit):
                print 'closing software'
                
        #run()
        run2()
    
    def test07(self):
        '''testing the concept of using queues to change the parameter at any given time 
        this is a SPIKE test a concept driven test scenario
        '''
        #https://pymotw.com/2/Queue/
        #http://www.troyfawkes.com/learn-python-multithreading-queues-basics/

        q = Queue(maxsize=0)
        ans=(1, 2)
        q.put(ans)
        
        def ok(x,y):
            #this function is simply outputting the queue values after there
            #passed in here 
            a=x
            b=y
            #print 'ok a: ',  a
            #print 'ok b: ', b
            
        def run():
            #using a for looop to mimick a while loop 
            #using queues to pass in the values
            for x in range(6):
                ans=random.random()
                ans1=random.random()
                value=(ans, ans1)
                #print x
                #print value
                #print 'xxx'
                while not q.empty():
                    a = q.get()
                    #print type(a)
                    #print repr(a)
                    q.task_done()
                    ok(a[0], a[1])
                   #q.join()
                q.put(value)
                
        run()
    
    def testx(self):
        '''This function has important functions/discussions or concepts we put in here simply for reference
        this function is not tested or anything simply important skype discussions are placed here
        '''
        
        """
        processs overview: at 4 pm take measurement thaen at 4:05 pm taken another measurement
        between 4:01pm to 4:04 pm twiddle your software thumbs do nothing 
        put into list and a timestamp into another list 
        use clear or reset functions() to empty those lists

        #for adr in addresslist:
        #    Sensor-list.append(Mlx90164(adr) )
   
   
        ProcessMoreSensors = True
        while (ProcessMoreSensors):
            sensors = GetAllSensors()
            UpdateAllSensorsClass(sensors)
            CalculateDataClass(sensors)
            UpdateStatistics(sensors)
            LogYourData(sensors)
            if SomeReasonToQuit():
              ProcessMoreSensors = False
  
        ProcessMoreSensors = True
        while (ProcessMoreSensors):
          sensors = GetAllSensors()
          UpdateAllSensorsClass(sensors)
          CalculateDataClass(sensors)
          UpdateStatistics(sensors)
          LogYourData(sensors)
          if SomeReasonToQuit():
            ProcessMoreSensors = False

        Yes and it's easy, you just need one entry point - 
        main. That configures the log.  
        Then any class it instantiates can simply use get logger
        to get a child handle to the main log file.
 
        NOte: rotate handler is finicky on windows
        """
        
        pass


class Main():
	def __init__(self):
		self.sensorfile = linux_command()
		self.class_list = []
	
	def function_setup(self):
		for item in self.sensorfile.simulator_list:
			IR_class = MLX90614_IR_sensor(item)
			IR_class.control_class.run(2, 2)
			self.class_list.append(IR_class)
					
	def run(self):
		myfile = open(FILENAME, "a")
		myfile.write("Time,Cycle, address, Tobject, Tambient, jumpvalue" + NEWLINE)
		myfile.close()
		
		self.function_setup()
		
		try:
			timerx = time.clock()
			while True:
				timery = time.clock()
				ans = timery - timerx
				if ans >= 3.0:
					for item in self.class_list:
						item.run()
					timerx = time.clock()
		except (KeyboardInterrupt, SystemExit):
			print 'clsoing program thank you and have a good day'
			sys.exit()


############################################################################
if __name__ == '__main__':
	myfile = Main()
	myfile.run()
    