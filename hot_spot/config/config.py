#!/usr/bin/python
#config.py

import ConfigParser
from ConfigParser import SafeConfigParser
import os
import sys

"""This script is designed contains a "Config" class that main can import.
Takes care of everything Configparser related and also able to return
the final dict of all info. And maybe functions for looking up single values.
"""

#REFERENCES
#https://pymotw.com/2/ConfigParser/
#https://docs.python.org/2/library/configparser.html
#http://www.blog.pythonlibrary.org/2013/10/25/python-101-an-intro-to-configparser/

class Config():
    """Class that will take care of configparser write and read 
    """
    def __init__(self):
        """initalizing the dict class"""
        #set up configparser
        self.config = ConfigParser.ConfigParser()
        
        self.parser = SafeConfigParser()
        
        self.path = 'settings.ini'
        
        #empty dict value
        self.config_dict = {}
        
        #run teh function in the init() function all the imported classes will have access to 
        #updated values of dict is now possible and will be done        
        self.run()
        
    def writeconfig(self):
        '''write and create the config .ini file if its deleted or if its the 
        first run
        '''
        #opens up a header 
        self.config.add_section("Temperature")
        #adds in the parameter
        #self.config.set(header, subheader, default value)
        self.config.set("Temperature", "jump_value", 1.0)
        self.config.set("Temperature", "limit_value", 1.0)
        
        #sim parameter 
        self.config.add_section("Sim")
        #set parameter to true
        self.config.set('Sim', 'sim', True)
        
        #gui parameter 
        self.config.add_section("Gui")
        #set parameter t false 
        self.config.set('Gui', 'gui', False)
        
        #file size parameter
        self.config.add_section("Size")
        self.config.set('Size', 'length', 20)
        self.config.set('Size', 'slice', 10)
        
        #timer component
        self.config.add_section('Time')
        self.config.set('Time', 'time', 300)
        
        #writing the value to the .ini value
        with open(self.path, "wb") as config_file:
            self.config.write(config_file)
    
    def readconfig(self):
        '''read the config .ini file '''
        self.parser.read('settings.ini')
        
        #print 'reading values'
        #extract jump value
        jump_value = self.parser.get('Temperature', 'jump_value')
        #extract limit value
        limit_value = self.parser.get('Temperature', 'limit_value')
        #extract sim value
        sim_value = self.parser.get('Sim', 'sim')
        #extract gui value
        gui_value = self.parser.get('Gui', 'gui')
        #extract size value
        length_value = self.parser.get('Size', 'length')
        #extract slice value 
        slice_value = self.parser.get('Size', 'slice')
        #timer value
        time_value = self.parser.get('Time', 'time')
        
        #append/combine the values into a dict so it can be passed around to all the lists
        self.dict={'jump_value': jump_value, 'limit_value': limit_value, 'sim':sim_value, 'gui':gui_value, 'length': length_value,
                        'slice':slice_value, 'time': time_value}
    
    def run(self):
        """Run function to run everything
        """
        if not os.path.exists(self.path):
            #if the file does not exist then rewrite it
            self.writeconfig()
        else:
            try:
                #testing to see if we can read the config file
                #read the config parser
                self.readconfig()
            except(ConfigParser.NoSectionError):
                #if we have added new headings then rewrite the settings file
                self.writeconfig()
                #reread the file
                self.readconfig()

class Main():
    """Main class to run and execute everything
    """
    def __init__(self):
        self.myfile = Config()
    def run(self):
        '''Run the class'''
        self.myfile.run()
        

       
#######################################################################
if __name__ == '__main__':
    myfile = Main()
    myfile.run()
