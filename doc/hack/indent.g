
parser IndentParser:

    set indent = "\s", "#"


    separator spaces: "\s";
    separator comment: "#.*";








    BLOCK ->
        (   INSTR
        |   indent
                BLOCK
            deindent
        )*;


















    INSTR ->
        '\w+'
        ;
