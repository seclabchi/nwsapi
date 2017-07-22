'''
Created on Jul 20, 2017

@author: zaremba
'''

import os
import re
import urllib2
from fileinput import filename

class RadarDownloader(object):
    '''
    classdocs
    '''
    
    overlay_dirs = ['Cities', 'County', 'Highways', 'LatLon', 'RangeRings', 'Rivers', "Topo"]
    remote_url_base = 'https://radar.weather.gov/ridge/'
    
    def __init__(self, download_home_dir, station_id):
        self.station_id = station_id.upper()
        self.download_home_dir = download_home_dir + "/"
        
    def download_url_to_local(self, remote_url, local_dest_dir, local_dest):
        print "Downloading " + remote_url + " to " + local_dest
        
        if False == os.path.isdir(local_dest_dir):
            print "Creating directory " + local_dest_dir
            os.makedirs(local_dest_dir)
        
        if True == os.path.exists(local_dest):
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
                
    def download_radar_images(self, type):
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
        