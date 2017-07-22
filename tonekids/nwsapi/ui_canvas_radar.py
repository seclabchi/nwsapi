'''
Created on Jul 22, 2017

@author: zaremba
'''

import Tkinter as tk
from PIL import ImageTk, Image

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
        self.config(width=600, height=550, bg="#333333", cursor='crosshair')
        #test_topo_img = pil.Image('/Users/zaremba/tmp/nwsapi/Overlays/LOT_Topo_Short.jpg')
        self.test_topo_pi = ImageTk.PhotoImage(Image.open('/Users/zaremba/tmp/nwsapi/Overlays/LOT_Topo_Short.jpg'))
        self.create_image((0,0), anchor=tk.NW, image=self.test_topo_pi)