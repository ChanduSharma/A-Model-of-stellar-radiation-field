#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  writetable.py
#  
#  Copyright 2017 azreal <azreal@DESKTOP-Q7S0ERU>

import krucuzflux



def writetable(wavelength,hipfile):
	
	new_file = open("MKSpDATA/MKSpType00m.in","r")
	data = new_file.readlines()
	new_file.close()
	
	lines_to_read = int(data[0].strip()) + 4
	#print(total_lines_to_read)
	data = data[4:lines_to_read]
	star_list = []
	
	for lines in data:
		#print(lines)
		coloumns = lines.split('|')[:3]
		st_coloumns = [x.lstrip().rstrip() for x in coloumns]
		#print(st_coloumns)
		flux = krucuzflux.krucuz_flux(st_coloumns,wavelength)
		x = st_coloumns[0] +' '+ str(flux) + '\n'
		#print(x)
		star_list.append(x)
		
