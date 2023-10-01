import numpy as np
import csv
import os
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file

print("Please provide the following.")
systename=input("Study system: ")
basedyn=input("Molecular dynamics base name: ")
print("Part of the system for RMSF measurement.")
system=input("e.g.: protein, chain X, name CA, resid 123: ")
print("Select frames to measure RMSF")
first=input("first: ")
last=input("last: ")
steps=input("Steps number for read purpose: ")

f = open("RMSF.tcl", "w")
f.write("""
#Get trajectory files in a ordered list
set files [glob *.coor.dcd]
set list [lsort $files]
foreach i $list {
mol addfile "$i" first 0 step """+steps+"""  waitfor all
} 
set outfile [open """+basedyn+"""_RMSF.csv w]

set reference [atomselect top " """+system+""" " frame 0]
# the frame being compared
set compare [atomselect top " """+system+""" "]
set num_steps [molinfo top get numframes]

for {set frame 0} {$frame < $num_steps} {incr frame} {
  # get the correct frame
  $compare frame $frame

  # compute the transformation
  set trans_mat [measure fit $compare $reference]
  # do the alignment
  $compare move $trans_mat
}

set sel [atomselect top " """+system+""" "]
set rmsf [measure rmsf $sel first """+first+""" last """+last+""" step 1]
for {set i 0} {$i < [$sel num]} {incr i} {
puts $outfile "[expr {$i+1}]\,[lindex $rmsf $i]"
} 
close $outfile﻿
exit""")

f.close()
os.system("vmd -dispdev text "+basedyn+".a.0.psf -e RMSF.tcl")
os.system("rm RMSF.tcl")

p1 = figure()
p1.grid.grid_line_alpha=1
p1.xaxis.axis_label = 'Residue number'
p1.yaxis.axis_label = 'RMSF (\u212B)'
x = []
y = []
with open(archivo+'_RMSF.csv', newline='') as a:
    reader = csv.reader(a)
    for row in reader:
    	x.append(float(row[0]))
    	y.append(row[1])
p1.line(x1, ya, color='#8e8c3e', legend_label=systename)
p1.legend.location = "top_left"
window_size = 30
window = np.ones(window_size)/float(window_size)
output_file("RMSF "+basedyn+".html", title="RMSF "+systename)
show(gridplot([[p1]], plot_width=1000, plot_height=600))  # open a browser
