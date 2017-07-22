'''
Created on Jul 20, 2017

@author: zaremba
'''
import unittest
from radar_downloader import *

class TestRadarDownloader(unittest.TestCase):

    rd = None
    
    def setUp(self):
        self.rd = RadarDownloader('/Users/zaremba/tmp/nwsapi', 'lOt')
        
    def tearDown(self):
        pass

    def testDownloadOverlays(self):
        self.rd.download_overlays()
        
    def testDownloadRadarImages(self):
        self.rd.download_radar_images('ncR')
        
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()