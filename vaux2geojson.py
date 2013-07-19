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
import sys
import os

from bs4 import BeautifulSoup
import requests


def load_from_csv(filename):
    """Load the csv into a big dictionary in memory.
    """
    with open(filename, 'rb') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            print(json.dumps(row))


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
    print(get_questions_and_choices())
    #print("Downloading images")
    #get_char_images()
    #dataset = load_from_csv(sys.argv[1])
    #print(dataset)


if __name__ == '__main__':
    main()
