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

import os
import re
import subprocess

from properties import properties

def get_just_text(raw_text):
	'''
	It takes a Wikipedia raw_text version of a web page and escape all the 
	useless things (such as ref tags, {{..}}, an infoboxes).
	'''
	# Remove tags (eventually in the text)
	tag_name = r'[A-Za-z]+'
	empty_tags = r' *<'+tag_name+'[^>]*?/> *'	# <br />, <img att="" />
	noempty_tags = r' *<'+tag_name+'[^>]*?>.*?</'+tag_name+'> *'
	random_tags = r' *</?'+tag_name+'[^>]*?> *'
	raw_text = re.sub(empty_tags, ' ', raw_text)
	raw_text = re.sub(noempty_tags, ' ', raw_text)
	raw_text = re.sub(random_tags, ' ', raw_text)
	# Remove textual reference symbols
	raw_text = raw_text.replace('^', '')
	#Nobody doesn't like Unicode
	raw_text = unicode(raw_text, errors='ignore').decode('ascii', 'xmlcharrefreplace')
	#Discard some sections
	raw_text = re.sub(r' +(Links to related articles)\n', r'g<1>', raw_text, flags=re.IGNORECASE)

	section_names_to_skip = ('external links','see also','citations',
		'footnotes','notes','references','further reading','sources',
		'contents','bibliography','','','')
	lines = []
	section_name = '__init__'
	for raw_line in raw_text.split('\n'):
		if raw_line:
			if raw_line.startswith(' '):
				if section_name not in section_names_to_skip:
					lines.append(raw_line.strip())
			else:
				section_name = raw_line.lower().strip()
				if section_name == 'links to the related articles':
					break
	lines = ' '.join(lines)
	return {'text': lines}

def wikipedia_text(title, fullURL=False):
	'''It takes in input a wikipedia url and extract all the text in ASCII
   	format.'''
	os.chdir(properties['MAIN_DIR'])
	title = title.decode("unicode-escape")
	if fullURL:
		query = title.split('/')[-1]
		process = subprocess.Popen([properties['WIKIPEDIA2TEXT'], '-l', 'en', query], stdout=subprocess.PIPE)
	else:
		process = subprocess.Popen([properties['WIKIPEDIA2TEXT'], '-l', 'en', title], stdout=subprocess.PIPE)
	wikipedia2text_output, err = process.communicate()
	text = get_just_text(wikipedia2text_output)
	return text
