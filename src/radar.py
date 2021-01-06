import os
import sys
import logging
#import argparse
from urllib.parse import quote_plus
from datetime import datetime
#from dateutil.parser import parse
import pytz

import requests
from bs4 import BeautifulSoup, Comment
import re
from io import BytesIO

from pprint import pprint

def bom_radar_image(radar: str = 'IDR503', when: datetime = datetime.now()):
    """
    Generate a radar PNG url based on a radar ID and datetime

    :param radar: A radar product ID from http://www.bom.gov.au/australia/radar/
    :param when: A <datetime> which will be converted to UTC and formatted for url
    :returns: url <str> for curl/wget/requests.get()
    """
    radar = quote_plus(radar)

    timestamp = when.astimezone(pytz.utc).strftime("%Y%m%d%H%M")
    url = f"http://www.bom.gov.au/radar/{radar}.T.{timestamp}.png"
    return(url)

def bom_radar_s3_key(radar: str = 'IDR553', when: datetime = datetime.now(), extn: str = 'png'):
    """
    Generate an S3 key from radar and timestamp

    :param radar: A radar product ID
    :param when: A <datetime> which will be converted to UTC and formatted
    :returns: S3 Key <str> for s3.put_object()
    """
    timestamp = when.astimezone(pytz.utc).strftime("%Y/%m/%d/%H%M")
    return(f"radar/{radar}/{timestamp}Z.{extn}")

def bom_radar_name(soup):
    """ 
    Find the radar name from a bom radar page using BeautifulSoup
    """
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    
    radar_names = []
    for comment in comments: 
        radar_names = radar_names + re.findall(r"radar_name: (.*)}", str(comment))

    return(radar_names[0])

def bom_radar_state(soup):
    """ 
    Find the state from a bom radar page using BeautifulSoup
    """
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    
    radar_names = []
    for comment in comments: 
        radar_names = radar_names + re.findall(r"radar_name: (.*)}", str(comment))

    return(radar_names[0])

def bom_radar_images(radar: str = 'IDR664'):
    """
    Get a list of active radar image urls

    :param radar: A radar product ID from http://www.bom.gov.au/australia/radar
    :returns: <list[str]> of url(s)
    """

    # Build page url from radar
    url = f"http://www.bom.gov.au/products/{radar}.loop.shtml"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    dv = soup.find(class_='public-radar')
    scripts = dv.find_all('script')
    imgs = []
    for s in scripts:
        imgs = imgs + re.findall(r"(/radar/[\w\d]+\.T\.[\d]{12}.png)", str(s.string))

    return(imgs)

def bom_radar_sites():
    """
    Get a dictionary of active radar sites from http://www.bom.gov.au/australia/radar

    :returns: list<dict> of sites
    """
    url = f"http://www.bom.gov.au/australia/radar/"

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    map = soup.find('map')

    radar = []
    for area in map.find_all('area'):
        radar.append({
            'title': area.get('title'),
            'url': area.get('href'),
            'radar': re.findall(r'/products/(.*).loop', area.get('href'))[0]
        })

    return(radar)
    
def bom_radar_state_sites(state: str = 'qld'):
    """
    Get a list of radars at many resolutions for a single state

    :param state: <str> One of: [nsw, vic, qld, wa, sa, tas, nt]
    :returns: <list[str]> of radar codes
    """
    url = f"http://www.bom.gov.au/australia/radar/{state}_radar_sites_table.shtml"

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    sites = soup.find('table')
    radars = []
    for site in sites.find_all('a'):
        if re.match(r"/products/.*", site.get('href')):
            radars.append(re.findall(r'/products/(.*).loop', site.get('href'))[0])

    return(radars)


if __name__ == "__main__":
    #states = ["nsw", "vic", "qld", "wa", "sa", "tas", "nt"]
    #radars = []
    #for state in states:
    #    radars = radars + bom_radar_state_sites(state)
    #images = []
    #for radar in radars:
    #    images = images + bom_radar_images(radar)
    #print(images)

    imgs = bom_radar_images("IDR663")

    pprint(imgs)
    pass
