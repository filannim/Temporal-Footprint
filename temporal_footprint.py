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

import argparse
import sys

from temporal_footprint.predict import predict as tf_predict

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("URL", help="full Wikipedia page address of the page you want to analyse.", type=str)
	parser.add_argument("-s", "--start", help="expected date of start", type=int)
	parser.add_argument("-e", "--end", help="expected date of end", type=int)
	parser.add_argument("-p", "--plot", help="plot the result.", action="store_true")
	parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
	args = parser.parse_args()

	
	prediction = tf_predict(args.URL, start=args.start, end=args.end)

	if args.verbose:
		print prediction
	else:
		result = prediction.results[0]
		start_year = str(int(result.predicted_temporal_frame.start))
		end_year = str(int(result.predicted_temporal_frame.end))
		footprint_prediction = '-'.join([start_year, end_year]) 
		print 'Prediction: ', footprint_prediction
	if args.plot:
		prediction.plot()

if __name__ == '__main__':
	main()