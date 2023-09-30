import os

#print("Archivo para cargar, en VMD, trayectorias de dinamica formato NAMD *.coor.dcd.")
#print("Proporcioname los siguientes datos.")
#basedyn=input("Carpeta de trayectoria/nombrebase: ")
#steps=input("Steps para leer: ")
#carpeta=input("Root directory: ")

f = open("average.tcl", "w")
f.write("""
set files [glob *.coor.dcd]
set list [lsort $files]
foreach i $list {
	mol addfile "$i" first 0 step 1 waitfor all
	}
set sel [atomselect top protein]
set pos [measure avpos $sel]
$sel set {x y z} $pos
$sel writepdb estructura_prom_dinamica_completa.pdb
exit""")

f.close()

os.system("vmd -dispdev text *.a.0.psf -e average.tcl")
os.system("rm average.tcl")

