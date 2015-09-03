#!/usr/bin/python

#mlx90614.py


import unittest
import time
import logging 
import random

import mlx90614_sim
import control_variable

from Queue import Queue




logging.basicConfig(filename='control_variable_test.log', filemode='a', level=logging.DEBUG, format='%(asctime)s, %(levelname)s, %(message)s')
logging.info(" ---------------------- root --------------------------------")


class Control_Variable_Test(unittest.TestCase):
    '''unittest class for testing and TDD'''
    
    def setUp(self):
        self.m = control_variable.Control_Variable() 
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
        print directory
        print self.m
        ans = control_variable
        print dir(ans)
        '''
        ['__doc__', '__init__', '__module__', 'answer', 'control_setpoint', 'jump_value'
        , 'limit_value', 'logger', 'report_control', 'run']
        <control_variable.Control_Variable instance at 0x02A34D28>
        ['Control_Variable', 'Log_File', 'Main', '__builtins__', '__doc__', '__file__',
        '__name__', '__package__', 'division', 'logging']
        '''
        #self.logger.debug('ok')
        #determining the temperature range we should use whcih is 20 to 50 degrees
        #(20+273.15)/0.02 = 14657
        #(50+273.15)/0.02 = 16157
        #(0.5+273.15)/0.02 = 13682
    
    def test02(self):
        '''Testing the control_Variable() classt to change and report control variables as needed
        Here we are testing the default parameters
        '''
        myfile = control_variable.Control_Variable()
        ans=(0.01, 0.5)
        self.assertEqual(ans, (myfile.limit_value, myfile.jump_value) )
        self.assertEqual((), myfile.answer)
    
    def test03(self):
        '''testing that the control_Variable parameters can be changed once
        '''
        #the fun function is useless and static 
        myfile = control_variable.Control_Variable()
        #myfile.run()
        myfile.control_setpoint(20, 10)
        myfile.report_control()
        ans = (0.2, 10)
        self.assertEqual(ans, (myfile.limit_value, myfile.jump_value) )
        self.assertEqual(ans, myfile.answer)
        
        myfile.control_setpoint(200, 100)
        myfile.report_control()
        ans2=(2, 100)
        self.assertEqual(ans2, myfile.answer)
        
    
    def test04(self):
        '''testing the control_variable where we change the value via the main.run() function 
        this way we dont need to touch the control_variable() class 
        setting the parameter using main is too indirect and not useful better to directly access the class
        and alter the variables
        '''
        myfile = control_variable.Main()
        myfile.run()
        #print myfile
        #print 'ok1: ', myfile.myfile.limit_value
        #print 'ok2: ', myfile.myfile.jump_value
        self.assertEqual(0.01, myfile.myfile.limit_value)
        self.assertEqual(0.5, myfile.myfile.jump_value)
    
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
        myfile = control_variable.Control_Variable()
        myfile.control_setpoint('x', 'xxx')
        myfile.report_control()
        #asserting that the default values will be used
        self.assertEqual(0.01, myfile.limit_value)
        self.assertEqual(0.5, myfile.jump_value)
        self.assertEqual((0.01, 0.5), myfile.answer)
    
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
    
    def test08(self):
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
    print('Welcome to my Unit-Testing Environment!\n')
#    os.environ['PYTHONINSPECT'] = "True"
    unittest.main()