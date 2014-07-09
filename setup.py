# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
#   Copyright 2014 Michele Filannino
#
#   gnTEAM, School of Computer Science, University of Manchester.
#   All rights reserved. This program and the accompanying materials
#   are made available under the terms of the GNU General Public License.
#   
#   author: Michele Filannino
#   email:  filannim@cs.man.ac.uk
#   
#   For details, see www.cs.man.ac.uk/~filannim/

import distutils.core
import os

# Importing setuptools adds some features like "setup.py develop", but
# it's optional so swallow the error if it's not there.
try:
    import setuptools
except ImportError:
    pass

distutils.core.setup(
    name="temporal_footprint",
    description="Temporal footprint extractor from Wikipedia pages.",
    long_description="""Temporal footprint is a Python based piece of software, 
    which predicts the temporal footprint of a concept by analysing the 
    textual content of its encyclopeadiac description.""",
    version="1.0",
    author="Michele Filannino",
    author_email="filannim@cs.man.ac.uk",
    url="https://github.com/filannim/Temporal-Footprint",
    download_url="https://github.com/filannim/Temporal-Footprint",
    setup_requires = [],
    packages = ['temporal_footprint'],
    include_package_data = True,
    install_requires = [],
    classifiers=[],
)