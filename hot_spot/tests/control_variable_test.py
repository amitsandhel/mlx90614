#!/usr/bin/python

#control_variable_test.py


import unittest
import time
import logging 
import random

from Queue import Queue

import sim.mlx90614_sim
import mlx.control_variable



logging.basicConfig(filename='control_variable_test.log', filemode='a', level=logging.DEBUG, format='%(asctime)s, %(levelname)s, %(message)s')
logging.info(" ---------------------- root --------------------------------")


class Control_Variable_Test(unittest.TestCase):
    '''unittest class for testing and TDD'''
    
    def setUp(self):
        self.m = mlx.control_variable.Control_Variable() 
        #self.debug = False
        self.debug = True
        self.logger = logging.getLogger('mlx90614_test_logs')

    def diag_print(self, msg= '\n'):
        if self.debug:
            print (msg)
            
    def test01(self):
        #testing log output works
        #print 'ok'
        directory=dir(self.m)
        #print directory
        #print self.m
        ans = dir(mlx.control_variable)
        #print dir(ans)
        
        #print directory list
        ['__doc__', '__init__', '__module__', 'answer', 'control_setpoint', 'jump_value'
            , 'limit_value', 'logger', 'report_control', 'run']
        ['Control_Variable', 'Log_File', 'Main', '__builtins__', '__doc__', '__file__',
        '__name__', '__package__', 'division', 'logging']
        #self.logger.debug('ok')
        #determining the temperature range we should use whcih is 20 to 50 degrees
        #(20+273.15)/0.02 = 14657
        #(50+273.15)/0.02 = 16157
        #(0.5+273.15)/0.02 = 13682
    
    def test02(self):
        '''Testing the control_Variable() classt to change and report control variables as needed
        Here we are testing the default parameters
        '''
        ans=(0.01, 0.5)
        self.assertEqual(ans, (self.m.limit_value, self.m.jump_value) )
        self.assertEqual((), self.m.answer)
    
    def test03(self):
        '''testing that the control_Variable parameters can be changed once
        '''
        #the fun function is useless and static 
        #myfile = control_variable.Control_Variable()
        #myfile.run()
        self.m.control_setpoint(20, 10)
        self.m.report_control()
        ans = (0.2, 10)
        self.assertEqual(ans, (self.m.limit_value, self.m.jump_value) )
        self.assertEqual(ans, self.m.answer)
        
        self.m.control_setpoint(200, 100)
        self.m.report_control()
        ans2=(2, 100)
        self.assertEqual(ans2, self.m.answer)
        
    
    def test04(self):
        '''testing the control_variable where we change the value via the main.run() function 
        this way we dont need to touch the control_variable() class 
        setting the parameter using main is too indirect and not useful better to directly access the class
        and alter the variables
        '''
        self.m.run()
        #print myfile
        #print 'ok1: ', myfile.myfile.limit_value
        #print 'ok2: ', myfile.myfile.jump_value
        self.assertEqual(0.01, self.m.limit_value)
        self.assertEqual(0.5, self.m.jump_value)
    
    def test05(self):
        '''testing hte case where the control varaible parameters are not float and integer values
        user purposefully adds in a string character
        '''
        def control_setpoint(limit, jump):
            global ans
            try:
                limit_value = limit /100
                jump_value = jump
            except TypeError:
                limit_value = 0.01
                jump_value = 0.5
            #print limit_value
            #print jump_value
            ans = (limit_value, jump_value)
        
        control_setpoint('xxx', 'xx')
        self.assertEqual((0.01, 0.5), ans)
    
    def test06(self):
        '''testing the case that incorrect parameters are passed to the control_variable() class script 
        will it go to default values
        Tests passed 
        '''
        
        self.m.control_setpoint('x', 'xxx')
        self.m.report_control()
        #asserting that the default values will be used
        self.assertEqual(0.01, self.m.limit_value)
        self.assertEqual(0.5, self.m.jump_value)
        self.assertEqual((0.01, 0.5), self.m.answer)
    
    
    def test07(self):
        '''changing the control and jump value to a negative value
        something how to change the value of hte control in real time 
        Note to fix the problem using an abs() function to make sure the value is indeed positive
        '''
        
        self.m.control_setpoint(-1, -0.5)
        self.m.report_control()
        
        self.assertEqual(0.01, self.m.limit_value)
        self.assertEqual(0.5, self.m.jump_value)
        self.assertEqual((0.01, 0.5), self.m.answer)
        
        self.m.run(2.0, 2)
        self.assertEqual(0.02, self.m.limit_value)
        self.assertEqual(2, self.m.jump_value)
        self.assertEqual((0.02, 2), self.m.answer)

    
#####################################################################################    
if __name__ == '__main__':
    print('Welcome to my Control_variable Unit Testing Environment!\n')
#    os.environ['PYTHONINSPECT'] = "True"
    #suite = unittest.TestLoader().loadTestsFromTestCase(Control_Variable_Test)
    #unittest.TextTestRunner(verbosity=3).run(suite)
    unittest.main()