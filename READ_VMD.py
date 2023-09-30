import os

#print("Archivo para cargar, en VMD, trayectorias de dinamica formato NAMD *.coor.dcd.")
#print("Proporcioname los siguientes datos.")
#basedyn=input("Carpeta de trayectoria/nombrebase: ")
print('Indica la seleccion de tu sistema segun corresponda:')
sel_rec=input("Receptor con estructura secundaria. (Ej. chain A, protein, resid 1): ")
sel_lig=input("Ligando. (Ej. chain B, resname UNK,...): ")
steps=input("Steps para leer: ")


f = open("READ.tcl", "w")
f.write("""
set files [glob *.coor.dcd]
set list [lsort $files]
foreach i $list {
	mol addfile "$i" first 0 step """+steps+""" waitfor all
	}
mol selection """+sel_rec+"""
mol modcolor 0 0 Structure
mol modstyle 0 0 NewCartoon 0.300000 10.000000 4.100000 0
mol selection """+sel_lig+"""
mol addrep 0
mol modcolor 1 0 Type
mol modstyle 1 0 CPK 1.000000 0.300000 12.000000 12.000000
""")
f.close()

os.system("vmd *.a.0.psf -e READ.tcl")
os.system("rm READ.tcl")

