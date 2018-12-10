#!/usr/bin/python
# -*- coding: utf-8 -*-
from SmoldynManipulator import *

import math

hex_manipulator = Manipulator.from_file("template_hexagon_enzymes.txt", True)
control_manipulator = Manipulator.from_file("template_control.txt", True)
len_linker = 7
hex_rib    = 21							# width of the hexagon's faces

#Define desired hexagon dimensions
for inter_enz_dist in range(10, 90+1, 10):
	interenzyme_distance = inter_enz_dist
	hex_len = 50+interenzyme_distance		# depth of the hexagon

	#dynamic
	hex_wing = hex_rib/2.0 					# want perfecte hexagon
	hex_width = hex_wing*2.0 + hex_rib
	alpha = math.asin(hex_wing/ hex_rib)
	half_height = math.cos(alpha)*hex_rib
	hex_height = half_height*2.0
	linker_x = len_linker*math.cos(alpha)	# x-component of slanted linker dna
	linker_y = len_linker*math.sin(alpha)	# Y-component of slanted linker dnaS
	#get dimensions and centre coordinates of the simulation box
	centre = hex_manipulator.center()
	hexagon = Polygon("hexagon", centre, 6, hex_rib, hex_len, n_segments = 2)

	hexagon.thickness(1)
	hexagon.color("both", 1, 0, 1, 0.5) # magenta is love, magenta is life!
	hexagon.set_property("action", "both all reflect")

	#create planes in hex for spawning enzymes
	GOx_plane_coords = (centre[0]-hex_width/2.0, centre[1]-hex_height/2.0, centre[2]+interenzyme_distance/2.0) 
	GOx_plane = "panel rect +2 {} {} {} gox_plane".format(" ".join(map(str, GOx_plane_coords)), hex_width, hex_height)

	HRP_plane_coords = (centre[0]-hex_width/2.0, centre[1]-hex_height/2.0, centre[2]-interenzyme_distance/2.0) 
	HRP_plane = "panel rect +2 {} {} {} hrp_plane".format(" ".join(map(str, HRP_plane_coords)), hex_width, hex_height)

	#place enzymes on planes
	enzyme_placement = []
	planes = [("E1", "gox_plane", GOx_plane_coords),
				("E2", "hrp_plane", HRP_plane_coords)]
	dx = (hex_wing/2.0)+linker_x
	dy = (hex_height/4.0+linker_y)
	for p in planes:
		enzyme_name = p[0]
		plane_name = p[1]
		c = p[2]
		enzyme_placement.append("surface_mol 1 {}(front) enzyme_planes r {} {} {} {}".format(enzyme_name, plane_name, c[0]+dx, c[1] + dy, c[2]))
		enzyme_placement.append("surface_mol 1 {}(front) enzyme_planes r {} {} {} {}".format(enzyme_name, plane_name, c[0]+hex_width-dx, c[1] + dy, c[2]))
		enzyme_placement.append("surface_mol 1 {}(front) enzyme_planes r {} {} {} {}".format(enzyme_name, plane_name, c[0]+(hex_width/2.0), c[1]+(hex_height-len_linker), c[2]))
	
	# calculate distances between the enzymes in the hexagon (on linkers)
	opposite 	= hex_height - len_linker - dy	
	dw 			= (hex_width - 2*dx)				# horizontale afstand
	adjacent 	= 1.0/2.0*dw
	hypothenuse = (adjacent**2+opposite**2)**.5		# schuine afstand
	
	#inserts the hexagon in "reactionkinetics.txt" where "#TAG: hexagonnetje" is present
	hex_manipulator.insert("hexagonnetje", hexagon)
	hex_manipulator.insert("GOx_plane", GOx_plane)
	hex_manipulator.insert("HRP_plane", HRP_plane)
	hex_manipulator.insert("enzyme_placement", enzyme_placement)
	hex_manipulator.set_output_filename("hexagon\\hexagon_scaffold_"+str(interenzyme_distance)+".txt").save()
	
	# create the control groups
	control_manipulator.insert("makeScaffold", None)
	control_manipulator.set_output_filename("control_plane\\control_"+str(interenzyme_distance)+".txt")
	control_manipulator.insert("IED", interenzyme_distance)
	control_manipulator.insert("len_linker", len_linker)
	control_manipulator.insert("substrate_mol", 4800)
	control_manipulator.insert("neighbour_distance", dw)
	control_manipulator.save()
	control_manipulator.set_output_filename("control_free\\control_"+str(interenzyme_distance)+".txt")
	control_manipulator.insert("makeScaffold", "makeScaffold")
	control_manipulator.save()
	

