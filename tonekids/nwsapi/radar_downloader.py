'''
Created on Jul 20, 2017

@author: zaremba
'''

import os
import re
import urllib2
from fileinput import filename
import threading
import hashlib
import binascii
import time

class RadarDownloader(object):
    '''
    classdocs
    '''
    
    overlay_dirs = ['Cities', 'County', 'Highways', 'LatLon', 'RangeRings', 'Rivers', "Topo"]
    remote_url_base = 'https://radar.weather.gov/ridge/'
    
    def __init__(self, download_home_dir, station_id):
        self.station_id = station_id.upper()
        self.download_home_dir = download_home_dir + "/"
        self.last_radar_img_hash = "\x00"
        
    def download_url_to_local(self, remote_url, local_dest_dir, local_dest, duplicate=False):
        print "Downloading " + remote_url + " to " + local_dest
        
        if False == os.path.isdir(local_dest_dir):
            print "Creating directory " + local_dest_dir
            os.makedirs(local_dest_dir)
        
        if (True == os.path.exists(local_dest)) and (False == duplicate):
            print local_dest + " exists.  Skipping."
        else:
            try:
                remote_file = urllib2.urlopen(remote_url)
                remote_data = remote_file.read()
                local_file = open(local_dest, "wb")
                local_file.write(remote_data)
                local_file.close()
            except urllib2.HTTPError as e:
                print "HTTPError " + str(e.code) + " occurred downloading " + remote_url + ": " + e.reason
        
    def download_overlays(self):
        remote_url_overlay_base = self.remote_url_base + "Overlays/"
        local_overlay_base = self.download_home_dir + "Overlays/"
        
        for dir in self.overlay_dirs:
            for ls in ("Short", "Long"):
                if 'Topo' == dir:
                    extension = '.jpg'
                else:
                    extension = '.gif'
                    
                if 'Cities' == dir:  #this is because the NWS is smoking crack
                    filetype_name = 'City'
                elif 'RangeRings' == dir:  #lots of crack
                    filetype_name = 'RangeRing'
                else:
                    filetype_name = dir
                    
                remote_url = remote_url_overlay_base + dir + "/" + ls + "/" + self.station_id + "_" + filetype_name + "_" + ls + extension
                local_dest_dir = local_overlay_base 
                
                local_dest = local_dest_dir + self.station_id + "_" + filetype_name + "_" + ls + extension
                
                self.download_url_to_local(remote_url, local_dest_dir, local_dest)
    
    def download_current_radar_image(self, type):
        type = type.upper()
        filename = self.station_id + "_" + type + "_0.gif"
        remote_url_base = self.remote_url_base + "RadarImg/"
        remote_url = remote_url_base + type + "/" + filename
        
        local_dest_dir = self.download_home_dir + "RadarImg/" + self.station_id + "/" + type + "/realtime/" 
        local_dest = local_dest_dir + filename
        
        if True == os.path.exists(local_dest):
            #there is already a last-downloaded processed file
            print "Checking hash of existing downloaded radar file..."
            ext_file = open(local_dest, "rb")
            ext_file_data = ext_file.read()
            hash = hashlib.md5()
            hash.update(ext_file_data)
            self.last_radar_img_hash = hash.digest()
        
        self.download_url_to_local(remote_url, local_dest_dir, local_dest, duplicate=True)
        
        img_data_file = open(local_dest, "rb")
        img_data = img_data_file.read()
        img_data_file.close()
        hash = hashlib.md5()
        hash.update(img_data)
        img_data_hash = hash.digest()
        print "Img hash is " + binascii.hexlify(img_data_hash)
        print "Previous img hash is " + binascii.hexlify(self.last_radar_img_hash)
        if img_data_hash != self.last_radar_img_hash:
            print "This is new radar image data."
            self.last_radar_img_hash = img_data_hash
            curtime = time.gmtime()
            timestr = time.strftime("%Y%m%d-%H%M%S", curtime)
            radar_file = open(local_dest_dir + self.station_id + "_" + type + "_" + timestr + ".gif", "wb")
            radar_file.write(img_data)
            radar_file.close()
        else:
            print "This is duplicate radar image data."
                
    def download_radar_image_history(self, type):
        type = type.upper()
        remote_url_base = self.remote_url_base + "RadarImg/"
        remote_url_base = remote_url_base + type + "/" + self.station_id + "/" 
        
        local_dest_dir = self.download_home_dir + "RadarImg/" + self.station_id + "/" + type + "/"
        
        img_list_url = urllib2.urlopen(remote_url_base)
        
        rex = re.compile('<a href=\".*?\">(.*?\.gif)</a>')
        
        while(True):
            img_list_url_data_line = img_list_url.readline()
            if '' == img_list_url_data_line:
                break
            match_obj = rex.search(img_list_url_data_line)
            
            #print img_list_url_data_line
            
            if None != match_obj:
                #print match_obj.group(1)
                filename = match_obj.group(1)
                remote_url = remote_url_base + filename
                local_dest = local_dest_dir + filename
                
                self.download_url_to_local(remote_url, local_dest_dir, local_dest)   
                
class RadarDownloadTimer(object):
    def __init__(self, download_home_dir, station_id, data_type):
        self.radar_downloader = RadarDownloader(download_home_dir, station_id)
        self.data_type = data_type
        self.timer = None
        self.is_running = False
        self.interval = 0.0
        
    def start(self, interval):
        '''
        interval is in minutes
        '''
        self.interval = interval
        print "Radar download timer set to " + str(self.interval) + " minutes."
        self.timer = threading.Timer(interval * 60.0, self.timer_callback)
        self.timer.start()
        print "Radar download timer started."
        self.is_running = True
    
    def timer_callback(self):
        print "Radar download timer fired.  Downloading..."
        self.radar_downloader.download_current_radar_image(self.data_type)             
        if True == self.is_running:
            print "Radar download timer resetting."
            self.start(self.interval)
            
            
    def stop(self):
        if True == self.is_running:
            self.timer.cancel()
            self.is_running = False
            print "Radar download timer stopped."
    