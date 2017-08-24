#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  krucuzflux.py
#  
#  Copyright 2017 azreal <azreal@DESKTOP-Q7S0ERU>
import os
import os.path
import math


def krucuz_flux(coloumns,wavelength):
	
	KFD = "KURUCZ_FLUX" #Krucuz Flux Directory
	KFSD = "P00"        #Krucuz Flux Sub directory
	
	spec_type = coloumns[0]
	
	flux_file = os.path.join(os.path.sep,os.getcwd(),KFD,KFSD,coloumns[1])
	
	abs_mag = float(coloumns[2])
	
	wnf = []
	
	file_handle = open(flux_file,'r')
	
	for lines in file_handle:
		wavelen,flux = map(float,lines.split())
		wnf.append([wavelen,flux])
		#print(str(wavelen)+" "+str(flux))
	
	file_handle.close()
	
	dw = math.pow(wavelength,2)
	
	i = 0
	j = 0
	
	for line in wnf:
		dw1 = math.pow(line[0]-wavelength,2)
		
		if dw1 < dw:
			j = i
			dw = dw1
		
		i = i + 1
	
	return wnf[j][1]
