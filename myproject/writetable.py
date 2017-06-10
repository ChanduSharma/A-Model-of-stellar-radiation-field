#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  writetable.py
#  
#  Copyright 2017 azreal <azreal@DESKTOP-Q7S0ERU>

import krucuzflux as kf


def writetable(wavelength):
	
	spectral_to_krucuz = open("MKSpDATA/MKSpType00m.in","r")
	data = spectral_to_krucuz.readlines()
	spectral_to_krucuz.close()
	
	# The magic number 4 is used as the file contains
	# initial lines as comments or info about the file.
	JUMP_CONTENTS = 4
	
	lines_to_read = int(data[0].strip()) + JUMP_CONTENTS
	
	#print(total_lines_to_read)
	#Spectral type and relative krucuz file name for known type.
	
	data = data[JUMP_CONTENTS:lines_to_read]
	
	dict_file = open('spectype_to_flux.dat','w')
	
	for lines in data:
		#print(lines)
		
		spectral_type,krucuz_flux_file,v_mag = lines.split('|')[:3]
		
		#print(krucuz_flux_file)
		
		normalized_flux = kf.krucuz_flux(krucuz_flux_file.strip(),wavelength)
		#print(normalized_flux)
		x = '{}|{}\n'.format(spectral_type.strip(),normalized_flux)
		
		print(x)
		
		dict_file.write(x)
		
	dict_file.close()
		
if __name__  == '__main__':
	writetable(895.0,'sdnsjs')
