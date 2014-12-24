#!/usr/bin python
# -*- coding: utf-8 -*-

""" Pincode to OSM Map url

pin = '380061'

API = '6207f57bfae3ea4c762fd595398e50ba'

url = 'http://data.gov.in/api/datastore/resource.json?resource_id=6176ee09-3d56-4a3b-8115-21841576b2f6&api-key=<API>&filters[pincode]=<pin>&fields=officename,pincode,officeType,Deliverystatus,divisionname,regionname,circlename,Taluk,Districtname,statename'

a = urllib.request.urlopen(url)

out = json.loads(a.read())

 https://www.openstreetmap.org/#map=16/23.0662/72.5329

"""
import sys
import json
from urllib.request import urlopen


def getPinData(key, pin):
    # get data from data.gov.in based on API-key and pincode
    #~ print(key, pin)
    reqUrl = 'http://data.gov.in/api/datastore/resource.json?resource_id=6176ee09-3d56-4a3b-8115-21841576b2f6&api-key=' + key + '&filters[pincode]=' + pin + '&fields=officename,pincode,officeType,Deliverystatus,divisionname,regionname,circlename,Taluk,Districtname,statename'

    req = urlopen(reqUrl)

    return req.read()

def parsePinData(jsonData):
    # parse to get records and first Officename, districtname
    ofcName = None
    districtName = None
    parseJson = json.loads(jsonData)
    if 'records' in parseJson:
        ofcName = parseJson['records'][0]['officename']
        districtName = parseJson['records'][0]['Districtname']
        return ofcName, districtName

def getLatLong(name, pin=None):
    # search for lat long based on names in Nominatim
    # can use names
    # can use pin directly
    if pin:
        reqUrl = 'http://nominatim.openstreetmap.org/search?postalcode=%s&format=json' \
        % (pin)
    else:
        reqUrl = 'http://nominatim.openstreetmap.org/search?city=%s&country=india&format=json' \
        % (name[1])

    req = urlopen(reqUrl)
    locJson = req.read().decode()
    latLon = json.loads(locJson)
    return (latLon[0]['lat'], latLon[0]['lon'], latLon[0]['display_name'])

def genOSMUrl(latLon):
    #  https://www.openstreetmap.org/#map=16/23.0662/72.5329
    #  https://www.openstreetmap.org/#map=16/lat/lon
    url = 'https://www.openstreetmap.org/#map=16/'
    osmUrl = url + latLon[0][:8] + '/' + latLon[1][:8]
    return osmUrl


if __name__ == "__main__":
    err1 = "Provide API Key followed by Pincode! "
    if len(sys.argv) == 1:
        print("Error in Arguments.")
        print(err1)
        sys.exit(0)
    elif len(sys.argv) == 2:
        print("Error in Arguments. Either API Key or Pincode missing.")
        print(err1)
        sys.exit(0)
    elif len(sys.argv) == 3:
        print("API provided is %s" % sys.argv[1])
        print("Pincode provided is %s" % sys.argv[2])
    else:
        print("Error in Arguments.")
        print(err1)
        sys.exit(0)

    pinData = getPinData(sys.argv[1], sys.argv[2])
    #print(pinData)
    ofcName = parsePinData(pinData.decode())
    #print(ofcName)
    latLon = getLatLong(ofcName)
    #~ latLon = getLatLong(ofcName, pin)
    #print(latLon)
    osmUrl = genOSMUrl(latLon)
    print(osmUrl)
