
{{
    class List(list):
        add = list.append
}}
parser Foo:
    LIST/l ->

        l = List<>
        ITEM/a
        l-a
        ;
