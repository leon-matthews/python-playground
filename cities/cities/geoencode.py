#!/usr/bin/env python3

import collections
import csv
import json
import re
import urllib.parse
import urllib.request


# Installer
Installer = collections.namedtuple('Installer', 'name street suburb city phone')


# Location
Location = collections.namedtuple('Location', 'latitude longitude address')


def installers():
    "Generator to producing installer objects from csv file"
    with open('3m-installers.csv', 'rt') as f:
        reader = csv.reader(f)
        for row in reader:
            yield Installer(*row)


def get_location(i):
    """
    Use Google's geoencodeAPI to find installer location

    i   Installer object

    Returns Location object.
    """
    assert isinstance(i, Installer)
    url = "http://maps.googleapis.com/maps/api/geocode/json?"
    params = {
        'address': ', '.join((i.street, i.suburb, i.city)),
        'language': 'en',
        'region': 'nz',
        'sensor': 'false',
    }
    url = url + urllib.parse.urlencode(params)
    request = urllib.request.urlopen(url)
    data = request.read().decode()
    location = read_json(data)
    return location


def read_json(data):
    "Produce Location from given json string"
    d = json.loads(data)
    assert d['status'] == 'OK', "Response status not 'OK'"
    result = d['results'][0]
    latitude = result['geometry']['location']['lat']
    longitude = result['geometry']['location']['lng']
    address = result['formatted_address']
    return Location(latitude, longitude, address)


def format_phone(phone):
    assert isinstance(phone, str)
    # Remove all whitespace
    phone = re.sub('\s', '', phone)
    # Add space after prefix
    phone = re.sub('^(02\d|0800|0\d)', '\g<1> ', phone)
    # Add space after exchange
    phone = re.sub('(\d{3})(\d{3,4})$', '\g<1> \g<2>', phone)
    return phone


if __name__ == '__main__':
    header = ('Name', 'Phone', 'Address', 'Latitude', 'Longitude')
    with open('3m-installer-locations.csv', 'wt') as fout:
        writer = csv.writer(fout)
        writer.writerow(header)

        for count, installer in enumerate(installers()):
            if count == 0:
                continue
            location = get_location(installer)
            print(location)
            row = (installer.name, format_phone(installer.phone),
                location.address, location.latitude, location.longitude)
            writer.writerow(row)
