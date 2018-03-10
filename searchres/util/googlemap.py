#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 11:39:22 2018

@author: JoshuaZhou
"""

import googlemaps
KEY = 'AIzaSyCvCGQEpPnDAJZ1fr56cSvWqdCuWNdxWqk'

def get_geocode(address):
    '''
    Geocoding an address
    Input:
        address: input from user
    Output:
        tuple: (location_type, coordinates, formatted_address)
    '''
    gmaps = googlemaps.Client(KEY)
    geocode_result = gmaps.geocode(address)
    geo_dict = geocode_result[0]
    loc_type = geo_dict['geometry']['location_type']
    loc = geo_dict['geometry']['location']
    formatted_address = geo_dict['formatted_address']
    
    return (loc_type, loc, formatted_address)
    
'''
if __name__ == '__main__':    
    address = "Rockefeller center"
    rv = get_geocode(address)
    print('\n',rv)
    
'''