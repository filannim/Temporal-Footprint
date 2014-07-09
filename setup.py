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

import temporal_footprint

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md', 'LICENSE')

# This class is required in order to allow python setup.py test to work
# correctly. The code has been copied by the official py.test website.
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

# Importing setuptools adds some features like "setup.py develop", but
# it's optional so swallow the error if it's not there.
try:
    import setuptools
except ImportError:
    pass

# Current folder
current_folder = os.path.abspath(os.path.dirname(__file__))

distutils.core.setup(
    name="temporal_footprint",
    description="Temporal footprint extractor from Wikipedia pages.",
    long_description=long_description,
    version=temporal_footprint.__version__,
    author="Michele Filannino",
    author_email="filannim@cs.man.ac.uk",
    url="https://github.com/filannim/Temporal-Footprint",
    download_url="https://github.com/filannim/Temporal-Footprint",
    setup_requires = [],
    packages = ['temporal_footprint'],
    include_package_data = True,
    install_requires = ['matplotlib', 'numpy', 'scipy'],
    classifiers=[],
)