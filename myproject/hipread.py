#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Hipread.py
#  
#  Copyright 2017 azreal <azreal@DESKTOP-Q7S0ERU>

import math
import os
import sys

def hip_read(hipfile):
	'''This function takes the file hip_main.dat and
		return the path of the output file
		Input File: hip_main.dat
		Output File: 
	'''
	######################################################
	# First read the lookup file : 'spectype_to_flux.dat'#
	# for calculatint the flux of each star.             #             
	######################################################
	lookup_table_file = open('spectype_to_flux.dat')
	
	lookup_table = dict()
	
	for lines in lookup_table_file:
		
		spectral_type,flux = lines.split('|')

		lookup_table[spectral_type] = flux
	
	lookup_table_file.close()
	
	
	
	HIPPARCOS_CATALOG="hip_main.dat"
	PELIMIT = 100.0  #Parallax Error limit of d¶/¶ 
	
	hip_handle = open(HIPPARCOS_CATALOG,"r") #Reading hipparcos catalog
	
	data_file = open(hipfile,'w')
	
	
	while True:
        
		star_info = hip_handle.readline() 
		if not star_info:
			break
		
		data_list = star_info.split('|')
		
		data_list = [x.lstrip().rstrip() for x in data_list]
		
		hip_no = int(data_list[1])
		
		right_ascension = data_list[3].split()
		#print(rightAscension)
		RA = int(right_ascension[0]) + int(right_ascension[1])/60 + float(right_ascension[2])/3600
		
		declination = data_list[4].split()
		sn = 1
		if int(declination[0]) < 0:
			sn = -1
		#print(declination)
		DEC = int(declination[0]) + sn * int(declination[1])/60 + sn * float(declination[2])/3600
        
		v_mag_str = data_list[5]
		
		if not v_mag_str:
			v_mag = 0.0
		else:
			v_mag = float(v_mag_str)
        
		rightasc_str = data_list[8]
		
		if not rightasc_str:
			right_asc = 0
		else:
			right_asc = float(rightasc_str)
        
		dec_str = data_list[9]
		
		if not dec_str:
			dec = 0.0
		else:
			dec = float(dec_str)
        
		parallax_str = data_list[11]
        
		if not parallax_str:
			parallax = 0.0
			distance = 1.0E+6
		else:
			parallax = float(parallax_str)
			if parallax > 0.0:
				distance = 1.0E3/parallax
			else:
				distance = 1.0E+6
			
		epstr = data_list[16]
		
		
		if not epstr:
			
			errorParallax = 0.0
			#print(str(hipNo)+"e\n")
		else:
			
			errorParallax = float(data_list[16])
			if parallax > 0:
				if errorParallax/parallax > PELIMIT:
					distance = 1.0E6
				
				
		b_vostr = data_list[37]
		
		if not b_vostr:
			b_vo = -9.9e+9
		else:
			b_v0 = float(b_vostr)
		
		hd_no_str = data_list[71]
		if not hd_no_str:
			hd_no = '****'
		else:
			hd_no = int(hd_no_str)
		spectral_type_str = data_list[76]
		
		if not spectral_type_str:
			spectral_type = "*****"
			distance = 9.9E+9
			star_flux = 0
		else:
			spectral_type = spectral_type_str
			star_flux = lookup_table.get(spectral_type,0)
		
		#Writing the data to hipfile for wavelength of investigation.
		
		line_to_be_written = '{0}|{1}|{2}|{3}|{4}\n'.format(hip_no,hd_no,distance,spectral_type,star_flux)
		data_file.write(line_to_be_written)
		
		
	hip_handle.close()
	data_file.close()
	
	
if __name__ == '__main__':
	hip_read('dhsj')
