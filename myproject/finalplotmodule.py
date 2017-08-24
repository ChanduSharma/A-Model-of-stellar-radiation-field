#! python3

import math
import os
import time
from collections import namedtuple
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.modeling import projections
import numpy as np
#import ismextinction
#Library containing function for calculating ISM Absorption
#based on cross section of Draine et al.
import ismabsorption

def plotfun(wavelength,hipfile):


	cross_section = ismabsorption.read_cross_section(wavelength) #Reading the ISM Absorption
	GL1 = 0
	GL2 = 360
	GB1 = -90
	GB2 = 90
	DL = 1
	DB = 1

	NL = math.floor( (GL2 - GL1) / DL + 1.5)
	NB = math.floor( (GB2 - GB1) / DB + 1.5)

	flux_mat = np.zeros((NL-1,NB-1))
	
	#lam = ismextinction.read_lambda(wavelength)
	
	# Reading the processed hipfile.
	star_file = open(hipfile,'r')

	star_data = star_file.read() #Reading complete hipfile in list
	
	star_file.close() 
	
	# Closed the hipfile 
	
	star_data = star_data.split('\n') #creating a list of lines from the hipfile data
	
	#First line contains the kexpvalue
	skexpvalue,*rest = star_data[1].split()

	kexpvalue = float(skexpvalue)
	#print(kexpvalue)
	fldpts = namedtuple('fieldpts','x y z')

	testing_fieldpt = fldpts(0.0,0.0,0.0)
	
	star = namedtuple('star','hip_number spectral_type hd_number distance_from_origin flux x y z')
	
	##############################
	#Loop of hipfile starts here.#
	##############################
	processed_star_data = []
	for line in star_data[4:]:
		
		data = line.split('|')
		if line:
			hip_no = data[0].strip() # Hipparcos Catalog number
		
			gal_lattitude = float(data[1].strip()) #Galactic Lattitude (in degrees)
			gal_longitude = float(data[2].strip()) #Galactic Longitude (in degrees)

			
			glr = math.radians(gal_lattitude)
			gbr = math.radians(gal_longitude)
		
			dist = float(data[3].strip()) # Distance of star (in parsecs)
			
			x_c = dist * math.cos(gbr) * math.sin(glr)
			y_c = dist * math.cos(gbr) * math.cos(glr)
			z_c = dist * math.sin(gbr)
		
			spec_type = data[4].strip()
			star_flux = float(data[5].strip())

			
			hd_no = data[6].strip()
			
			processed_star_data.append(star(hip_no,spec_type,hd_no,dist,star_flux,x_c,y_c,z_c))
		
			#print(processed_star_data[-1])

	del star_data
	
	pcintocm = lambda x: ( 3.085678E+18 * x ) #Function to change Parsecs to CM(CentiMeter)
	
	n = 0.22  #Ndensity
	

	for star in processed_star_data:
		
		dx =  star.x - testing_fieldpt.x
		dy =  star.y - testing_fieldpt.y
		dz =  star.z - testing_fieldpt.z
					  
		dr2pc = dx * dx + dy * dy + dz * dz
		drpc = math.sqrt(dr2pc)  #Distance between star and point

					
		dr = pcintocm(drpc) #Converting parsecs into centimetres.
					
		d4pir2 = 4.0 * math.pi * (dr * dr) * kexpvalue

		gbr = math.asin(dz/drpc)
		glr = math.atan2(dx,dy)

		gld = math.degrees(glr)
		gbd = math.degrees(gbr)
		scale = 1
		RHO = math.acos(math.cos(gbr) * math.cos(glr/2))
		THETA = math.asin(math.cos(gbr) * math.sin(glr/2)/math.sin(RHO))

		x = -4 * scale * (180/math.pi) * math.sin(RHO/2) * math.sin(THETA)

		if gbd < 0:
			y = 2 * scale * (180/math.pi) * math.sin(RHO/2) * math.cos(THETA)
		else:
			y = -2 * scale * (180/math.pi) * math.sin(RHO/2) * math.cos(THETA)
		


		if dr > 0.0:
			tau = n * cross_section * dr
			star_flux = (star.flux / d4pir2) * math.exp(-tau)
			flux_mat[int(x),int(y)] += star_flux
		else:
			flux_mat[int(x),int(y)] += star.flux
		
					
		#Projection of Flux by the star.

		#print(star_flux,math.degrees(gbr),math.degrees(glr))
					
		#flux in respective directions
		#flux_x = star_flux * math.cos(lat_flux) * math.cos(lon_flux)
		#flux_y = star_flux * math.cos(lon_flux) * math.sin(lat_flux)
		#flux_z = star_flux * math.sin(lon_flux)
					
		#Dividing the flux into six different directions
		#based on whether the flux is positive or negative.

	for (x,y),val in np.ndenumerate(flux_mat):
		if val > -1.0:
			datamax = val
		else:
			flux_mat[x,y] = -1
		
	hdu = fits.PrimaryHDU()
	hdu.data = flux_mat
	hdu.writeto('flux2365.fits')
	
	#plt.show()


if __name__ == '__main__':
	plotfun(2365.0,'hip_2365.dat')