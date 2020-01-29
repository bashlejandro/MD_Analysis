puts "Nombre del archivo: "
gets stdin nombre

puts "Elige el sistema:"
puts "Ejemplo: protein, chain, name CA"
gets stdin sistema


#############################################
######  RADIUS OF GYRATION  #################
#############################################
proc gyr_radius {sel} {
  # make sure this is a proper selection and has atoms
  if {[$sel num] <= 0} {
    error "gyr_radius: must have at least one atom in selection"
  }
  # gyration is sqrt( sum((r(i) - r(center_of_mass))^2) / N)
  set com [center_of_mass $sel]
  set sum 0
  foreach coord [$sel get {x y z}] {
    set sum [vecadd $sum [veclength2 [vecsub $coord $com]]]
  }
  return [expr sqrt($sum / ([$sel num] + 0.0))]
}

#############################################
######  CENTER OF MASS  #####################
#############################################
proc center_of_mass {selection} {
        # some error checking
        if {[$selection num] <= 0} {
                error "center_of_mass: needs a selection with atoms"
        }
        # set the center of mass to 0
        set com [veczero]
        # set the total mass to 0
        set mass 0
        # [$selection get {x y z}] returns the coordinates {x y z} 
        # [$selection get {mass}] returns the masses
        # so the following says "for each pair of {coordinates} and masses,
	#  do the computation ..."
        foreach coord [$selection get {x y z}] m [$selection get mass] {
           # sum of the masses
           set mass [expr $mass + $m]
           # sum up the product of mass and coordinate
           set com [vecadd $com [vecscale $m $coord]]
        }
        # and scale by the inverse of the number of atoms
        if {$mass == 0} {
                error "center_of_mass: total mass is zero"
        }
        # The "1.0" can't be "1", since otherwise integer division is done
        return [vecscale [expr 1.0/$mass] $com]
}



#############################################
###############  LOOP  ######################
#############################################

set outfile [open ${nombre}_ROG.csv w]
#puts $outfile "i rad_of_gyr"
set nf [molinfo top get numframes] 
set i 0

set prot [atomselect top $sistema ]
while {$i < $nf} {

    $prot frame $i
    $prot update

    set i [expr {$i + 1}]
    set rog [gyr_radius $prot]

    puts $outfile $i\,$rog

} 
#for {set i 0} {$i < $nf} {incr i} {
#   puts $outfile "[expr {$i+1}]\,[lindex gyr_radius $prot]"
#} 

close $outfile
#############################################
###############  PYTHON GRAPH  ##############
#############################################
python3 ROG.py

#continuara...
