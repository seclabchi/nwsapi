'''
Created on Jul 22, 2017

@author: zaremba
'''

import Tkinter as tk
from ui_canvas_radar import *
from tonekids.nwsapi import ui_canvas_radar

class UiMain(tk.Tk, object):
    '''
    classdocs
    '''
    shutdown_signaled = False
    
    def __init__(self, *args, **kwargs):
        '''
        Constructor
        '''
        tk.Tk.__init__(self, *args, **kwargs)
        self.setup_ui()
        
    def setup_ui(self):
        self.title('Secret Lab Console:  NWS Radar View')
        self.frame_main = tk.Frame(self)
        self.frame_main.grid()
        self.lot_radar_plot = ui_canvas_radar.UiCanvasRadar(self, "LOT")
        self.lot_radar_plot.grid(row=0, column=0)
        
        
    def shutdown(self):
        UiMain.shutdown_signaled = True
       
    def go(self):
        print "Hello.  Starting UI..."
        
        self.protocol('WM_DELETE_WINDOW', self.shutdown)
        
        while False == UiMain.shutdown_signaled:
            self.update_idletasks()
            self.update()
            
        print "Goodbye."
    
       
def main():
    app = UiMain() 
    app.go()
        
if __name__ == '__main__':
    main()