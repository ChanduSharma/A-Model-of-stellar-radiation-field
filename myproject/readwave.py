#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#  
#  Copyright 2017 azreal <azreal@DESKTOP-Q7S0ERU>
 
import writetable as wt
import hipread as hr

from os import path


def readwave(filename):
	'''This function specifically read wavelength.dat file
	   and outputs lookup table for all wavelength in the 
	   wavelength.dat file.'''
	
	wavelength_file = open(filename,"r")
	
	for lines in wavelength_file:
		
		wavelength,hipfile = lines.split()
		
		#print(wavelength+" "+hipfile)
		
		file_path = path.relpath(hipfile)
		
		wt.writetable(float(wavelength))
		
		hr.hip_read(hipfile)

	
	wavelength_file.close()


if __name__ == '__main__' :
	
	readwave("Wavelength.dat")
