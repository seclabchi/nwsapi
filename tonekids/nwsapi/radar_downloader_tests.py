'''
Created on Jul 20, 2017

@author: zaremba
'''
import unittest
import time
from radar_downloader import *

class TestRadarDownloader(unittest.TestCase):

    rd = None
    
    def setUp(self):
        self.rd = RadarDownloader('/Users/zaremba/tmp/nwsapi', 'lOt')
        
    def tearDown(self):
        pass

    def testDownloadOverlays(self):
        self.rd.download_overlays()
        
    def testDownloadRadarImageHistory(self):
        self.rd.download_radar_image_history('ncR')
        
    def testDownloadTimer(self):
        rd_timer = RadarDownloadTimer('/Users/zaremba/tmp/nwsapi', 'LOT', 'NCR')
        rd_timer.start(5)
        time.sleep(36000)
        rd_timer.stop()
    
    def testDownloadCurrentRadarImage(self):
        self.rd.download_current_radar_image("NCR");
        
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()