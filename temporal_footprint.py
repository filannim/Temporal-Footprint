#!/usr/bin/python
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

import sys

from temporal_footprint.predict import predict as tf_predict

def main():
	input_url = sys.argv[1]
	prediction = tf_predict(input_url)
	result = list(prediction.results)[0]
	start_year = str(int(result.predicted_temporal_frame.start))
	end_year = str(int(result.predicted_temporal_frame.end))
	footprint_prediction = '-'.join([start_year, end_year]) 
	print 'Prediction: ', footprint_prediction
	prediction.plot()

if __name__ == '__main__':
	main()