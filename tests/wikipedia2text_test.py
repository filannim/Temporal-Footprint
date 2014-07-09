# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
#	Copyright 2014 Michele Filannino
#
#	gnTEAM, School of Computer Science, University of Manchester.
#	All rights reserved. This program and the accompanying materials
#	are made available under the terms of the GNU General Public License.
#	
#	author: Michele Filannino
#	email:  filannim@cs.man.ac.uk
#	
#	For details, see www.cs.man.ac.uk/~filannim/

from temporal_footprint.wikipedia2text import get_just_text
from temporal_footprint.wikipedia2text import wikipedia_text

def test_no_title():
	assert get_just_text('','bla bla') == {'text': ''}

def test_no_raw_text():
	assert get_just_text('a test','') == {'text': ''}