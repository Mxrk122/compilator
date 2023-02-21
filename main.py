# Laboratorio 1
# Marco Pablo Orozco Saravia
# Pasar de regex a AFN a partir de un arbol
from utils.postfix import *
from AFD import *

#regex = add_concatenation("a(aab*|bba*)*b|baba")
#regex = add_concatenation("0?(1?)?0*")
regex = add_concatenation("(a*|b*)c")
#regex = add_concatenation("(b|b)*abb(a|b)*")
#regex = add_concatenation("(a|E)b(a+)c?")
#regex = add_concatenation("(a|b)*a(a|b)(a|b)")

regex_postfix = postfix(regex)
print(regex_postfix)

afn: AFN = regex_to_nfa(regex_postfix, regex)
draw(afn)
afd = AFD(afn)
print(afd)