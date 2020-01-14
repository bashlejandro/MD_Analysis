"""El siguiente script es un intento para producir una gráfica que muestre la salida de RMSF (Root mean square deviation) de una dinámica molecular realizada con NAMD
SIGO TENIENDO PROBLEMAS AYUDA POR FAVOR



"""

import numpy as np
import csv
import os
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file
sysname=input("Enter system name of your simulation: (e.g. Folate-reductase-Methotrexate: \n")
basedyn=input("Please enter your files basename(If your file is named Base1.dcd or Base1.coor.dcd, only write Base1: \n)")
dynextension=input("Please enter your extension (.dcd, .xyz, etc) \n")
steps=input("If your simulation is too long, please enter steps for reading big trajectories (recommended 10): \n")
print("Now select your fragment of system (based on VMD options of selection): \n ")
sistema=input("protein, chain, name CA, resid: \n")

f = open("RMSF.tcl", "w")
f.write("""
	#The next lines are for listing and selecting trajectory files and selecting system selection for calculation
	#This one list files in the current folder
	set files [glob *"""+dynextension+"""]
	#This line makes a list of all files
	set list [lsort $files]
	#With this command, we order to charge in memory every file in order and with the steps required.
	foreach i $list {
	mol addfile "$i" first 0 step """+steps+""" waitfor all
	}
	#This command writes a file with extension *.csv, it can be read with xmgrace or python.
	set outfile [open """+basedyn+"""_RMSF.csv w]
	#Setting number of frames
	set nf [molinfo top get numframes]
	set frame0 [atomselect top """+sistema+""" frame 0]
	#selecion of atoms, preferably use residues
	set sel [atomselect top """+sistema+"""]
	

	#Now is time for RMSF calculation loop 
	#modified from https://github.com/kippjohnson/UChicago/blob/master/RMSF.tcl

	# Set output name below (in quotes)
	#set outfile [open "2LMN-40-dE22.dat" w]
	#set sel [atomselect top all]
	#set sel0 [$sel num]
	#set sel [atomselect top "resid 1 to $sel0 and name CA"]
	# Change the number below to change steps that are skipped 
	# When calculating RMSF (suggest 5 or 10) {equiv. to "stride"}
	set stepsize 10
	#originally the above stepsize is 10
	#set nframes [molinfo top get numframes]
	set nframes2 [expr $nf - 1]
	# Comment out below line if you do not want a header in output
	puts $outfile "#Residue \t RMSF"

	for {set i 0} {$i < [$sel num]} {incr i} { 
     	set rmsf [measure rmsf $sel first 1 last $nframes2 step $stepsize] 
     	puts $outfile "[expr {$i+1}] \t [lindex $rmsf $i]" 
	} 
	close $outfile
	exit"""

	)
f.close()

os.system("mkdir -m 777 var/www/html/python_graph")

os.system("vmd -dispdev text "+basedyn+".a.0.psf -e RMSF.tcl")


p1 = figure()
p1.grid.grid_line_alpha=1
p1.xaxis.axis_label = 'Tiempo (ps)'
p1.yaxis.axis_label = 'RMSF (\u212B)'
x = []
y1 = []
with open(basedyn+'_RMSF.csv', newline='') as a:
    reader = csv.reader(a)
    for row in reader:
    	x.append(float(row[0])*float(steps))
    	y1.append(row[1])
p1.line(xa, y1, color='#6b4c9a', legend=systename)
p1.legend.location = "top_left"
window_size = 30
window = np.ones(window_size)/float(window_size)
output_file("/var/www/html/python_graph/RMSF_"+basedyn+".html", title="RMSF de "+systename)
show(gridplot([[p1]], plot_width=900, plot_height=600))
