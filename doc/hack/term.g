
parser Foo:




	token predef: 'bar' ;

	
	S ->

		'inline'
		predef
		'inline'/s1
		predef/s2
		;
