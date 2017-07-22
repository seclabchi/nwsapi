'''
Created on Jul 22, 2017

@author: zaremba
'''

import Tkinter as tk

class UiCanvasRadar(tk.Canvas, object):
    '''
    classdocs
    '''

    def __init__(self, master, station_id, *args, **kwargs):
        '''
        Constructor
        '''
        self.station_id = station_id
        tk.Canvas.__init__(self, master=master, *args, **kwargs)
        self.config(width=600, height=550, bg="#333333")
    