import numpy as np
import csv
import os
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file

basedyn=input("Tira el nombre base de la dinamica: ")
#archivo=input("Tira el nombre de tu archivo otra vez...")

f = open("RMSD.tcl", "w")
f.write("""
puts "Steps para leer dinamica:	"
gets stdin steps
puts "Sistema para el cual calcular RMSD."
puts "protein, chain, name CA, resid	"
gets stdin sistema
set files [glob *.coor.dcd]
set list [lsort $files]
foreach i $list {
mol addfile "$i" first 0 step $steps waitfor all
} 
set outfile [open """+basedyn+"""_RMSD.csv w]
set nf [molinfo top get numframes]
set frame0 [atomselect top $sistema frame 0]
set sel [atomselect top $sistema]
# rmsd calculation loop
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
p1.xaxis.axis_label = 'Tiempo (ps)'
p1.yaxis.axis_label = 'RMSD (\u212B)'
x = []
y = []
xa = []
m = 0
with open(basedyn+'_RMSD.csv', newline='') as a:
    reader = csv.reader(a)
    for row in reader:
    	x.append(row[0])
    	y.append(row[1])
for n in x:
	xa.append(float(x[m]))
	m = m+1

p1.line(xa, y, color='#6b4c9a', legend='RMSD vs Frame')
#p1.line(x3, yc, color='#cc2529', legend='ACh')
#p1.line(x4, yd, color='#8e8c3e', legend='LQM 919')
#p1.line(x5, ye, color='#3b914e', legend='LQM 996')
#p1.line(x6, yf, color='#d97726', legend='Lisinopril')
#p1.line(x1, ya, color='#396ab1', legend='apo')

p1.legend.location = "top_left"
window_size = 30
window = np.ones(window_size)/float(window_size)

output_file("/var/www/html/alex/RMSD_"+basedyn+".html", title="RMSD de "+basedyn)
show(gridplot([[p1]], plot_width=900, plot_height=600))  # open a browser
