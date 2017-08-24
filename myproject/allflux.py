#! python3

########################################################################
# Modelling of Interstellar Radiation Field
# Chandra Kant Sharma (Dr. Pavan Chakraborty)
########################################################################
#
# Description: This file reads the file "HIPFILES/hip_wavelength.dat" for 
#               a particular wavelength and a z'th coordinate and 
#               outputs a file 'fluxdensityframe_wavelength|Z's coord.dat'
#               containing flux from all six direction on the XY plane of
#               Z's frame.
#
# 
# INPUT :       HIPFILES/hip_wavelength.dat - Processed file containing
#               hip number,Galactic lattitude,Galactic Longitude,distance
#               ,Flux of star at wavelength specified in the file
#               
#               wavelength - Wavelength of Investigation
#
#               k - The z's coordinate for which the XY plane is to be 
#                   calculated.
#
# OUTPUT FILE:  fluxdensityframe_wavelength|z.dat
#               where z is z's coordinate frame
# 
# Run command: python3 allflux.py
# 
# Last Date Modified : JULY 11 2017
#
########################################################################


import math
import os
import time
from collections import namedtuple
#import ismextinction
#Library containing function for calculating ISM Absorption
#based on cross section of Draine et al.
import ismabsorption


def all_flux(wavelength,hipfile,frame):

    cross_section = ismabsorption.read_cross_section(wavelength) #Reading the ISM Absorption
    
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
    #k = 10
    
    # Flux filename for Z'th XY frame
    for k in range(frame[0],frame[1]):
        flux_file = 'fluxdensityframe_{}.{}.dat'.format(int(wavelength),k)
        flux_file = os.path.join('data',flux_file) 
    
        file_handle = open(flux_file,'w')
    
        # Creating Frames at 100 parsecs grid on the z'th XY plane.
        start_time = time.time()
        for i in range(0,101):
            flux_list = []
            for j in range(0,101):
                
                #Initial Values of flux in all directions             
                flux_x_p = 0
                flux_y_p = 0
                flux_z_p = 0
                flux_x_n = 0
                flux_y_n = 0
                flux_z_n = 0
                
                #Loops start here
                #Reading each line of processed_star_data
                for star in processed_star_data:
                        
                    dx = i*100 - star.x
                    dy = j*100 - star.y
                    dz = k*100 - star.z
                    
                    r =  dx * dx + dy * dy
                    dr2pc = r + dz * dz
                    drpc = math.sqrt(dr2pc) #Distance between star and point
                    
                    r = math.sqrt(r)
                    
                    dr = pcintocm(drpc)
                    
                    d4pir2 = 4.0 * math.pi * (dr * dr) * kexpvalue
                        
                    if dr > 0.0:
                        tau = n * cross_section * dr
                    
                    star_flux = (star.flux / d4pir2) * math.exp(-tau)
                    
                    #Projection of Flux by the star.
                    lat_flux = math.atan2(dy,dx) 
                    lon_flux = math.atan(dz/r)
                    
                    #flux in respective directions
                    flux_x = star_flux * math.cos(lat_flux) * math.cos(lon_flux)
                    flux_y = star_flux * math.cos(lon_flux) * math.sin(lat_flux)
                    flux_z = star_flux * math.sin(lon_flux)
                    
                    #Dividing the flux into six different directions
                    #based on whether the flux is positive or negative.
                    if flux_x >= 0:
                        flux_x_p += flux_x
                    else:
                        flux_x_n += flux_x
                    
                    if flux_y >= 0:
                        flux_y_p += flux_y
                    else:
                        flux_y_n += flux_y
                        
                    if flux_z >= 0:
                        flux_z_p += flux_z
                    else:
                        flux_z_n += flux_z
                        
                flux_list.append('{}|{}|{}|{}|{}|{}'.format(flux_x_p,flux_x_n,flux_y_p,flux_y_n,flux_z_p,flux_z_n))
                
            file_handle.write(' '.join(flux_list) + '\n')
                #flux_matrix[i][j] += star_flux

            #print(flux_matrix[i][j],time.time()-start)
        
        file_handle.close()
        print(time.time()-start_time)
    

#if __name__ == '__main__':
#all_flux(895,'HIPFILES/hip_0895.dat',0)
