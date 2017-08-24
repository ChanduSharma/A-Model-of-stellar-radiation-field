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
	'''This function takes the name of hip_main.dat and
		return the path of the output file
		Input File: hip_main.dat
		Output File: 
	'''
	HIPPARCOS_CATALOG="hip_main.dat"
	pelimit = 100.0  #Parallax Error limit of d¶/¶ 
	
	hip_handle = open(HIPPARCOS_CATALOG,"r") #Reading hipparcos catalog
	
	
	while True:
        
		starInfo = hip_handle.readline() 
		if not starInfo:
			break
		
		dataList = starInfo.split('|')
		
		dataList = [x.lstrip().rstrip() for x in dataList]
		
		hipNo = int(dataList[1])
		
		rightAscension = dataList[3].split()
		#print(rightAscension)
		RA = int(rightAscension[0]) + int(rightAscension[1])/60 + float(rightAscension[2])/3600
		
		declination = dataList[4].split()
		if int(declination[0]) < 0:
			sn = -1
		#print(declination)
		DEC = int(declination[0]) + sn * int(declination[1])/60 + sn * float(declination[2])/3600
        
        v_mag = float(dataList[5])
        
        rightasc = float(dataList[8])
        dec = float(dataList[9])
        
		parallax_str = dataList[11]
        
		if parallax_str:
			parallax = float(parallax_str)
			distance = 1.0E3/parallax
			#print(hipNo)
		else:
			distance = 1.0E+6

		epstr = dataList[16]
        
		if not epstr:
			errorParallax = 0.0
			#print(str(hipNo)+"e\n")
		else:
			errorParallax = float(dataList[16])
			if math.isclose(errorParallax/parallax,pelimit,rel_tol = 1.0e-01):
				distance = 1.0E6
        
		b_vostr = dataList[37]
		if not b_vostr:
			b_vo = -9.9e+9
		else:
			b_v0 = float(b_vostr)
			
		hd_no = float(dataList[71])
		
		spectral_type_str = dataList[76]
		
		if not spectral_type_str:
			spectral_type = "*****"
			distance = 9.9E+9
		else:
			spectral_type = spectral_type_str
	hip_handle.close()

hip_read("ads.dat")
