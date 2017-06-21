#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  allflux.py
#  
#  Copyright 2017 chandu sharma <chandu@Mithras>

def all_flux(wavelength,hipfile):

    #cross_section = read_cross_section(wavelength)
    #lam = read_lambda(wavelength)
    
    star_file = open(hipfile,'r')

    star_data = star_file.read()
    #Reading complete hipfile in list
    star_file.close()
    
    star_data = star_data.split('\n')
    #line containing the kexpvalue
    skexpvalue,*rest = star_data[1].split()

    kexpvalue = float(skexpvalue)
    print(kexpvalue)

    ##############################
    #Loop of hipfile starts here.#
    ##############################
    for line in star_data[4:]:
        
        data = line.split('|')
        hip_no = data[0].strip()
        gal_l = float(data[1])
        gal_b = float(data[2])
        distance = float(data[3])
        spectral_type = data[4].strip()
        star_flux = float(data[5])
        hd_no = data[6].strip()
        #print(line)
        



    

if __name__ == '__main__':
    all_flux(895,'data/hip_0895.dat')
