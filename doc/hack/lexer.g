
parser Foo:





	token integer: '\d+' int ;
	token arrow: '->' ;
	separator spaces: '\s+' ;


	S ->
	
		'\('
		integer
		arrow
		'\)'
		;
