#!/usr/bin/env python
#######################################################################
#######################################################################
import os
import numpy as np
import time
import math

def dataset_creator(wavelength):
    
    

    main_folder = 'data_set'
    subfolder = 'wavelength' + str(int(wavelength))

    path_to_file = os.path.join(main_folder,subfolder)

    start_time = time.time()
    #cmap = ListedColormap(['r', 'g', 'b'])
    #norm = BoundaryNorm([-1, -0.5, 0.5, 1], cmap.N)
    #tick_spacing = 1
    
    new_dataset_filename = 'new_dataset1.csv'
    dataset_handle = open(new_dataset_filename,'a')
    for z in range(0,101):
        
        flux_frame_file = 'fluxdensityframe_' + str(int(wavelength)) + '.' + str(z) + '.dat'
        flux_frame_file_path = os.path.join(path_to_file,flux_frame_file)
        if not os.path.isfile(flux_frame_file_path):
            continue
        flux_frame = open(flux_frame_file_path,'r')
        
        for x in range(0,101):
            
            total_data = flux_frame.readline()
            flux_list = total_data.split()
            
            for y in range(0,101):
                
                flux_at_xyz = list(map(float,flux_list[x].split('|')))
                flux_in_x_direction = flux_at_xyz[0] - flux_at_xyz[1]
                flux_in_y_direction = flux_at_xyz[2] - flux_at_xyz[3]
                flux_in_z_direction = flux_at_xyz[4] - flux_at_xyz[5]
                
                res = math.sqrt(flux_in_x_direction*flux_in_x_direction + flux_in_y_direction*flux_in_y_direction + flux_in_z_direction*flux_in_z_direction)
               
                #res = math.log10(res)
                data_to_append = (str(x),str(y),str(z),str(wavelength),str(res))
                dataset_handle.write(','.join(data_to_append) + '\n')
        
        flux_frame.close()

    dataset_handle.close()
    #wavelength_l = np.ones(101*101*101) * wavelength
    #flux_grid = flux_grid / np.amax(flux_grid)
    #dist = dist / np.amax(dist) 

    

if __name__ == '__main__':
    file_name = 'dataset.txt'
    
   
    wavelength_file = open(file_name,'r')
    for lines in wavelength_file:
        
        start_time = time.time()
        dataset_creator(float(lines.rstrip('\n')))
        print(time.time()-start_time)
    
    wavelength_file.close()