"""
Este es un script que genera una gráfica de RMSD (Root Mean Square Deviation)
para una dinámica molecular de M picosegundos usando NAMD como motor de dinámica.
La aplicacion comienza introduciendo el nombre de tu sistema (e.g. Complejo Proteína-Ligando)
Despues el nombre base de tu dinámica, e.g. dyna1 que englobará a los archivos dyna1.a.0.psf que es la informacion
que VMD (Visual Molecular Dynamics) lee como entrada estructural. Luego lee archivos del tipo dyna1.X.N.coor.dcd, donde X
puede tomar un valor de a cuando va de 0 a 9, b de 10 a 99, c de 100 a 999, d de 1000 a 9999, y así sucesivamente. N representa
el valor (en picosegundos generalmente) del archivo de trayectorias (dcd) dependiendo del sample time será el tiempo en ps de 
la dinámica.

La salida de la grafica consiste de un archivo HTML que puede ser visualizado en un explorador, este archivo es depositado por
default en la ruta publica del servidor web Apache2 en un sistema basado en debian.
"""
import numpy as np
import csv
import os
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file

print("Please provide the following.")
systename=input("Study system: ")
basedyn=input("Molecular dynamics base name: ")
steps=input("Steps number for read purpose: ")
sample=input("MD sample time in ps: ")
print("Select system for RMSD measurement.")
system=input("e.g.: protein, chain X, name CA, resid 123: ")

f = open("RMSD.tcl", "w")
f.write("""

######### Get trajectory files in a ordered list ###########
############################################################
set files [glob *.coor.dcd]
set list [lsort $files]
foreach i $list {
mol addfile "$i" first 0 step """+steps+""" waitfor all
} 
set outfile [open """+basedyn+"""_RMSD.csv w]
set nf [molinfo top get numframes]
set frame0 [atomselect top " """+system+""" " frame 0]
set sel [atomselect top " """+system+""" "]

####################### RMSD Loop ##########################
############################################################
for { set i 0 } { $i <= $nf } { incr i } {
$sel frame $i
$sel move [measure fit $sel $frame0]
puts $outfile "[expr {$i+1}]\,[measure rmsd $sel $frame0]"
}
close $outfile
exit""")

f.close()
os.system("vmd -dispdev text "+basedyn+".a.0.psf -e RMSD.tcl")
p1 = figure()
p1.grid.grid_line_alpha=1
p1.xaxis.axis_label = 'Time (ps)'
p1.yaxis.axis_label = 'RMSD (\u212B)'
x = []
y = []
with open(basedyn+'_RMSD.csv', newline='') as a:
    reader = csv.reader(a)
    for row in reader:
    	x.append(float(row[0])*float(sample)*float(steps))
    	y.append(float(row[1]))
p1.line(x, y, color='#6b4c9a', legend_label=systename)
p1.legend.location = "top_left"
window_size = 30
window = np.ones(window_size)/float(window_size)
output_file("RMSD_"+systename+".html", title="RMSD de "+systename)
show(gridplot([[p1]], plot_width=900, plot_height=600))
