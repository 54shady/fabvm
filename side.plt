set title 'Index Score'
set xlabel '4C2G demo-i'
set ylabel 'y Score'

set term png
set output 'STUB.png'
set style data linespoints
set key noenhanced

plot 'side-STUB.dat' u 1:2 title "STUB"
