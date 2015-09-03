#!/usr/bin/python

#linux_cmd_setup.py

import sys
import subprocess
import logging 
from loggingfile import Logging_File as Log_File

'''
THis script is designed to run all the linux commands we need to run our main script 
the commands we need is to set the combined parameter to yes
and to give super user access to the script 
though if we do an auto on the srcript we may not need to 

auto on log in is the most safest proecudre you log in first and then check it out
'''
Log_File('Linux_Commands.log') 

class Linux_Command():
    def __init__(self):
        '''This class is designed to use subprocess to run all the linux commands needed'''
        #find the slave addresst to all the sensors attached
        self.i2cdetect_command = 'sudo i2cdetect -y 1'
        
        #these two commands are needded to activate combined transactions
        self.chmod666_command = 'sudo chmod 666 /sys/module/i2c_bcm2708/parameters/combined'
        self.echo_command = 'sudo echo -n 1 > /sys/module/i2c_bcm2708/parameters/combined'
        
        #usb command activation deprecated functoion as usb can be run in auto mode too
        #TOD: may or may not be used and needed
        self.ls_command = 'sudo ls -l /dev/disk/by-uuid/'
        self.chown_command = 'sudo chown -R pi:pi usb'
        self.mount_command = 'sudo mount /dev/sda1 usb -o uid=pi,gid=pi'
        #possible values we will ignore when parsing the address string table
        self.possible_values = ['--', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f',
                        '00:', '10:', '20:', '30:', '40:', '50:', '60:', '70:']
        
        self.address_list = []
        self.useless_list = []
        
        self.logger = logging.getLogger('Linux_Commands.log')
        self.logger.info("************ROOT**************")
    
    
    def combined_transaction(self):
        '''Running the subprocess commands needed to activate the combined transaction'''
        subprocess.call(self.chmod666_command, shell = True)
        subprocess.call(self.echo_command, shell = True)
    
    def i2c_detect_cmd(self):
        '''this function sets the i2cdetect and parses the address to obtain the adress cal
        Note: 
        '''
        subprocess.call(self.i2cdetect_command, shell=True)
        ans = subprocess.check_call()
        parse_string =  ans.strip().split('\n')
        for item in parse_string:
            b=item.strip().split()
            for value in b:
                if value in self.possible_values:
                    self.address_list.append(value)
                else:
                    self.useless_list.append(value)
        print 'address list: ', self.address_list
        
        self.logger.debug('address string: ' + repr(ans) ) 
        self.logger.debug('address_list: ' + repr(self.address_list) )
        self.logger.debug('useless_list: ' + repr(self.useless_list) )
            
            
    def usb_setup(self):
        '''this function sets up the usb and allows the usb to be read
        TODo: it is possible to automate this componet in linux and hence this is 
        a deprecated and useless function
        '''
        subprocess.call(self.ls_command, shell=True)
        subprocess.call(self.chown_command, shell = True)
        subprocess.call(self.mount_command, shell=True)
        
    
    def run(self):
        '''this function will run the self commands using the subprocess call'''
        self.combined_transaction()
        self.usb_setup()
        self.i2c_detect_cmd()
        


    
class Main():
    def __init__(self):
        self.linux_setup = Linux_Command()
    
    def run(self):
        self.linux_setup.run()

#######################################################################
if __name__ == '__main__':
    myfile = Main()
    myfile.run()
    

        
        
        