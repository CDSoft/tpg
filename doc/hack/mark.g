
parser Foo:

	S ->

		A
		!x			# put a mark 'x'
		B
		C
		!y			# put a mark 'y'
		t = x..y	# extract from 'x' to 'y'
		;
