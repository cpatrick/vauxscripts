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

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='vauxscripts',
    version='0.0.1',
    description='Script(s) for working with the Bert Vaux linguistic survey',
    long_description=readme,
    author='Patrick Reynolds',
    author_email='cpreynolds@gmail.com',
    url='https://github.com/cpatrick/vauxscripts',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
