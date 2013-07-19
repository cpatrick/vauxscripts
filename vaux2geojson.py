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

from bs4 import BeautifulSoup
import requests


def load_from_csv(filename):
    """Load the csv into a big dictionary in memory.
    """
    with open(filename, 'rb') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            print(json.dumps(row))


def get_questions_and_choices():
    """Scrape the dialect survey site to get the questions and answers.
    """
    base_url = 'http://dialect.redlog.net/staticmaps'
    for i in range(1, 123):
        cur_url = '{}/q_{}.html'.format(base_url, i)
        resp = requests.get(cur_url)
        soup = BeautifulSoup(resp.text)
        cur_text = soup.get_text()
        for line in cur_text.split('\n'):
            if line.startswith('{}.'.format(i)):
                print(line)
            if line.startswith('Choice'):
                print('--{}'.format(line))


def main():
    """Load the specified csv file and convert it to a GeoJSON.
    """
    get_questions_and_choices()
    #dataset = load_from_csv(sys.argv[1])
    #print(dataset)


if __name__ == '__main__':
    main()
