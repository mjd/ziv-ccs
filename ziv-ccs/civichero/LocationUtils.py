"""Contains various helper methods for working with locations.
   Functions primarily focus on updating geo coords."""
import urllib
from xml.dom import minidom, Node

__author__ = 'jlparise'



GOOGLE_GEOCODE_URL = 'http://maps.googleapis.com/maps/api/geocode/xml?address='
GOOGLE_DIRECTIONS_URL = 'http://maps.googleapis.com/maps/api/directions/xml?'
DIRECTIONS_ORIGIN_URL = 'origin='
DIRECTIONS_DEST_URL = 'destination='
SENSOR_STRING = '&sensor=false'


def convertToUrl(value):
    """Replaces invalid url characters to make teh string a URL."""
    s = str(value)
    return s.replace(' ', '+') + ','

def getGeoUrl(location):
    """Get the URL for geocoding a URL with google."""

    url = GOOGLE_GEOCODE_URL
    url += convertToUrl(location.street_address)
    url += convertToUrl(location.city)
    url += convertToUrl(location.state)
    #Don't need the comma on the last value
    url += convertToUrl(location.zip_code)[:-1]
    url += SENSOR_STRING

    return url


def getGeo(location):
    """Returns a tuple of lat, lon for the given location."""

    status = ''
    lat = ''
    lng = ''
    url = getGeoUrl(location)
    xml_file = urllib.urlopen(url)
    dom = minidom.parse(xml_file)

    for response in dom.getElementsByTagName('GeocodeResponse'):
        for statusNode in  response.getElementsByTagName('status'):
            for child in statusNode.childNodes:
                if child.nodeType == Node.TEXT_NODE:
                    status = child.data

        #If the status is no OK bail
        if len(status) <=0 or status != 'OK':
            return None

        for result in response.getElementsByTagName('result'):
            for geometry in result.getElementsByTagName('geometry'):
                for location in geometry.getElementsByTagName('location'):
                    for lat in location.getElementsByTagName('lat'):
                        for child in lat.childNodes:
                            if child.nodeType == Node.TEXT_NODE:
                                lat = child.data
                    for lng in location.getElementsByTagName('lng'):
                        for child in lng.childNodes:
                            if child.nodeType == Node.TEXT_NODE:
                                lng = child.data
    return lat, lng


def updateGeo(location):
    """Updates the lat and lon fields on the given location to the correct coords."""

    geo = getGeo(location)
    if not geo:
        return

    location.lat = geo[0]
    location.lon = geo[1]

def getDirectionsURL(fromAddress, toAddress):
    url = GOOGLE_DIRECTIONS_URL
    url += DIRECTIONS_ORIGIN_URL
    url += convertToUrl(fromAddress)[:-1]
    url += '&' + DIRECTIONS_DEST_URL
    url += convertToUrl(toAddress)[:-1]
    url += SENSOR_STRING

    return url


def getDirections(fromAddress, toAddress):
    url = getDirectionsURL(fromAddress, toAddress)
    print(url)
    xml_file = urllib.urlopen(url)
    dom = minidom.parse(xml_file)
    status = None
    for response in dom.getElementsByTagName('DirectionsResponse'):
        for statusNode in  response.getElementsByTagName('status'):
            for child in statusNode.childNodes:
                if child.nodeType == Node.TEXT_NODE:
                    status = child.data

        #If the status is no OK bail
        if len(status) <= 0 or status != 'OK':
            return None

