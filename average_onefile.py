import os


#print("Proporcioname los siguientes datos.")
trayec=input("Indica el nombre del archivo con extension .coor.dcd para generar un promedio: ")
#Carpeta de trayectoria/nombrebase: ")
#steps=input("Steps para leer: ")
#carpeta=input("Root directory: ")

f = open("average.tcl", "w")
f.write("""
mol addfile """+trayec+""" first 0 step 1 waitfor all
set sel [atomselect top protein]
set pos [measure avpos $sel]
$sel set {x y z} $pos
$sel writepdb estructura_prom_dinamica.pdb
exit""")

f.close()

os.system("vmd -dispdev text *.a.0.psf -e average.tcl")
os.system("rm average.tcl")

