import numpy as np
import csv
import os
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file
"""
"Este es un scritp que genera una gráfica de RMSD (Root Mean Square Deviation)")
"para una dinámica molecular de M picosegundos usando NAMD como motor de dinámica.")
"La utilizacion comienza con introducir el nombre de tu sistema (e.g. Complejo Proteína-Ligando)")
"Despues el nombre base de tu dinámica, e.g. dyna1 que englobará a los archivos dyna1.a.0.psf que es la informacion
que VMD (Visual Molecular Dynamics) lee como entrada estructural. Luego lee archivos del tipo dyna1.X.N.coor.dcd, donde X
puede tomar un valor de a cuando va de 0 a 9, b de 10 a 99, c de 100 a 999, d de 1000 a 9999, y así sucesivamente. N representa
el valor (en picosegundos generalmente) del archivo de trayectorias (dcd) dependiendo del sample time será el tiempo en ps de 
la dinámica.
Para añadir mas lineas usese:
#p1.line(xb y2 color='#cc2529', legend='systename')
#p1.line(xc y3 color='#8e8c3e', legend='systename')
#p1.line(xd y4 color='#3b914e', legend='systename')
#p1.line(xe y5 color='#d97726', legend='systename')
#p1.line(xf y6 color='#396ab1', legend='systename')
"""
systename=input("Tira el nombre de tu complejo, sistema o modelo (e.g. Complejo ACHE-Taxol):")
basedyn=input("Tira el nombre base de la dinamica: ")
steps=input("Steps para leer dinamica: ")
print("Sistema para el cual calcular RMSD.")
sistema=input("protein, chain, name CA, resid: ")
f = open("RMSD.tcl", "w")
f.write("""
#Para listar los archivos de trayectoria
set files [glob *.coor.dcd]
set list [lsort $files]
foreach i $list {
mol addfile "$i" first 0 step """+steps+""" waitfor all
} 
set outfile [open """+basedyn+"""_RMSD.csv w]
set nf [molinfo top get numframes]
set frame0 [atomselect top """+sistema+""" frame 0]
set sel [atomselect top """+sistema+"""]
# Loop para calcular RMSD
for { set i 0 } { $i <= $nf } { incr i } {
$sel frame $i
$sel move [measure fit $sel $frame0]
puts $outfile "[expr {$i+1}]\,[measure rmsd $sel $frame0]"
}
close $outfile
exit""")
f.close()
os.system("mkdir -m 777 var/www/html/python_graph")
os.system("vmd -dispdev text "+basedyn+".a.0.psf -e RMSD.tcl")
p1 = figure()
p1.grid.grid_line_alpha=1
p1.xaxis.axis_label = 'Tiempo (ps)'
p1.yaxis.axis_label = 'RMSD (\u212B)'
x = []
y1 = []
with open(basedyn+'_RMSD.csv', newline='') as a:
    reader = csv.reader(a)
    for row in reader:
    	x.append(float(row[0])*float(steps))
    	y1.append(row[1])
p1.line(xa, y1, color='#6b4c9a', legend=systename)
p1.legend.location = "top_left"
window_size = 30
window = np.ones(window_size)/float(window_size)
output_file("/var/www/html/python_graph/RMSD_"+basedyn+".html", title="RMSD de "+systename)
show(gridplot([[p1]], plot_width=900, plot_height=600))  # open a browser
