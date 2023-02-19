from graphviz import Digraph

# Crear un objeto Digraph
f = Digraph('finite_state_machine', filename='afn.gv')

# Agregar los estados al grafo
f.attr(rankdir='LR')
f.attr('node', shape='doublecircle')
f.node('1')
f.attr('node', shape='circle')
f.node('2')

# Agregar las transiciones
f.edge('1', '2', label='a')

# Mostrar el grafo
print(f.source)
