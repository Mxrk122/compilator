from collections import deque

class AFN(object):
    def __init__(self, regex, start, final, transitions: dict) -> None:
        self.regex = regex
        self.start = start
        self.final = final
        self.transitions = transitions
    
    def __str__(self) -> str:
        return f"Regex: {self.regex}, start: {self.start}, final: {self.final}, transitions: {self.transitions}"

class State:
    #el propio estado controla sus transiciones
    def __init__(self, name, transitions=None):
        self.name = name
        self.transitions = transitions or []

    def add_transition(self, state, symbol):
        self.transitions.append((state, symbol))
    
    def set_transitions(self, transitions):
        self.transitions = transitions
    
    def __eq__(self, __o: object) -> bool:
        if self.name == __o.name:
            return True
        else: 
            return False
    
    def __str__(self) -> str:
        return self.name
    
    def show_transitions(self):
        print("transiciones de", self.name)
        for transition in self.transitions:
            print(transition[0], transition[1])

class NFA_creation:
    def __init__(self, name, start, accept, states=None):
        self.name = name
        self.start = start
        self.accept = accept
        self.states = states or []
    
    def getInfo(self):
        print(self.name)
        print("estados: ")
        for state in self.states:
            print(state)
            state.show_transitions()
        
    # metodo para recargar con la nueva informacion
    def reload(self):
        self.states.pop(0)
        self.states.insert(0, self.start)
        self.states.pop()
        self.states.append(self.accept)
    
    # reload echo para añadir el estado inicial y cambiar el estado final de ir
    def reload_or(self):
        self.states.insert(0, self.start)
        self.states.append(self.accept)

    def to_dfa(self):
        # Convert NFA to DFA
        pass

# crear estados segun se requiera
q = []
for i in range(100):
    value = str(i)
    q.append(value)

def regex_to_nfa(postfix):
    epsilon = "E"
    stack = deque()
    i = 0
    for symbol in postfix:
        
        # crear AFNs segun se requiera
        # SEgun notacion postfix, ya debe haber mas de un AFN en el stack
        if symbol == '.':
            # AFN de concaatenacion se trat de unir 2 AFNS
            # se une el estado final del primero al principio del segundo
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            # extraer el estado final del segundo AFN 
            # unirlo con el estado final del primer AFN con toda su info
            new_state = nfa2.states.pop(0)
            nfa1.accept.set_transitions(new_state.transitions)
            nfa1.reload()
            # finalmente crear el nuevo AFN con los estados de ambos AFNs excepto el inicial del segundo
            states = nfa1.states
            for state in nfa2.states:
                states.append(state)

            concat_AFN = NFA_creation("concat", nfa1.start, nfa2.accept, states)
            concat_AFN.reload()
            stack.append(concat_AFN)

        elif symbol == '|':
            # Afn de or se trata de separar el camino para elegir 2 afns diferentes
            nfa2 = stack.pop()
            nfa1 = stack.pop()

            # crear estados para separar el camino
            start = State(q.pop(0))
            start.add_transition(nfa1.start, epsilon)
            start.add_transition(nfa2.start, epsilon)
            accept = State(q.pop(0))
            nfa1.accept.add_transition(accept, epsilon)
            nfa2.accept.add_transition(accept, epsilon)

            states = nfa1.states
            for state in nfa2.states:
                states.append(state)

            new_afn = NFA_creation("or", start, accept, states)
            new_afn.reload_or()
            stack.append(new_afn)

        elif symbol == '*':
            # Afn de kleene se trata de agregar estados a un afn existente
            nfa = stack.pop()
            start = State(q.pop(0))
            accept = State(q.pop(0))
            start.add_transition(nfa.start, epsilon)
            start.add_transition(accept, epsilon)
            nfa.accept.add_transition(nfa.start, epsilon)
            nfa.accept.add_transition(accept, epsilon)

            states = nfa.states

            new_afn = NFA_creation("kleene", start, accept, states)
            new_afn.reload_or()
            stack.append(new_afn)
        elif symbol == '+':
            # AFN de una o más veces se trata de agregar un nuevo estado inicial y final
            # y unirlo con el estado final anterior con una transicion epsilon y con el estado incial con la transicion de simbolo
            nfa = stack.pop()
            start = State(q.pop(0))
            accept = State(q.pop(0))
            start.add_transition(nfa.start, 'Epsilon')
            nfa.accept.add_transition(nfa.start, 'Epsilon')
            nfa.accept.add_transition(accept, 'Epsilon')
            states = nfa.states
            states.append(start)
            states.append(accept)

            new_afn = NFA_creation("one or more", start, accept, states)
            new_afn.reload_or()
            stack.append(new_afn)
        elif symbol == '?':
            # AFN de cero o una vez se trata de agregar un nuevo estado inicial y final
            # y unirlo con el estado final anterior con una transicion epsilon y con el estado incial con la transicion de simbolo
            nfa = stack.pop()
            start = State(q.pop(0))
            accept = State(q.pop(0))
            start.add_transition(nfa.start, 'Epsilon')
            start.add_transition(accept, 'Epsilon')
            nfa.accept.add_transition(accept, 'Epsilon')
            states = nfa.states
            states.append(start)
            states.append(accept)

            new_afn = NFA_creation("zero or one", start, accept, states)
            new_afn.reload_or()
            stack.append(new_afn)
        else:
            # este afn solo tiene 2 estados, el inicial y final con transicion de simbolo
            final_state = State(q.pop(0))
            first_state = State(q.pop(0), [(final_state, symbol)])
            # escribir el NFA resultante:
            simple_NFA = NFA_creation("simple", first_state, final_state, [first_state, final_state])
            stack.append(simple_NFA)

        i += 1
    if len(stack) > 1:
        return None
    else:
        # el AFN se ha creado correctamente, devolver una AFN
        afn = stack.pop()
        print("AFN resultante:")
        regex = "(a|b)*"
        start = afn.start.name
        final = afn.accept.name
        transitions = {}
        print("estados:")
        for state in afn.states:
            print(state)
            transitions[state.name] = {}
            for transition in state.transitions:
                # Añadir transiciones al diccionario
                print(transition[0], transition[1])
                transitions[state.name][transition[1]] = []
            for transition in state.transitions:
                # Añadir transiciones al diccionario
                print(transition[0], transition[1])
                transitions[state.name][transition[1]].append(transition[0].name)

        return AFN(regex, start, final, transitions)


