#!/usr/bin/env python
#######################################################################
#######################################################################
import os
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import cm
import numpy as np
import time
import math

def plotting_flux(wavelength):
	
	

	main_folder = 'data_set'
	subfolder = 'wavelength' + str(int(wavelength))

	path_to_file = os.path.join(main_folder,subfolder)

	flux_grid = np.zeros(101*101*101)
	start_time = time.time()
	#cmap = ListedColormap(['r', 'g', 'b'])
	#norm = BoundaryNorm([-1, -0.5, 0.5, 1], cmap.N)
	#tick_spacing = 1
	dist = np.zeros(101*101*101)
	
	i = 0
	for z in range(0,101):
		
		flux_frame_file = 'fluxdensityframe_' + str(int(wavelength)) + '.' + str(z) + '.dat'
		flux_frame_file_path = os.path.join(path_to_file,flux_frame_file)
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
				distance = math.sqrt(x*x + y*y + z*z)
				dist[i] = distance
				flux_grid[i] = math.log10(res)
				i += 1
		
		flux_frame.close()


	#wavelength_l = np.ones(101*101*101) * wavelength
	#flux_grid = flux_grid / np.amax(flux_grid)
	#dist = dist / np.amax(dist) 
	return dist,flux_grid

	

if __name__ == '__main__':
	file_name = 'dataset.txt'
	
	fig = plt.figure()
	ax = fig.gca(projection='3d')
	#tick_spacing = 5
	
	wavelength_file = open(file_name,'r')
	for lines in wavelength_file:
		
		start_time = time.time()
		x,y = plotting_flux(float(lines.rstrip('\n')))

		ax.scatter(x,np.ones(x.size)*float(lines.rstrip('\n')),y)
		
		print(time.time()-start_time)
	
	wavelength_file.close()
	#plt.xlabel('Distance (in parsecs)')
	#plt.ylabel('flux')
	ax.set_xlabel('Distance')
	ax.set_ylabel('Wavelength')
	ax.set_zlabel('flux normalized')
	plt.savefig('dataset1.png',format='png')
				
	#ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
	#ax.yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
	#ax.zaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
	