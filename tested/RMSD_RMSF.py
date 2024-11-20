import numpy as np
import csv
import os
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file
print("This script uses VMD to help you read your NAMD molecular dynamics and extract the information to make RMSD, RMSF. It will generate two types of files for each graph: an HTML file and also a CSV file in >
print("Provide the following information")
neq=input("Indicate the number of *.coor.dcd files that do not correspond to the production phase (minimization, heating, equilibrium, etc.): ")
systename=input("System name (this name will appear on the graph): ")
steps=input("Steps to read the trajectory: ")
sample=input("Sample time (ps): ")

print("Atom selection for RMSD measurement.")
system1=input("e.g.: protein, chain X, name CA, resid 123: ")

print("Atom selection for RMSF measurement.")
system2=input("e.g.: protein, chain X, name CA, resid 123: ")
fresid=input("Number of the first amino acid: ")

pibici=input("""Write pbc "unwrap -all" if your protein voló alv si no solo salta""")

f = open("RMSD_RMSF.tcl", "w")
f.write("""
############################################################
######### Get trajectory files in a organized list #########
############################################################
set dcdfiles [glob *.coor.dcd]
set dcdfiles [lsort $dcdfiles]
set dcdfiles [lreplace $dcdfiles 0 """+str(int(neq)-1)+"""]
foreach i $dcdfiles {
mol addfile "$i" first 0 step """+steps+""" waitfor all
}
package require pbctools
"""+pibici+"""
############################################################
####################### RMSD ###############################
############################################################
set outfile [open """+systename+"""_RMSD.csv w]
set nf [molinfo top get numframes]
set frame0 [atomselect top " """+system1+""" " frame 0]
set sel [atomselect top " """+system1+""" "]
for { set i 0 } { $i <= $nf } { incr i } {
$sel frame $i
$sel move [measure fit $sel $frame0]
puts $outfile "[expr {$i+1}]\,[measure rmsd $sel $frame0]"
}
############################################################
####################### RMSF ###############################
############################################################
set outfile [open """+systename+"""_RMSF.csv w]
set reference [atomselect top " """+system2+""" " frame 0]
# the frame being compared
set compare [atomselect top " """+system2+""" "]
set num_steps [molinfo top get numframes]
for {set frame 0} {$frame < $num_steps} {incr frame} {
  # get the correct frame
  $compare frame $frame
  # compute the transformation
  set trans_mat [measure fit $compare $reference]
  # do the alignment
  $compare move $trans_mat}

set sel [atomselect top " """+system2+""" "]

set rmsf [measure rmsf $sel first 0 step 1]
for {set i 0} {$i < [$sel num]} {incr i} {
puts $outfile "[expr {$i+1}]\,[lindex $rmsf $i]"} 

close $outfile﻿
exit""")

f.close()
os.system("vmd -dispdev text *.a.0.psf -e RMSD_RMSF.tcl")
os.system("rm RMSD_RMSF.tcl")
p1 = figure()
p1.grid.grid_line_alpha=1
p1.xaxis.axis_label = 'Time (ns)'
p1.yaxis.axis_label = 'RMSD (\u212B)'
x = []
y = []
with open(systename+'_RMSD.csv', newline='') as a:
    reader = csv.reader(a)
    for row in reader:
        x.append(float(row[0])*float(sample)*float(steps)/1000)
        y.append(float(row[1]))
p1.line(x, y, color='#6b4c9a', legend_label=systename)
p1.legend.location = "top_left"
window_size = 300
window = np.ones(window_size)/float(window_size)
output_file("RMSD_"+systename+".html", title="RMSD_"+systename)
show(gridplot([[p1]], width=1000, height=666))

p1 = figure()
p1.grid.grid_line_alpha=1
p1.xaxis.axis_label = 'Residue number'
p1.yaxis.axis_label = 'RMSF (\u212B)'
x = []
y = []
with open(systename+'_RMSF.csv', newline='') as a:
    reader = csv.reader(a)
    for row in reader:
        x.append(float(fresid)-float(1)+float(row[0]))
        y.append(row[1])
p1.line(x, y, color='#8e8c3e', legend_label=systename)
p1.legend.location = "top_left"
window_size = 300
window = np.ones(window_size)/float(window_size)
output_file("RMSF_"+systename+".html", title="RMSF_"+systename)
show(gridplot([[p1]], width=1000, height=666))  # open a browser
