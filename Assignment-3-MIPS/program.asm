# Example MIPS4 Assembly Program
addi $t0, $zero, 3
addi $t1, $zero, 2
add  $t2, $t0, $t1
sw   $t3, 0($zero)

loop:
j loop
