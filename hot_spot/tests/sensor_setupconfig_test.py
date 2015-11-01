#!/usr/bin/python
#sensor_setupconfig_test.py


import unittest
import time
import logging 

import mlx.control_variable

import sim.mlx90614_sim

#REFERENCES
#http://code.activestate.com/recipes/496969-convert-string-to-hex/


logging.basicConfig(filename='mlx90614_test_logs.log', filemode='a', level=logging.DEBUG, format='%(asctime)s, %(levelname)s, %(message)s')
logging.info(" ---------------------- root --------------------------------")


class Sensor_setupconfig_Test(unittest.TestCase):
    '''unittest class for testing and TDD'''
    
    def setUp(self):
        self.m = sim.mlx90614_sim.MLX90614_IR_sensor(address=90)
        #self.debug = False
        
        self.text = '     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f\n00:          -- -- -- -- -- -- -- -- -- -- -- -- -- \n10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- \n20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- \n30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- \n40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- \n50: -- -- -- -- -- -- -- -- -- -- 5a -- -- -- -- -- \n60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- \n70: -- -- -- -- -- -- -- --                         \n'
        
        self.debug = True
        self.logger = logging.getLogger('mlx90614_test_logs')

    def diag_print(self, msg= '\n'):
        if self.debug:
            print (msg)
    
    def test01(self):
        '''this function is testing the concept of how to run several addresses of different IR 
        sensors
        first testing that the mlx90614_sim library is properly imported with all the libraries we need
        '''
        #testing to ensure the class is properly imported tested here need to move to test01 and renumber
        #this is the mlx_sim class
        library = dir(self.m)
        mlx_dir = dir(sim.mlx90614_sim)
        control_dir = dir(mlx.control_variable)
        #print library 
        #print mlx_dir
        #print control_dir
        
        ans = ['__doc__', '__init__', '__module__', 'address', 'ambient_temp_analysis', 'control_class', 'cycle', 
        'init_tamb_value', 'init_tobj_value', 'jump_value', 'logger1', 'object_temp_analysis', 'read', 
        'record_data', 'run', 'tamb_num', 'tobj_num', 'tobj_percent_limit_down', 'tobj_percent_limit_up']
        
        control_ans = ['Control_Variable', 'Log_File', 'Main', '__builtins__', '__doc__', '__file__',
        '__name__', '__package__', 'division', 'logging']
        
        self.assertEqual(library, ans)
        self.assertEqual(control_dir, control_ans)
        
    def test02(self):
        '''Testing the case of having several sensor address and calling them into the mlx90614 sensor 
        From the linux terminal we obtain a string table which gives us the sensor address however a "0x" needs
        to be joined to the string and then converted to a 16 bit integer value which is then passed into the class
        This procedure was resolved using the linux terminal and a raspberry pi 
        NOTE This is a SPIKE/CONCEPT TEST
        '''
        

        address= ['5a', '5b']
        intern_add = []
        address2 = []
        for item in address:
            ans = '0x' + item
            #ensure that the 0x has been added
            intern_add.append(ans)
            value = int(ans, 16) 
            address2.append(value)
        
        self.assertEqual(intern_add, ['0x5a', '0x5b'] )
        self.assertEqual(address2, [90, 91])

        
        
        
        
        
        
        
        
        
#####################################################################################    
if __name__ == '__main__':
    print('Welcome to my Sensor_Setupconfig Unit-Testing Environment!\n')
#    os.environ['PYTHONINSPECT'] = "True"
    unittest.main()