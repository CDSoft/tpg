
Content of the archive:

* TPG

tpg_grammar.g is the source grammar for TPG. To regenerate tpg.py run
python tpg.py tpg_grammar.g -o tpg.py
Obviously you need tpg.py to regenerate it ;-)

* TPG/calc

calc.g is a simple calculator. Run python TPG.py calc.g > calc.py to
generate calc.py then run python calc.py and type in some mathematical
expressions.

* TPG/notation

notation.py recognizes and translates infix, prefix and postfix
expressions. Run python notation.py and type in some expressions.
For example :
	1 + 1
	+ 1 + 2 3
	5 6 7 + *
	...

