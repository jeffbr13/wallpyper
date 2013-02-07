#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import errno
from lxml import etree
import requests
import os
import os.path as path
import random
import re
import subprocess


def main(args):
    """
    Update your GNOME desktop background from an online source.

    By default this is the top upvoted image on
    <reddit.com/r/wallpaper+wallpapers>.
    """
    install_location = path.expanduser('~/.config/wallpyper/')
    image_location = path.join(install_location, 'image')

    if args.colourlovers:
        image_url = find_colourlovers_url()
        picture_options = 'wallpaper'
    else:
        image_url = find_reddit_url()
        picture_options = 'zoom'

    image_data = download_image(image_url)
    save_image(image_location, image_data)
    set_wallpaper(image_location, picture_options)
    return


def set_wallpaper(image_location, picture_options='zoom'):
    """
    Given the expanded path to the image on disk, sets it as the current
    desktop background (on GNOME desktops at least).

    The picture_options string can be one of "none", "wallpaper", "centered",
    "scaled", "stretched", "zoom", or "spanned".
    The most useful are "zoom" and "wallpaper" for images or tiles,
    respectively.
    """

    picture_uri = 'file://' + path.abspath(path.expanduser(image_location))

    # if GNOME...
    try:
        subprocess.call(['gsettings', 'set', 'org.gnome.desktop.background',
            'picture-uri', picture_uri])
        subprocess.call(['gsettings', 'set', 'org.gnome.desktop.background',
                'picture-options', picture_options])
    except:
        print "Could not set desktop background to " + picture_uri
        print "Changing the background currently only works with GNOME/gsettings."
        raise

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


def find_reddit_url():
    """
    Find the URL of one of this week's top Reddit wallpapers.
    """
    print 'Scraping /r/wallpaper+wallpapers...'

    try:
        index_request = requests.get('http://www.reddit.com/r/wallpaper+wallpapers/top/?sort=top&t=week')
    except requests.exceptions.ConnectionError as e:
        raise e

    valid_href = re.compile('^http://i.imgur.com')

    index_tree = etree.HTML(index_request.text)
    thumbnail_elements = index_tree.xpath("//a[contains(@class, 'thumbnail')]")
    valid_urls = [a.get('href') for a in thumbnail_elements
                                        if valid_href.match(a.get('href'))]

    return random.choice(valid_urls)


def find_colourlovers_url():
    """
    Get the URL of a top COLOURlovers pattern.
    """
    print 'Accessing the COLOURlovers pattern API...'

    try:
        payload = {'format': 'json'}
        pattern_request = requests.get('http://www.colourlovers.com/api/patterns/top', params=payload)
    except requests.exceptions.ConnectionError as e:
        raise e

    return random.choice(pattern_request.json)[u'imageUrl']


def download_image(image_href):
    try:
        print 'Fetching ' + image_href
        return(requests.get(image_href).content)
    except Exception as e:
        print 'Error downloading ' + image_href
        raise e


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Python script to update your GNOME desktop background from an online source.')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-r', '--reddit', help='Fetch wallpaper image from /r/wallpaper(s)', action="store_true")
    group.add_argument('-c', '--colourlovers', help='Fetch wallpaper pattern from http://www.colourlovers.com', action="store_true")

    args = parser.parse_args()

    main(args)
