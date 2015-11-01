#!/usr/bin/python

#mlx_wx.py

'''This gui is the hardcorded version to the sim gui 
outputs the data into a notepad and then will change the temp limit 
parameters as needed 
this will gives us an understanding of how the gui is set up 
'''

import sys
import time
import wx #, gettext

import wx.lib.plot as plot

import matplotlib.pyplot as plt


from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
import pylab

import numpy as np

#import threading 
#import Queue
import time
import logging
#from sim.mlx90614_sim import Main as myMain
import sim.mlx90614_sim

#http://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.transpose.html
#http://matplotlib.org/users/pyplot_tutorial.html
#http://newville.github.io/wxmplot/plotpanel.html
#https://www.daniweb.com/programming/software-development/code/216913/using-wxpython-for-plotting

logging.basicConfig(filename='XXX.log', filemode='a', level=logging.DEBUG, format='%(asctime)s, %(levelname)s, %(message)s')
logging.info(" ---------------------- root --------------------------------")
mylog9 = logging.getLogger('XXX')


class TerminalFrame(wx.Frame):
    '''This is the base frame
    '''
    def __init__(self, *args, **kwds): #, parent, title):
        wx.Frame.__init__(self, *args, **kwds)
        #wx.Frame.__init__(self, parent, title=title, size=(600,400))
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.panel = wx.Panel(self)
        
        self.button = wx.Button(self, -1, "Button")
        self.button2 = wx.Button(self, -1, "Button2")
        
        self.button3 = wx.Button(self, -1, "Start")
        self.button4 = wx.Button(self, -1, "Close")
        self.button5 = wx.Button(self, -1, "XXX")
        
        self.ddict={}
        self.ans = []
        self.ans2 = []
        self.y=[0,0] #None
        self.color= ['green','red', 'blue', 'yellow', 'magenta']
        
        # loop in run function
        # Timer class event
        self.redraw_timer = wx.Timer(self)
        
        
        #create status bar
        self.CreateStatusBar()
        #setup the sizers
        self.sizer_setup()
        #stup the graph in the panel
        self.init_graph()
        #add events
        self.attach_events()
        #call the simulator calss
        self.myfile = sim.mlx90614_sim.Main() #myMain()
        #if you don't use self,dameon = True then even if the gui shuts down the script will still go crazy
        #and be running without your control
        #running the dameon
        self.myfile.daemon = True
        
        mylog9.debug('GUI LOG'+ repr(self.myfile) )
        

    def attach_events(self):
        #This function is designed to run the script 
        self.Bind(wx.EVT_BUTTON, self.OnStart, self.button3)
        self.Bind(wx.EVT_BUTTON, self.OnClose, self.button4)
        self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)
        self.Bind(wx.EVT_TIMER, self.onpause, self.button5)
    
    def onpause(self, event):
        self.redraw_timer.Pause()

    
    def on_redraw_timer(self, event):
        '''This function loops the OnStart event button until new parameters
        are not added when the pause button is clicked.'''
        #self.redraw_graph(event)
        self.data_analysis(event)
        

    def OnStart(self, event):
        '''For nthreads the .start() function runs the thread therefore use that in the onstart button 
        otherwise 
        Dont put the .start() function inside the init() function and then use run() function inside the onstart button then youll
        run the function twice and screw yourself over big big time !!!
        '''
        print 'starting from gui'
        self.myfile.start()
        self.redo(event)
        #event.Skip()

    def OnClose(self, event):
        self.redraw_timer.Stop()
        self.Destroy()
        #event.Skip()
        
    def sizer_setup(self):

        #this sizer sets up the first horizontal row which is our buttons 
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.button, 1, wx.EXPAND)
        self.sizer.Add(self.button2, 1, wx.EXPAND)
        #this sizer adds om the second set of buttons labelled porn-expilcitally 
        self.sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer3.Add(self.button3, 1, wx.EXPAND)
        self.sizer3.Add(self.button4, 1, wx.EXPAND)
        self.sizer3.Add(self.button5, 1, wx.EXPAND)
        
        #This is the main sizer window so we are positioning everything in a top down fashion approach
        #we are adding the text control and a panel as well
        self.sizer2 = wx.BoxSizer(wx.VERTICAL)
        self.sizer2.Add(self.control, 1, wx.EXPAND)
        self.sizer2.Add(self.sizer)
        self.sizer2.Add(self.panel, 1, wx.EXPAND)
        self.sizer2.Add(self.sizer3)
        
        #this is needed to show the sizers and the resulting widgets
        # This is going to show the PARENt SIZER ONLY
        self.SetSizer(self.sizer2)
        #self.SetAutoLayout(1)
        #self.sizer.Fit(self)
        self.Show()
    
    def init_graph(self):
        '''initalizing the graph setup inside the panel
        '''
        self.fig = Figure(figsize=(8, 6), dpi=40)
        
        # setting the axes fo the figure graph
        self.axes = self.fig.add_subplot(1, 1, 1)
        self.axes.set_axis_bgcolor('black')
        self.axes.set_title('XXX', size=20)
        self.axes.grid(True, color='red', linewidth=2)
        pylab.setp(self.axes.get_xticklabels(), fontsize=16)
        pylab.setp(self.axes.get_yticklabels(), fontsize=16)

        # This is the first plot graph
        self.plotData = self.axes.plot([0], linewidth=1, color=(1, 1, 0),)[0]
        
        # This is the canvas display for the first notepad tab-v1
        self.canvas = FigCanvas(self.panel, -1, self.fig)
        
    
    def data_analysis(self, event):
        #parsing the data
        #~ for item in self.myfile.sensorfile.simulator_list:
        #for item in self.myfile.sensorfile.simulator_list:
        #self.y = self.myfile.callx
        #for item in self.myfile.sensorfile.simulator_list:
        #    self.y = self.myfile.callx
        #self.control.AppendText(str(self.y) + "\n")
        #self.control.AppendText(str(self.myfile.class_list) + "\n")
        
        ans = []
        
        for item in self.myfile.class_list:
            value = item
            self.y = (value.address, value.tobj_num)
            self.control.AppendText(str(value) + "\n")
            self.control.AppendText('ans: ' + str(self.y) + "\n")
            #a tuple. list of data is stored/saved 
            ans.append(self.y[1])
            #append the data into a list 
            self.ans.append(ans)
        #print 'self.ans: ', self.ans
        self.control.AppendText('selfans: ' + str(self.ans) + "\n")
        #print 'len: ', len(self.ans)
        
        #make the appended data into an array 
        valarray = np.array(self.ans)
        #print 'valarray: ', valarray #np.shape(valarray)
        #print 'valarray: ', valarray
        #self.control.AppendText('valarray: ' + str(valarray) + "\n")
        
        #transpose the array so that the array [s1,s2] can be appened vertically 
        self.ans2 = valarray.transpose()
        print 'self.ans2: ', self.ans2
        self.control.AppendText('self.ans2: ' + str(self.ans2) + "\n")
        
        

        #plt.plot(self.ans2[0], 'r', self.ans2[1], 'b')
        #plt.show(block=False)
        #plt.draw()
        
        #self.canvas.draw()
        #ans2.append(ans)
        #self.control.AppendText('ans2 list: ' + str(ans2) + "\n")
        #for item in self.ans:
        #    print 'item: ', item
            
            #for value in item:
                #print 'value: ', value
        #clear autoscale and add in the grid for the sensors 
        self.axes.cla()
        self.axes.autoscale(enable=True)
        self.axes.grid(True, color='red', linewidth=2)
        
        #the cycle is herre so we can use it as an index item to get the colors we can use 
        cycle=0
        #iterating over the values inside the array (the array will ahve a number of lists equal to the number 
        #of sensors available
        for item in self.ans2:
            #iterate the cycle
            cycle+=1
            #color value is the cycle counter plus the index item
            #TODO: what happens if the list is exhauted ???
            colorvalue = self.color[cycle]
            print 'colorvalue: ',colorvalue
            self.axes.plot(item[-30:], linewidth=3,color=colorvalue,)[0:] #(1, 1, 0),)[0:]
            self.canvas.draw()
        #Need a nameerror here 
        #self.axes.plot(self.ans2[0], linewidth=3,color=(1, 1, 0),)[0:]
        #self.axes.plot(self.ans2[1], linewidth=3,color='green',)[0:]
        #self.canvas.draw()
    

        #print item
        #self.ddict[item] = []
        #print self.ddict
        #print self.ddict.keys()
                
        
    def redraw_graph(self, event):
        #redrawing the graph
        #self.redraw_timer.Start(3)
        
        #self.control.AppendText(str(self.myfile.callx) + "\n")
        #self.control.AppendText(str(self.myfile.class_list) + "\n")
    
        if self.myfile.callx == None:
            pass
        else:
            value = self.myfile.callx #.values()
            if value == self.y: 
                pass
            else:
                self.y = value
                
                if self.y[0] in self.ddict.keys():
                    print 'yes key is present '
                    self.ddict[self.y[0] ].append(self.y[1] )
                    a=self.ddict[90]
                    b=self.ddict[91]
            #self.data_analysis(event)
        #    self.control.AppendText(str(self.y) + "\n")
        #    self.yval.append(self.y)
            #print 'self.yval: ', self.yval
        #self.y = self.myfile.callx
                    self.control.AppendText(str(self.y) + "\n")
                    self.control.AppendText(str(self.ddict) + "\n")
                    #for item in self.ddict.keys():
                    ans = zip(self.ddict[item], self.ddict[item]) #a, b)
                        #for item in self.ddict.keys():
                    self.axes.cla()
                    self.axes.autoscale(enable=True)
                    self.axes.grid(True, color='red', linewidth=2)
                    #Need a nameerror here 
                    self.axes.plot(ans, linewidth=3,color=(1, 1, 0),) #[0:]
                    #self.axes.plot(b, linewidth=3,color=(1, 1, 0),) #[0:]
                    self.canvas.draw()
        #print 'xxx: ', self.y
   
    
    def redo(self, event):
        self.redraw_timer.Start(3000) #3 second interval
        #self.redraw_graph(event)
        self.data_analysis(event)
        
        
        


# end of class TerminalSettingsDialog
class MyApp(wx.App):
    def OnInit(self):
        #wx.InitAllImageHandlers()
        frame_terminal = TerminalFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(frame_terminal)
        frame_terminal.Show()
        return 1

# end of class MyApp
######################################################################
if __name__ == "__main__":
    #gettext.install("app") # replace with the appropriate catalog name
    app = MyApp(0)
    app.MainLoop()
    


########################################################################
#app = wx.App(False)
#frame = TerminalFrame(None, 'Small editor')
#app.MainLoop()

'''
class MyApp(wxmain.MyApp):
    def OnInit(self):
        wx.InitAllImageHandlers()
        frame_terminal = TerminalFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(frame_terminal)
        frame_terminal.Show()
        return 1


if __name__ == "__main__":
    gettext.install("app") # replace with the appropriate catalog name

    app = MyApp(0)
    app.MainLoop()

'''

'''
class MyApp(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        frame_terminal = TerminalFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(frame_terminal)
        frame_terminal.Show()
        return 1

################################################
if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()

'''
