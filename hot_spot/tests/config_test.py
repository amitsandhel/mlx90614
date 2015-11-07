#!/usr/bin/python

#configtest.py


import unittest
import time
import logging 


import mlx.control_variable



logging.basicConfig(filename='config.log', filemode='a', level=logging.DEBUG, format='%(asctime)s, %(levelname)s, %(message)s')
logging.info(" ---------------------- root --------------------------------")

class Control_Variable_Test(unittest.TestCase):
    '''unittest class for testing and TDD'''
    
    def setUp(self):
        self.m = mlx.control_variable.Control_Variable() 
        self.n = sim.mlx90614_sim.Main()
        #self.debug = False
        self.debug = True
        self.logger = logging.getLogger('mlx90614_test_logs')

    def diag_print(self, msg= '\n'):
        if self.debug:
            print (msg)
    
    def test01(self):
        print 'testing'
    


    
#####################################################################################    
if __name__ == '__main__':
    print('Welcome to my Config Unit Testing Environment!\n')
#    os.environ['PYTHONINSPECT'] = "True"
    #suite = unittest.TestLoader().loadTestsFromTestCase(Control_Variable_Test)
    #unittest.TextTestRunner(verbosity=3).run(suite)
    unittest.main()