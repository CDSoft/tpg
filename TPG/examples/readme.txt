
Content of the archive:

* tpg

tp.g is the source grammar for TPG. To regenerate TPG.py run
python TPG.py tp.g -o TPG2.py
Obviously you need TPG.py to regenerate it ;-)

* calc

calc.g is a simple calculator. Run python TPG.py calc.g > calc.py to
generate calc.py then run python calc.py and type in some mathematical
expressions.

* graph

graph.py draws 2D curves and 3D surfaces given their equations.
run python graph.py tore to draw a torus

* notation

notation.py recognizes and translates infix, prefix and postfix
expressions. Run python notation.py and type in some expressions.
For example :
	1 + 1
	+ 1 + 2 3
	5 6 7 + *
	...

* dos2unix

dos2unix.g is a simple DOS 2 UNIX file converter.

