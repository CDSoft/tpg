
{{
    class Couple:
        def __init__(self, a, b):
            self.a = a
            self.b = b
}}
parser Foo:
    COUPLE1/c ->

        c=Couple<a,b>
        ;

    COUPLE2/Couple<a,b> ->

        ;
