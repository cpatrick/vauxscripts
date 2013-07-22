#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#
# Library:   vauxscripts
#
# Copyright 2013 Patrick Reynolds
#
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 ( the "License" );
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
###############################################################################

import json
import csv
import os
import sys

from clint import args
from bs4 import BeautifulSoup
import requests


def generate_feature(lon, lat, props):
    """Generate a feature to drop in a GeoJSON feature collection.
    """
    feature = dict()
    feature['type'] = 'Feature',
    feature['geometry'] = dict()
    feature['geometry']['type'] = 'Point'
    feature['geometry']['coordinates'] = [lon, lat]
    feature['properties'] = dict(props)
    return feature


def load_from_csv(filename):
    """Load the csv into a big dictionary in memory.
    """
    feature_collection = dict()
    feature_collection['type'] = 'FeatureCollection'
    feature_collection['features'] = list()
    with open(filename, 'rb') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        new_row = dict()
        for row in csv_reader:
            for k, v in row.iteritems():
                new_row[k.strip(' "')] = v.strip(' "')
            base_url = 'http://maps.googleapis.com/maps/api/geocode/json?'
            url = '{}address={}&sensor=false'.format(base_url, new_row['ZIP'])
            resp = requests.get(url)
            json_location = resp.json()
            if len(json_location['results']) >= 1:
                geoloc = json_location['results'][0]['geometry']['location']
            else:
                geoloc = {'lng': 0, 'lat': 0}
                print(json_location)
            lon = geoloc['lng']
            lat = geoloc['lat']
            feature_collection = generate_feature(lon, lat, new_row)
    return feature_collection


def get_char_images():
    """Pull down images from the dialect survey site."""
    base_url = 'http://dialect.redlog.net/staticmaps/images/'
    target_dir = 'images'

    try:
        os.mkdir(target_dir)
    except OSError:
        print('The directory, "{}," already exists.'.format(target_dir))

    resp = requests.get(base_url)
    soup = BeautifulSoup(resp.text)
    for link in soup.find_all('a'):
        img_target = link.get('href')
        if img_target.endswith('.gif'):
            resp = requests.get(base_url + img_target)
            with open(os.path.join(target_dir, img_target), 'wb') as output:
                output.write(resp.content)


def get_questions_and_choices():
    """Scrape the dialect survey site to get the questions and answers.
    """
    questions = dict()
    base_url = 'http://dialect.redlog.net/staticmaps'
    for i in range(1, 123):
        cur_url = '{}/q_{}.html'.format(base_url, i)
        cur_index = 'Q{0:03d}'.format(i)
        questions[cur_index] = dict()
        resp = requests.get(cur_url)
        soup = BeautifulSoup(resp.text)
        cur_text = soup.get_text()

        # Get the question on the page
        for line in cur_text.split('\n'):
            if line.startswith('{}.'.format(i)):
                cur_question = ''.join(line.split('.')[1:])
                cur_question = cur_question.replace('\r', '')
                questions[cur_index]['question'] = cur_question.strip()

        # Get the answers on the page
        answer_index = 0
        for line in soup.select('p > b'):
            if str(line).startswith('<b>Choice'):
                out = ''.join([str(tag) for tag in line.contents])
                ans = ''.join(out.split(':')[1:])
                ans = ans.replace('\r', '')
                questions[cur_index][answer_index] = ans.strip()
                answer_index += 1

    return questions


def main():
    """Load the specified csv file and convert it to a GeoJSON.
    """
    arguments = dict(args.grouped)

    command = args.get(0)

    if command == 'questions':
        data = json.dumps(get_questions_and_choices(), indent=2)
        if '-o' in arguments:
            with open(arguments['-o'][0], 'wb') as outfile:
                outfile.write(data)
        elif '--output' in arguments:
            with open(arguments['--output'][0], 'wb') as outfile:
                outfile.write(data)
        else:
            print(data)
    elif command == 'images':
        get_char_images()
    elif command == 'locations':
        if '-i' in arguments:
            infile = arguments['-i'][0]
        elif '--input' in arguments:
            infile = arguments['--input'][0]
        else:
            print('Set input csv with "-i" or "--input."')
            sys.exit(-1)

        data = json.dumps(load_from_csv(infile), indent=2)
        if '-o' in arguments:
            with open(arguments['-o'][0], 'wb') as outfile:
                outfile.write(data)
        elif '--output' in arguments:
            with open(arguments['--output'][0], 'wb') as outfile:
                outfile.write(data)
        else:
            print(data)
    else:
        print('Unrecognized command.')

if __name__ == '__main__':
    main()
