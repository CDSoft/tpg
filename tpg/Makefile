
all:	parser.py

parser.py:	parser.g
	tpg parser.g -o /tmp/parser.py
	sed 's/tpg\.base/base/g' /tmp/parser.py > parser.py
	rm -f /tmp/parser.py
