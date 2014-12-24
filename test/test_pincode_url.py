""" test getPincodeUrl Script to fetch data from data.gov.in """

import unittest
import getPincodeUrl

class TestPincodeToUrl(unittest.TestCase):

    def setUp(self):
        self.pin = '380061'
        self.key = '6207f57bfae3ea4c762fd595398e50ba'
        self.pinData = None
        self.ofcName = None
        self.latLon = None
        self.osmUrl = None

    def test_pincode_data(self):
        # receive json response
        self.pinData = getPincodeUrl.getPinData(self.key, self.pin)
        #print(self.pinData)
        assert b'records' in self.pinData

    def test_parse_data(self):
        # parse json response
        self.pinData = getPincodeUrl.getPinData(self.key, self.pin)
        #print(self.pinData)
        self.ofcName = getPincodeUrl.parsePinData(self.pinData.decode())
        #print(self.ofcName)
        assert self.ofcName is not None
#~ 
    def test_locn_data_fetch(self):
        # use Nominatim for location fetching
        # pin or cityname based
        self.pinData = getPincodeUrl.getPinData(self.key, self.pin)
        #print(self.pinData)
        self.ofcName = getPincodeUrl.parsePinData(self.pinData.decode())
        #print(self.ofcName)
        self.latLon = getPincodeUrl.getLatLong(self.ofcName)
        #~ #self.latLon = getPincodeUrl.getLatLong(self.ofcName, self.pin)
        print(self.latLon)
        assert len(self.latLon) == 3

    def test_map_url_gen(self):
        # generate osm link using lat lon values
        self.pinData = getPincodeUrl.getPinData(self.key, self.pin)
        #print(self.pinData)
        self.ofcName = getPincodeUrl.parsePinData(self.pinData.decode())
        #print(self.ofcName)
        self.latLon = getPincodeUrl.getLatLong(self.ofcName)
        #~ self.latLon = getPincodeUrl.getLatLong(self.ofcName, self.pin)
        #print(self.latLon)
        self.osmUrl = getPincodeUrl.genOSMUrl(self.latLon)
        print(self.osmUrl)
        assert 'https://' in self.osmUrl

if __name__ == '__main__':
    unittest.main()
