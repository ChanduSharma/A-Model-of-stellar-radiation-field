#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  allflux.py
#  
#  Copyright 2017 chandu sharma <chandu@Mithras>
import math
import time
from collections import namedtuple
#import ismextinction
import ismabsorption

def all_flux(wavelength,hipfile):

    cross_section = ismabsorption.read_cross_section(wavelength)
    #lam = ismabsorption.read_lambda(wavelength)
    
    star_file = open(hipfile,'r')

    star_data = star_file.read()
    #Reading complete hipfile in list
    star_file.close()
    
    star_data = star_data.split('\n')
    #line containing the kexpvalue
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
            hip_no = data[0].strip()
        
            gal_l = float(data[1].strip())
            gal_b = float(data[2].strip())
            glr = math.radians(gal_l)
            gbr = math.radians(gal_b)
        
            dist = float(data[3].strip())
            x_c = dist * math.cos(gbr) * math.sin(glr)
            y_c = dist * math.cos(gbr) * math.cos(glr)
            z_c = dist * math.sin(gbr)
        
            spec_type = data[4].strip()
            star_flux = float(data[5].strip())
            
            hd_no = data[6].strip()
            
            processed_star_data.append(star(hip_no,spec_type,hd_no,dist,star_flux,x_c,y_c,z_c))
        
            #print(processed_star_data[-1])

    del star_data
    
    pcintocm = lambda x: ( 3.085678E+18 * x )
    
    n = 1.0#Ndensity
    #flux_matrix = [ [0 for i in range(0,200)] for j in range(0,200) ] 
    
    for i in range(0,201):
        for j in range(0,201):
            
            k = 0 #Depending on which frame is being formed              
            flux_x_p = 0
            flux_y_p = 0
            flux_z_p = 0
            flux_x_n = 0
            flux_y_n = 0
            flux_z_n = 0
            start = time.time()
            for star in processed_star_data:
                    
                dx = star.x - i*50
                dy = star.y - j*50
                dz = star.z - k*50
                
                r =  dx * dx + dy * dy
                dr2pc = r + dz * dz
                drpc = math.sqrt(dr2pc)
                r = math.sqrt(r)
                dr = pcintocm(drpc)
                d4pir2 = 4.0 * math.pi * (dr * dr) * kexpvalue
                    
                if dr > 0.0:
                    tau = n * cross_section * dr
                
                star_flux = (star.flux / d4pir2) * math.exp(-tau)
                lat_flux = math.atan2(dy,dx)
                lon_flux = math.atan(dz/r)
                flux_x_p = star_flux * math.cos(lat_flux) * math.cos(lon_flux)
                flux_y_p = star_flux * math.cos(lon_flux) * math.sin(lat_flux)
                flux_z_p = star_flux * math.sin(lon_flux)
                print(flux_x_p,flux_y_p,flux_z_p)
                #flux_matrix[i][j] += star_flux

            #print(flux_matrix[i][j],time.time()-start)

    

if __name__ == '__main__':
    all_flux(895,'data/hip_0895.dat')
