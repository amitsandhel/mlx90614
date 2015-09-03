#!/usr/bin/python

#mlx90614.py


import unittest
import time
import logging 

import control_variable

import mlx90614_sim

#REFERENCES
#http://code.activestate.com/recipes/496969-convert-string-to-hex/


logging.basicConfig(filename='mlx90614_test_logs.log', filemode='a', level=logging.DEBUG, format='%(asctime)s, %(levelname)s, %(message)s')
logging.info(" ---------------------- root --------------------------------")


class Sensor_setupconfig_Test(unittest.TestCase):
    '''unittest class for testing and TDD'''
    
    def setUp(self):
        self.m = mlx90614_sim.MLX90614_IR_sensor()
        #self.debug = False
        
        self.text = '     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f\n00:          -- -- -- -- -- -- -- -- -- -- -- -- -- \n10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- \n20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- \n30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- \n40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- \n50: -- -- -- -- -- -- -- -- -- -- 5a -- -- -- -- -- \n60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- \n70: -- -- -- -- -- -- -- --                         \n'
        
        self.debug = True
        self.logger = logging.getLogger('mlx90614_test_logs')

    def diag_print(self, msg= '\n'):
        if self.debug:
            print (msg)
            
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
        
    
    def test04(self):
        '''this function is testing the concept of how to run several addresses of different IR 
        sensors
        first testing that the mlx90614_sim library is properly imported with all the libraries we need
        '''
        
        library = dir(self.m)
        ans = ['__doc__', '__init__', '__module__', 'ambient_temp_analysis', 'control_class',
        'init_tamb_value', 'init_tobj_value', 'logger1', 'logger2', 'logger3', 'logger4'
        , 'logger5', 'logger6', 'logger7', 'logger8', 'object_temp_analysis', 'read', 'run', 
        'tamb_num', 'tobj_num', 'tobj_percent_limit_down', 'tobj_percent_limit_up']
                    
        self.assertEqual(library, ans)
    
    def test05(self):
        '''Testing the case of having several sensor address and calling them into the mlx90614 sensor 
        Note we do not need to convert the address to string based on simple python terminal ideas 
        shown below
        '''
        #a='0x5a'
        #b=int(a, 16)
        #c=hex(b)
        #print a,b,c
        #print type(a), type(b), type(c)
        #print repr(a), repr(b), repr(c)
        
        
        address = [0x5a, 0x5b, 0x5c]
            
        
        print address
        
        #while(processmoresensor):
        #    self.m
            
        #self.m.run()
        #self.m.run()
        
        
        
            

        
        
        
        
        
        
        
        
#####################################################################################    
if __name__ == '__main__':
    print('Welcome to my Unit-Testing Environment!\n')
#    os.environ['PYTHONINSPECT'] = "True"
    unittest.main()