#print("Archivo para cargar, en VMD, trayectorias de dinamica formato NAMD *.coor.dcd.")
#print("Proporcioname los siguientes datos.")
#basedyn=input("Carpeta de trayectoria/nombrebase: ")
#mol modstyle 1 0 CPK 1.000000 0.300000 12.000000 12.000000

import os
neq=input("Indicate the number of *.coor.dcd files that do not correspond to the production phase (minimization, heating, equilibrium, etc.): ")
sel_lig=input("Indicate the atom selection of your ligand (e.g., chain B, resname UNK,...): ")
steps=input("Steps to load your trajectory: ")

f = open("READ.tcl", "w")
f.write("""
set dcdfiles [glob *.coor.dcd]
set dcdfiles [lsort $dcdfiles]
set dcdfiles [lreplace $dcdfiles 0 """+str(int(neq)-1)+"""]
foreach i $list {
	mol addfile "$i" first 0 step """+steps+""" waitfor all
	}
mol modcolor 0 0 Structure
mol modstyle 0 0 NewCartoon 0.300000 10.000000 4.100000 0
mol selection """+sel_lig+"""
mol addrep 0
mol modcolor 1 0 Type
mol modstyle 1 0 VDW 1.000000 12.0000000
""")
f.close()

os.system("vmd *.a.0.psf -e READ.tcl")
os.system("rm READ.tcl")

