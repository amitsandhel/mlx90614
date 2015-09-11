#!/usr/bin/python

#mlx90614.py


import unittest
import time
import logging 
import random

import mlx90614_sim
import control_variable

from Queue import Queue


logging.basicConfig(filename='mlx90614_test_logs.log', filemode='a', level=logging.DEBUG, format='%(asctime)s, %(levelname)s, %(message)s')
logging.info(" ---------------------- root --------------------------------")

class MLX90614_Test(unittest.TestCase):
    '''unittest class for testing and TDD'''
    
    def setUp(self):
        address = 90
        self.m = mlx90614_sim.MLX90614_IR_sensor(address)
        #self.debug = False
        self.debug = True
        self.logger = logging.getLogger('mlx90614_test_logs')

    def diag_print(self, msg= '\n'):
        if self.debug:
            print (msg)
        
    def test01(self):
        '''testing to ensure the import library works and the library and variables have been imported
        '''
        library = dir(self.m)
        ans = ['__doc__', '__init__', '__module__', 'ambient_temp_analysis', 'control_class',
        'init_tamb_value', 'init_tobj_value', 'logger1', 'logger2', 'logger3', 'logger4'
        , 'logger5', 'logger6', 'logger7', 'logger8', 'object_temp_analysis', 'read', 'run', 
        'tamb_num', 'tobj_num', 'tobj_percent_limit_down', 'tobj_percent_limit_up']
                    
        self.assertEqual(library, ans)
    
        #print dir(self.m)
    
    def test02(self):
        '''testing the ambient function is doing what we want 
        we are not running the read function so all self variables should be zero as of now
        '''
        self.m.ambient_temp_analysis()

        self.m.object_temp_analysis()
        
        self.assertEqual(-273.15, self.m.tobj_num)
        self.assertEqual(-273.15, self.m.tamb_num)
        self.assertEqual(0, self.m.init_tobj_value)
        self.assertEqual(0, self.m.init_tamb_value)
    
    def test03(self):
        '''testing the case with the control case activated 
        In this case the assertequal values will stay the same but the jump values will bear no change to any 
        of the values 
        the jump and limit values are stored locally and transported locally to log files
        '''
        self.m.control_class.run()
        
        self.m.ambient_temp_analysis()
        self.m.object_temp_analysis()

        
        self.assertEqual(-273.15, self.m.tobj_num)
        self.assertEqual(-273.15, self.m.tamb_num)
        self.assertEqual(0, self.m.init_tobj_value)
        self.assertEqual(0, self.m.init_tamb_value)
        
        self.assertEqual(0.01, self.m.control_class.limit_value)
        self.assertEqual(0.5, self.m.control_class.jump_value)
        self.assertEqual((0.01,0.5), self.m.control_class.answer)
    
    def test04(self):
        '''testing the jump and limit value using the read() function 
        the function of the read() function is to read the IR sensor here it is mimicked 
        using a random number generator
        the result is that the self.tobj_num and self.tamb_num value calculated is truly the value
        we expected it to be
        '''
        self.m.control_class.run()
        
        self.m.read()
        self.m.ambient_temp_analysis()
        self.m.object_temp_analysis()
        
        ans = (self.m.init_tobj_value*0.02)-273.15
        ans2 = (self.m.init_tamb_value*0.02)-273.15
        
        self.assertEqual(ans, self.m.tobj_num)
        self.assertEqual(ans2, self.m.tamb_num)
        
        self.assertEqual(0.01, self.m.control_class.limit_value)
        self.assertEqual(0.5, self.m.control_class.jump_value)
        self.assertEqual((0.01,0.5), self.m.control_class.answer)
    
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
            print self.m.control_class.jump_value
            print 'jump: ',  jump_value, tobj_ans
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
            
    
    def test06(self):
        '''changing the control and jump value to a negative value
        something how to change the value of hte control in real time 
        '''
        self.m.control_class.control_setpoint(-1, -0.5)
        self.m.control_class.report_control()
        #self.m.control_class.run()
        
        self.assertEqual(0.01, self.m.control_class.limit_value)
        self.assertEqual(0.5, self.m.control_class.jump_value)
        self.assertEqual((0.01, 0.5), self.m.control_class.answer)
        
    
    def test07(self):
        ''' testing an exit flag idea here
        SPIKE/CONCEPT TEST
        '''
        
        def run():
            process = True
            while (process):
                print 'yes'
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
                
                print self.init_tobj_value
                #print self.init_tamb_value
                #self.object_temp_analysis()
            
            def object_temp_analysis(self):
                tobj_ans = (self.init_tobj_value*0.02 ) - 273.15
                jump_value = self.tobj_num - tobj_ans
                print 'tobjans: ', tobj_ans
                print 'jump: ',  jump_value
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
            print value
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
        
        '''
        #https://docs.python.org/2/howto/logging-cookbook.html#using-file-rotation
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
            print i 
            my_logger.debug('i = ' + repr(i) )

        # See what files are created
        #logfiles = glob.glob('%s*' % LOG_FILENAME)

        #for filename in logfiles:
        #    print(filename)
                            
                




        '''
        #for adr in addresslist:
        #    Sensor-list.append(Mlx90164(adr) )
        '''

        '''
        ProcessMoreSensors = True
        while (ProcessMoreSensors):
            sensors = GetAllSensors()
            UpdateAllSensorsClass(sensors)
            CalculateDataClass(sensors)
            UpdateStatistics(sensors)
            LogYourData(sensors)
            if SomeReasonToQuit():
              ProcessMoreSensors = False
        '''
        
        '''
        ProcessMoreSensors = True
        while (ProcessMoreSensors):
          sensors = GetAllSensors()
          UpdateAllSensorsClass(sensors)
          CalculateDataClass(sensors)
          UpdateStatistics(sensors)
          LogYourData(sensors)
          if SomeReasonToQuit():
            ProcessMoreSensors = False
        '''
        
        
#####################################################################################    
if __name__ == '__main__':
    print('Welcome to my Unit-Testing Environment!\n')
#    os.environ['PYTHONINSPECT'] = "True"
    unittest.main()