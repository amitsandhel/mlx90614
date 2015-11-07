#!/usr/bin/env python

'''
Copyright Amit Sandhel

wxmain.py

This script is the GUI
'''
#references
#http://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.transpose.html
#http://matplotlib.org/users/pyplot_tutorial.html
#http://newville.github.io/wxmplot/plotpanel.html
#https://www.daniweb.com/programming/software-development/code/216913/using-wxpython-for-plotting
#http://zetcode.com/wxpython/widgets/#slider


#importing all files
import sys
import time
import wx #, gettext
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
import pylab
import numpy as np
import time
import logging
import sim.mlx90614_sim
#try:
    #import the real dude
   # import mlx.mlx90614
#except ImportError:
 #   print 'no smbus library'

import wxgui 
#import config file
import config.config



logging.basicConfig(filename='wxlog.log', filemode='a', level=logging.DEBUG, format='%(asctime)s, %(levelname)s, %(message)s')
logging.info(" ---------------------- root --------------------------------")
mylog10 = logging.getLogger('wxlog.log')


        
class MyFrame(wxgui.MyFrame):
    '''This is the main MyFrame GUI that sets up everything 
    '''
    def __init__(self, *args, **kwds):
        '''initalize all the variables needed'''
        super(MyFrame, self).__init__(*args, **kwds)
        
        self.tamb_list=[]
        self.tobj_list=[]
        self.tobj_list = []
        self.tobj_array=[]
        
        #the list to iterate over the line colors for multiple sensors
        self.color= ['green','red', 'yellow', 'orange', 'magenta', 'blue']
        
        #getting the simvalue 
        self.sim_checkbox.SetValue(True)
        self.simvalue = self.sim_checkbox.GetValue()
        
        if self.simvalue == True:
            #file is the simulator
            self.myfile = sim.mlx90614_sim.Main()
        else: 
            import mlx.mlx90614
            self.myfile = mlx.mlx90614.Main()
        

        # loop in run function Timer class event
        #activating redraw timer to draw the graph
        self.redraw_timer = wx.Timer(self)
        
        #initalizng the graph variables
        self.init_graph()
        
        #add events
        self.attach_events()
        
        #temperature slider value
        #jump slider value
        self.val=1
        self.val2=1
        
        #opening the config file 
        self.config = config.config.Config()
        #reading the config file
        #self.config.readconfig() 
        
    def attach_events(self):
        '''This function attaches events to the buttons
        '''
        #This one is the cheeckbox
        self.Bind(wx.EVT_CHECKBOX, self.On_Sim, self.sim_checkbox)
        #start button
        self.Bind(wx.EVT_BUTTON, self.On_Start, self.start_button)
        #close button
        self.Bind(wx.EVT_BUTTON, self.On_Close, self.close_button)
        #event timer
        self.Bind(wx.EVT_TIMER, self.redo, self.redraw_timer) 
        
        #event for temp slider
        self.Bind(wx.EVT_SCROLL, self.On_TempSliderScroll, self.temp_slider)
        #event for jump slider
        self.Bind(wx.EVT_SCROLL, self.On_JumpSliderScroll, self.jump_slider)
    
    def sim_analysis(self):
        """This function is designed to analysis the 
        sim function to see if its true or false
        """
        if self.simvalue == True:
            #clearing the text ctrl widget 
            self.address_text_ctrl_1.Clear()
            
            #set and find the address
            self.address = self.myfile.sensorfile.simulator_list
            
            #write the address list into the address textctrl box
            self.address_text_ctrl_1.AppendText(str(self.address) + "\n")
            
        if self.simvalue == False:
            #clearing the text ctrl widget 
            self.address_text_ctrl_1.Clear()
            
            #set and find address 
            self.address = self.myfile.sensorfile.final_address_list
            
            #write the address list into the address textctrl box
            self.address_text_ctrl_1.AppendText(str(self.address) + "\n")
        
        '''NOTE: if you don't use self.dameon = True then even if the gui shuts down the script 
        will still go crazy and be running without your control
        running the dameon
        self.myfile.daemon = True
        '''
        #set dameon = True to run the threads
        self.myfile.daemon = True
        

    def On_TempSliderScroll(self, event):
        """temp slider for temp limit """
        result = event.GetEventObject()
        val = result.GetValue()
        self.val = val
        #print self.val
        self.myfile.templimit = val
        #print val
        
        
    def On_JumpSliderScroll(self, event):
        """Jump limit slider """
        result = event.GetEventObject()
        val = result.GetValue()
        self.val2 = val
        self.myfile.jumplimit = val
        self.myfile.q.put(('jump',val))
       # print self.val2
    
    def redo(self, event):
        """This function loops the OnStart event button until new parameters 
        are not added when the pause button is clicked
        """
        starttimer = float(self.config.dict['time'])*1000
        self.redraw_timer.Start(starttimer) #3000) #3 second interval for event loop
        #self.data_collect(event)
        self.redraw_graph(event)
    
    def init_graph(self):
        '''initalizing the graph setup inside the panel
        '''
        self.fig = Figure(figsize=(8, 6), dpi=40)
        self.fig2 = Figure(figsize=(8, 6), dpi=40)
        
        # setting the axes fo the figure graph
        self.axes = self.fig.add_subplot(1, 1, 1)
        self.axes.set_axis_bgcolor('black')
        self.axes.set_title('XXX', size=20)
        self.axes.grid(True, color='white', linewidth=2)
        pylab.setp(self.axes.get_xticklabels(), fontsize=21)
        pylab.setp(self.axes.get_yticklabels(), fontsize=21)
        
        self.axes2 = self.fig2.add_subplot(1, 1, 1) 
        self.axes2.set_axis_bgcolor('black')
        self.axes2.set_title('XXX', size=20)
        self.axes2.grid(True, color='white', linewidth=2)
        pylab.setp(self.axes2.get_xticklabels(), fontsize=21)
        pylab.setp(self.axes2.get_yticklabels(), fontsize=21)

        
        # creates the tamb graph plot inside the first panel
        self.tamb_canvas = FigCanvas(self.tamb_panel_1, -1, self.fig)
        #createst the tobj graph plot inside the second panel
        self.tobj_canvas = FigCanvas(self.tobj_panel_2, -1, self.fig2)
        
        mylog10.debug(repr(self.tamb_canvas) )
        mylog10.debug(repr(self.tobj_canvas) )
    
    
    def On_Sim(self, event):
        """This function determines if sim is being used or not
        sets the sim parameter        
        """
        #store the sim value into a local variable first and then pass onto self variable
        result = self.sim_checkbox.GetValue()
        self.simvalue = result
        #print 'result: ', self.simvalue
        
        #run the function to do sim analysis to check the state of the checkbutton 
        self.sim_analysis()

    def On_Start(self, event):
        '''Start button to run the script'''
        '''For nthreads the .start() function runs the thread therefore use that in the onstart button 
        otherwise 
        Dont put the .start() function inside the init() function and then use run() function inside the onstart button then youll
        run the function twice and screw yourself over big big time !!!
        '''
        self.myfile.q.put(('temp',self.val))
        self.myfile.q.put(('jump',self.val2))
        #start the redo event
        self.redo(event)
        print 'starting from gui'
        #start the thread
        self.myfile.start()
        
        
    def On_Close(self, event):
        """Close Button to close the GUI"""
        print 'Closing GUI'
        print 'Thank you and Have a Good Day'

        self.myfile.q.put(('end','end'))
        self.redraw_timer.Stop()
        self.Destroy()
    
    def redraw_graph(self, event):
        """Function which redraws the graph
        """
        #empty local lists to store the data
        tamb_ans = []
        tobj_ans = []
        for item in self.myfile.class_list:
            value = item
            self.y = (value.address, value.tobj_ans, value.tamb_ans, value.record_list) #value.address, value.tobj_num, value.tamb_num, value.record_list)
            #a tuple. list of data is stored/saved 
            tobj_ans.append(self.y[1])
            #appending the tamb ans to the tamb list
            tamb_ans.append(self.y[2])
            
            #append the data into a list 
            self.tamb_list.append(tamb_ans)
            self.tobj_list.append(tobj_ans)
            
            #here we are appending the control text variables to the textctrl widget
            #this is the ambient data analysis results
            self.text_ctrl_1.AppendText("Address + " + str(self.y[0]) + " - Value - " + str( self.y[3][3] ) + "\n")
            self.text_ctrl_2.AppendText("Address + " + str(self.y[0]) + " - Value - " + str( self.y[3][4] ) + "\n")
            self.text_ctrl_3.AppendText("Address + " + str(self.y[0]) + " - Value - " + str( self.y[3][5] ) + "\n")
            
            #here we are appending the control text variables to the textctrl widget
            #this is the ambient data analysis results
            self.text_ctrl_4.AppendText("Address + " + str(self.y[0]) + " - Value - " + str( self.y[3][0] ) + "\n")
            self.text_ctrl_5.AppendText("Address + " + str(self.y[0]) + " - Value - " + str( self.y[3][1] ) + "\n")
            self.text_ctrl_6.AppendText("Address + " + str(self.y[0]) + " - Value - " + str( self.y[3][2] ) + "\n")

        #make the appended data into an array for transposing purposes
        tambvalarray = np.array(self.tamb_list)
        tobjvalarray = np.array(self.tobj_list)
        
        #transpose the array so that the array [s1,s2] can be appened vertically 
        self.tamb_array = tambvalarray.transpose() 
        self.tobj_array = tobjvalarray.transpose()
        
        #here we are iterating across the ambient temperature data 
        #the cycle is herre so we can use it as an index item to get the colors we can use 
        tamb_cycle=0
        
        #clear autoscale and add in the grid for the sensors 
        self.axes.cla()
        self.axes.autoscale(enable=True)
        self.axes.grid(True, color='white', linewidth=2)
        pylab.setp(self.axes.get_xticklabels(), fontsize=21)
        pylab.setp(self.axes.get_yticklabels(), fontsize=21)
        
        #iterating over the values inside the array (the array will ahve a number of lists equal to the number 
        #of sensors available
        for iteritem in self.tamb_array:
            #iterate the cycle
            tamb_cycle+=1
            
            #color value is the cycle counter plus the index item
            #TODO: what happens if the list is exhauted ???
            colorvalue = self.color[tamb_cycle]
         
            #set the the x value this is just a iterative placeholder
            xval = np.arange(len(iteritem) )
            
            #replot the data ambient temperature
            graph = self.axes.plot(xval[-100:], iteritem[-100:], linewidth=3,color=colorvalue,)
            
            plt.legend('xxx', loc='upper left', shadow=True)
            #self.axes.plot(xval, iteritem, linewidth=3,color=colorvalue,)
            #self.axes.plot(iteritem[-10:], linewidth=3,color=colorvalue,)
            
            #show the canvas
            self.tamb_canvas.draw()
        
        #here we are iterating across the object temperature data 
        #tobj cycle=0
        tobj_cycle=0
        
        #clear autoscale and add in the grid for the sensors 
        self.axes2.cla()
        self.axes2.autoscale(enable=True)
        self.axes2.grid(True, color='white', linewidth=2)
        pylab.setp(self.axes2.get_xticklabels(), fontsize=21)
        pylab.setp(self.axes2.get_yticklabels(), fontsize=21)
        
        #iterating over the cycle
        for item in self.tobj_array:
            #iterate the cycle
            tobj_cycle+=1
            #color value is the cycle counter plus the index item
            #TODO: what happens if the list is exhauted, we get a huge error need to fix this to a color 
            #one solution is to make the size unlkely to exhaust            ???
            
            #pick the colorvalue from the color list
            colorvalue = self.color[tobj_cycle]
            
            #set up the xc value, note this is just a iterative placeholder
            xvalb = np.arange(len(item) )
            
            #replot the data
            self.axes2.plot(xvalb[-100:], item[-100:], linewidth=3,color=colorvalue, label=self.y[0])
            
            #show the canvas
            self.tobj_canvas.draw()
            

class MyApp(wx.App):
    def OnInit(self):
        # wx.InitAllImageHandlers()
        frame_1 = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(frame_1)
        frame_1.Show()
        return 1

###############################################################################

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()



