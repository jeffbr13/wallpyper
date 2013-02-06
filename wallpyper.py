#!/usr/bin/env python
# -*- coding: utf-8 -*-

import errno
from bs4 import BeautifulSoup
import requests
import os
import os.path as path
import random
import re
import subprocess


def main():
    """
    Update your GNOME desktop background from some online location.

    By default this is the top upvoted image on
    <reddit.com/r/wallpaper+wallpapers>.
    """
    install_location = path.expanduser('~/.config/wallpyper/')
    image_location = path.join(install_location, 'image')

    image_url = find_reddit_image()
    image_data = download_image(image_url)
    save_image(image_location, image_data)
    set_wallpaper(image_location)
    return


def set_wallpaper(image_location):
    """
    Given the expanded path to the image on disk, sets it as the current
    desktop background (on GNOME desktops at least).
    """

    # if GNOME...
    if subprocess.call(['gsettings', 'set', 'org.gnome.desktop.background',
            'picture-uri', "file://" + path.abspath(image_location)]) != 0:
        print "Could not set desktop background to " + path.abspath(image_location)
        print "Changing the background currently only works with GNOME/gsettings."

    print 'Desktop background changed!'
    return


def save_image(image_location, image_data):
    try:
        print 'Writing image to file.'
        f = open(image_location, 'wb')
    except IOError as e:
        if e.errno == errno.ENOENT:
            print 'Ensuring installation directory is present.'
            os.makedirs(path.dirname(image_location))
            f = open(image_location, 'wb')

    try:
        f.write(image_data)
    except IOError as e:
        print 'Writing image to ' + image_location + ' failed.'
        raise e
    finally:
        print 'Closing image file.'
        f.close()


def find_reddit_image():
    """
    Finhd the URL of one of this week's top Reddit wallpapers.
    """
    print 'Scraping /r/wallpaper+wallpapers...'

    try:
        index_request = requests.get('http://www.reddit.com/r/wallpaper+wallpapers/top/?sort=top&t=week')
    except requests.exceptions.ConnectionError as e:
        raise e

    index_html = index_request.text
    index_soup = BeautifulSoup(index_html)
    index_thumbnails = index_soup.find_all('a', class_='thumbnail')

    valid_href = re.compile('^http://i.imgur.com')
    valid_urls = []

    for thumb in index_thumbnails:
        if valid_href.match(thumb['href']):
            valid_urls.append(thumb['href'])

    return random.sample(valid_urls, 1)[0]


def download_image(image_href):
    try:
        print 'Fetching ' + image_href
        return(requests.get(image_href).content)
    except Exception as e:
        print 'Error downloading ' + image_href
        raise e


if __name__ == '__main__':
    main()
