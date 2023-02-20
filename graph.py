import pydot
import graphviz
from NFA import *

def draw(afn: AFN):
    # crear grafico
    dot = graphviz.Digraph()
    dot.attr('node', shape='circle')
    dot.attr('edge', arrowhead='vee')
    dot.node('start', shape='none', label='')

    # Escribir AFN

    for s in afn.transitions:
        if s == afn.start:
            dot.edge('start', str(s))
        if s == afn.final:
            dot.node(str(s), shape='doublecircle')
        else:
            dot.node(str(s))
        for a in afn.transitions[s]:
            for t in afn.transitions[s][a]:
                dot.edge(str(s), str(t), label=a)
    
    dot.render('result_afn', format='png')