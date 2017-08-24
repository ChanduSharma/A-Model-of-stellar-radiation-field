#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#  
#  Copyright 2017 azreal <azreal@DESKTOP-Q7S0ERU>
 
import writetable
from os import path

def readwave(filename):
	datafile = open(filename,"r")
	for lines in datafile:
		wavelength,hipfile = lines.split()
		#print(wavelength+" "+hipfile)
		file_path = path.relpath(hipfile)
		writetable.writetable(float(wavelength),file_path)
	datafile.close()


readwave("Wavelength.dat")
