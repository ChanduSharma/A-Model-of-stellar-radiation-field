#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  krucuzflux.py
#  
#  Copyright 2017 azreal <azreal@DESKTOP-Q7S0ERU>
import os
import os.path
import math


def krucuz_flux(krucuz_flux_file,wavelength):
	
	KFD = "KURUCZ_FLUX"    #Krucuz Flux Directory
	KFSD = "P00"           #Krucuz Flux Sub directory
	
		
	flux_file = os.path.join(os.path.sep,os.getcwd(),KFD,KFSD,krucuz_flux_file)
	
	wnf = []
	
	wavelength_of_interest = float(wavelength)
	
	file_handle = open(flux_file,'r')
	
	for lines in file_handle:
		
		wavelen,flux = lines.split()
		wavelen = float(wavelen)
		
		wnf.append((wavelen,flux))
		
		#print(str(wavelen)+" "+str(flux))
	
	file_handle.close()
	
	dw = math.pow(wavelength_of_interest,2)
	
	i = 0
	j = 0
	
	for line in wnf:
		dw1 = math.pow(line[0]-wavelength_of_interest,2)
		
		if dw1 < dw:
			j = i
			dw = dw1
		
		i = i + 1
	
	return wnf[j][1]

if __name__ == '__main__':
	print(krucuz_flux('t09500g40p00.dat',895.0))
