
parser Foo:

	Bar ->

		x = y
		x = "string"
		x = <y>
		x = <y, z>
		x = {{ x + y }}
		x = y.z
		x = y<a,b>
		x = z<>
		x = lst[1]
		x = lst[2:3]
		x = lst[:3]
		x = lst[2:]
		x = lst[:]
		;
