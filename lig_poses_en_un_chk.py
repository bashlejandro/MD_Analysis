import os

print("Provee la siguiente informacion")
systename=input("Sistema de estudio: ")
steps=input("Steps para leer la trayectoria, se recomienda 100 o 1000: ")
ligand=input("Selecciona tu ligando (resname UNK) o por cadena: ")
#os.system("mkdir "systename"")


f = open("dynposes.tcl", "w")
f.write("""
mol new DB1.a.0.psf
set files [glob *.coor.dcd]
set list [lsort $files]
foreach i $list {mol addfile "$i" step """+steps+""" waitfor all}
set nr_frames [molinfo 0 get numframes ]
set a [atomselect top " """+ligand+""" "] 
mkdir poses
cd poses
for {set fr 0} {$fr < $nr_frames} {incr fr } {
	$a frame $fr 
	$a writepdb [format "_"""+systename+"""_%03d.pdb" $fr] 
	}
exit""")

f.close()
os.system("vmd -dispdev text -e dynposes.tcl")
os.system("rm dynposes.tcl")
