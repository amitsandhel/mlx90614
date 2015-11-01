#!/usr/bin/python

#mlx90614.py


import unittest
import time
import logging 
import random

import sim.mlx90614_sim 
import mlx.control_variable

from Queue import Queue


logging.basicConfig(filename='mlx90614_test_logs.log', filemode='a', level=logging.DEBUG, format='%(asctime)s, %(levelname)s, %(message)s')
logging.info(" ---------------------- root --------------------------------")

class MLX90614_Test(unittest.TestCase):
    '''unittest class for testing and TDD'''
    
    def setUp(self):
        '''Function which setups the classes and the like
        '''
        #default address used
        address = 90
        self.m = sim.mlx90614_sim.MLX90614_IR_sensor(address)
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
        ans = ['__doc__', '__init__', '__module__', 'address', 'ambient_temp_analysis', 
        'control_class', 'counter','cycle', 'init_tamb_value', 'init_tobj_value', 
        'object_temp_analysis', 'read', 'record_data', 'run', 'tamb_jump_value','tamb_num', 'tamb_percent_limit_down',
        'tamb_percent_limit_up','tobj_jump_value','tobj_num', 'tobj_percent_limit_down', 'tobj_percent_limit_up']
        
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
        '''changing the control and jump value to a negative value
        something how to change the value of hte control in real time 
        '''
        self.m.control_class.control_setpoint(-1, -0.5)
        self.m.control_class.report_control()
        #self.m.control_class.run()
        
        self.assertEqual(0.01, self.m.control_class.limit_value)
        self.assertEqual(0.5, self.m.control_class.jump_value)
        self.assertEqual((0.01, 0.5), self.m.control_class.answer)
        
    
    
    
        
#####################################################################################    
if __name__ == '__main__':
    print('Welcome to my mlx90614_sim Unit-Testing Environment!\n')
#    os.environ['PYTHONINSPECT'] = "True"
    unittest.main()