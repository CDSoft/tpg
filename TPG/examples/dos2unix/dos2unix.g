set runtime

parser d2u:

	lex START/unix ->
		t = Node<>
		(	'\r+'
		|	'[^\r]+'/c t-c
		)*
		'$'
		{{ unix = ''.join(t) }}
		.

main:

{{
	from sys import argv

	try:
		dos, unix = tuple(argv[1:])
	except:
		print "Syntax: dos2unix.py dos_file unix_file"
	else:
		f = open(dos, 'rb')
		g = open(unix, 'wb')
		g.write(d2u()(f.read()))
		f.close()
		g.close()
}}
