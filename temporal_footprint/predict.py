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

from __future__ import division

from collections import namedtuple
from collections import defaultdict
from datetime import date as Date
import re
import sys
import os
import random
import subprocess
import tempfile
import time

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import pylab
from scipy.stats import norm

from wikipedia2text import wikipedia_text
from properties import properties

Gaussian = namedtuple('Gaussian', ['mu', 'sigma'])
TemporalFrame = namedtuple('TemporalFrame', ['start', 'end'])
TemporalFrameResult = namedtuple('TemporalFrameResult', ['source', 'dates', 'gaussian_curve', 'optimised_gaussian_curve', 'predicted_temporal_frame', 'error'])

def HeidelTime_annotate(text):
	with tempfile.NamedTemporaryFile('w+t', delete=False) as f:
		name = f.name
		f.write(text)
	os.chdir(properties['HEIDELTIME_DIR'])
	process = subprocess.Popen(['java', '-jar', 'de.unihd.dbs.heideltime.standalone.jar', name, '-l', 'ENGLISH', '-t', 'NARRATIVES'], stdout=subprocess.PIPE)
	output, err = process.communicate()
	os.remove(name)
	os.chdir(properties['MAIN_DIR'])
	return str(output)

class Timer(object):
	def __init__(self, name=None):
		self.name = name

	def __enter__(self):
		self.tstart = time.time()

	def __exit__(self, type, value, traceback):
		if self.name:
			print '%s' % self.name
		print '(%.4fs)' % (time.time() - self.tstart)

class WikipediaPage(object):

	def __init__(self, title, text=None, HeidelTime_text=None, gold_start=None, gold_end=None):
		self.title = title.strip()
		self.text = re.sub(r'[<>]', '', wikipedia_text(title.strip(), fullURL=True)['text'])
		self.HeidelTime_text = HeidelTime_annotate(self.text)
		self.word_count = len(self.text.split())
		self.DDDD_density = len(re.findall(r'[12][\d]{3}', self.text)) / len(self.text.split())
		self.DDDD_sequences = len(re.findall(r'[12][\d]{3}', self.text))
		self.temporal_frame = TemporalFrame(0.0, 0.0)
		if gold_start and gold_end:
			self.temporal_frame = TemporalFrame(float(gold_start), float(gold_end))

	def __str__(self):
		text = 'TEXT:' + self.text[0:100] + '\n'
		text += '# DDDD sequences:' + str(len(re.findall(r'[12][\d]{3}', self.text))) + '\n'
		text += '# characters    :', str(len(self.text)) + '\n'
		text += '# words         :', str(len(self.text.split())) + '\n'
		text += '# DDDD density  :', str(len(re.findall(r'[12][\d]{3}', self.text)) / len(self.text.split()))
		return text
		

class Predictor(object):

	def __init__(self, Person, outlier_ray=7.9, gaussian_a=1.6, gaussian_b=-10):
		self.person = Person
		self.outlier_ray = outlier_ray
		self.gaussian_a = gaussian_a
		self.gaussian_b = gaussian_b
		self.extraction_functions = (self.__extract_DDDD_dates, self.__extract_HeidelTime_dates)
		#self.extraction_functions = (self.__extract_Baseline_dates, self.__extract_BaselineFiltered_dates, self.__extract_DDDD_dates, self.__extract_HeidelTime_dates)
		self.results = self.__compute()

	def __compute(self):
		results = []
		for function in self.extraction_functions:
			source = re.findall(r'extract_([A-Za-z]+)_dates', str(function))[0]
			results.append(self.__predict(source, function, self.outlier_ray, self.gaussian_a, self.gaussian_b))
		return results

	def __predict(self, source, function, outlier_ray, gaussian_a=1., gaussian_b=0.):
		if source == 'Baseline':
			dates = function(self.person.text)
			predicted_temporal_frame = TemporalFrame(np.amin(dates), np.amax(dates))
			error = self.__compute_error(self.person.temporal_frame, predicted_temporal_frame)
			return TemporalFrameResult(source, dates, Gaussian(0,1), Gaussian(0,1), predicted_temporal_frame, error)
		if source == 'BaselineFiltered':
			try:
				dates = function(self.person.text)
				dates_filtered = self.__reject_outliers(dates, outlier_ray)
				predicted_temporal_frame = TemporalFrame(np.amin(dates_filtered), np.amax(dates_filtered))
				error = self.__compute_error(self.person.temporal_frame, predicted_temporal_frame)
				return TemporalFrameResult(source, dates, Gaussian(0,1), Gaussian(0,1), predicted_temporal_frame, error)
			except ValueError:
				return TemporalFrameResult(source, dates, Gaussian(0,1), Gaussian(0,1), TemporalFrame(1000, Date.today().year), 1.0)
		elif source == 'DDDD':
			dates = function(self.person.text)
		elif source == 'HeidelTime':
			dates = function(self.person.HeidelTime_text)
		else:
			raise Exception('Function ' + source + 'not found!')	
		dates_filtered = self.__reject_outliers(dates, outlier_ray)
		gaussian_curve = Gaussian._make(self.__normal_fit(dates_filtered))
		optimised_gaussian_curve = Gaussian(gaussian_curve.mu+gaussian_b, gaussian_curve.sigma*gaussian_a)
		predicted_temporal_frame = TemporalFrame(optimised_gaussian_curve.mu - optimised_gaussian_curve.sigma, optimised_gaussian_curve.mu + optimised_gaussian_curve.sigma)
		error = self.__compute_error(self.person.temporal_frame, predicted_temporal_frame)
		return TemporalFrameResult(source, dates, gaussian_curve, optimised_gaussian_curve, predicted_temporal_frame, error)

	def __reject_outliers(self, dates, outlier_ray = 2.):
	    d = np.abs(dates - np.median(dates))
	    mdev = np.median(d)
	    s = d/mdev if mdev else 0
	    try:
	    	r = dates[s<outlier_ray]
	    except IndexError:
	    	r = np.array([])
	    if type(r) != np.ndarray:
	    	return np.array([r])
	    else:
	    	return r

	def __normal_fit(self, dates):
		y = map(float, dates)	#y = [float(d) for d in dates]
		return norm.fit(y)	# returns (mu, sigma)

	def __compute_error(self, gold_frame, predicted_frame):
		upper_bound = np.amax((gold_frame.start, gold_frame.end, predicted_frame.start, predicted_frame.end))	#can be more elegantly rewritten
		lower_bound = np.amin((gold_frame.start, gold_frame.end, predicted_frame.start, predicted_frame.end))	#can be more elegantly rewritten
		union_frame = (upper_bound - lower_bound) + 1
		try:
			overlap = len(set(range(int(gold_frame.start), int(gold_frame.end)+1)) & set(range(int(predicted_frame.start), int(predicted_frame.end)+1)))#can I write something more NumPy-ish?
			return 1 - (overlap/union_frame)
		except ValueError:
			return 1

	def __extract_Baseline_dates(self, text):
		result = np.array([float(y) for y in re.findall(r'[12][\d]{3}', text)]) 
		if len(result)<2:
			return np.array([1000,2014])
		else:
			return result

	def __extract_BaselineFiltered_dates(self, text):
		result = np.array([float(y) for y in re.findall(r'[12][\d]{3}', text)])
		if len(result)<2:
			return np.array([1000,2014])
		else:
			return result

	def __extract_DDDD_dates(self, text):
		result = np.array([float(y) for y in re.findall(r'[12][\d]{3}', text)])
		if len(result)<2:
			return np.array([1000,2014])
		else:
			return result

	def __extract_HeidelTime_dates(self, text):
		try:
			dates = re.findall('value=\"([^\"]+)\"', text)
			dates = [e[0:4] for e in dates if len(e)==4]
			dates = [int(y) for y in dates if y.isdigit()]
			return np.array(dates)
		except:
			return np.array([1000,2014])

	def plot(self):
		plt.close('all')
		fig, (axarr) = plt.subplots(len(self.extraction_functions))
		for id, result in enumerate(self.results):
			try:
				n, bins, patches = axarr[id].hist(result.dates, 100, normed=1, facecolor='blue', alpha=0.75)
				axarr[id].plot(bins, mlab.normpdf(bins, result.gaussian_curve.mu, result.gaussian_curve.sigma), 'r--', linewidth=2)
				gold = axarr[id].axvspan(self.person.temporal_frame.start, self.person.temporal_frame.end, color='blue', alpha=0.3)
				prediction = axarr[id].axvspan(result.predicted_temporal_frame.start, result.predicted_temporal_frame.end, color='red', alpha=0.3)
				next_year = int(Date.today().year+1)
				if id==0:
					axarr[0].set_title(self.person.title.replace('_', ' ') + ' (' + str(int(self.person.temporal_frame.start)) + '-' + str(int(self.person.temporal_frame.end)) + ')\n' + result.source + ' prediction [' + str(int(result.predicted_temporal_frame.start)) + '-' + str(int(result.predicted_temporal_frame.end)) + '], E = ' + str(np.around(result.error, 4)))
				else:
					axarr[id].set_title(result.source + ' prediction [' + str(int(result.predicted_temporal_frame.start)) + '-' + str(int(result.predicted_temporal_frame.end)) + '], E = ' + str(np.around(result.error, 4)))
				axarr[id].set_ylabel('freq')
				axarr[id].yaxis.set_ticklabels([])
				axarr[id].set_xticks(np.arange(1000,next_year, next_year/50))
				axarr[id].set_xlim(1000,next_year)
				print result.source, str(np.around(result.error, 4))
			except:
				continue
		axarr[id].set_xlabel('Years (0 - ' + str(next_year) + ')')
		plt.show(block=False)
		#plt.savefig('pictures/' + self.person.title + '.png', dpi=300)
		raw_input('Press Any Key To Exit')

def predict(title, start=None, end=None):
	prediction = Predictor(WikipediaPage(title, gold_start=start, gold_end=end))
	return prediction