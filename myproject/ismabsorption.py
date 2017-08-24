#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ismextinction.py
#  
#  Copyright 2017 chandu sharma <chandu@Mithras>

import math

EXTFILECS = r'IS_EXT/crossec0.dat'

def read_cross_section(wavelength):
	
	extinction_file = open(EXTFILECS,'r')
	
	data = extinction_file.read()
	data = data.split('\n')
	
	w1 = math.pow(wavelength,2)
	for lines in data:
		
		if lines:
			ww2,crosssec = lines.split()
			w2 = math.pow( (float(ww2) - wavelength),2)
		
			if w2 <= w1:
				w1 = w2
				cross_section = crosssec
			
	return float(cross_section)


if __name__ == '__main__':
	print(read_cross_section(895))
