from AFN import *
from utils.set import PersonalSet

class AFD(object):

    __states = PersonalSet([])
    __alphabet = PersonalSet([])
    __mapping = {}
    __initial_state = None
    __acceptance_states = PersonalSet([])

    
    def __init__(self, afn: AFN):
        self.__regex = afn.regex
        self.__states = afn.states
        self.__alphabet = afn.alphabet
        self.__mapping = afn.transitions
        self.__initial_state = afn.start
        self.__acceptance_states = afn.final
    
    def __str__(self):
        return f"""
        Regex: {self.__regex}
        Estados: {self.__states}
        Alfabeto: {self.__alphabet}
        Mapping: {self.__mapping}
        Estado inicial: {self.__initial_state}
        Estados de aceptacion: {self.__acceptance_states}
        """
    
    # Codigo dedicado a pasar a AFD
    def e_closure(self, states):
        #Añadir los estados a los que cada estado se mueve con EPSILON
        stacky = [*states]

        result = [*states]

        while(len(stacky) != 0):
            t = stacky.pop()
            try:
                reachable_states = self.__mapping.get(t).get("EPSILON")
                for state in reachable_states:
                    if state not in result:
                        result.append(state)
                        stacky.append(state)
            except:
                pass
        
        return PersonalSet(result)
    
    def move(self, states, symbol):
        #Añadir los estados a los que cada estado se mueve con el simbolo
        stacky = [*states]

        result = []

        while(len(stacky) != 0):
            t = stacky.pop()
            try:
            # Un try debido a que peude que no tenga transiciones con ese simbolo
                reachable_states = self.__mapping.get(t).get(symbol)
                for state in reachable_states:
                    if state not in result:
                        result.append(state)
            except:
                pass
        
        return PersonalSet(result)
    
    def to_dfa(self):

        # Diccionario de estados de este dfa
        dfa_states = {}

        # Pïla de estados, para compararlos entre ellos
        # elementos que deberia admitir: Personalsets
        dfa_states_set = []

        # Iniciar obteniendo el conjunto del estado inicial, su e-closure
        A = self.e_closure([self.__initial_state])
        dfa_states_set.append(A)


        # Añadir el estado al diccionario con su respectivo indice
        i = 0
        dfa_states[i] = A

        # ESte estado es el primer estado del AFD
        initial_state = dfa_states[i] = A

        # a partir de aca, se trata de hacer moves y añadir al stack los conjuntos
        # nuevos que son nuevos generados por e-closure
        # y descartar los que ya existen
        
        for state in dfa_states_set:
            #Hacer moves, con los simbolos del alfabeto
            for symbol in self.__alphabet.get_content():
                
                # Cambiar el indice del estado
                # Hacerlo aca, ya que este for es el que tiene
                # el verificador de estados
                i += 1


                # Realizar el move del estado
                # Y luego un e-closure de este
                movement = self.move(state.get_content(), symbol)
                new_state = self.e_closure(movement.get_content())

                #Si el estaado ya se encuentra en la pila, descartarlo
                #De lo contrario, agregarlo
                verifier = 0
                
                for j in range(len(dfa_states_set)):
                    # Si se encuentra un estado al que es igual, sumar uno al verificador
                    if dfa_states_set[j] == new_state:
                        verifier += 1
                # Si el verificador no se activo, agregarlo al stack
                if verifier < 1:
                    dfa_states_set.append(new_state)
                    name = dfa_states_set.index(new_state)
                    dfa_states[name] = new_state

        # Ahora solo toca encontrar a que estado se mueve cada quie
        # Crear una lista para almacenar los estados por conjunto
        # Se usara para comparar ya signar las transiciones
        set_states = []

        # ESte array guardara las transiciones
        transitions = []

        for value in list(dfa_states.values()):
            set_states.append(value.get_content())

        for current_state in dfa_states:
            # REvisar por cada simbolo del alfabeto

            for symbol in self.__alphabet.get_content():
                # Realizar el move del estado
                # Y luego un e-closure de este
                movement = self.move(dfa_states[current_state].get_content(), symbol)
                new_state = self.e_closure(movement.get_content())

                #Ver a cual es igual y añadirlo al array de map
                for state in dfa_states:
                    if new_state == dfa_states[state]:
                        # Al encontrar a que estado se mueve
                        # lo agregamos al array de transiciones
                        # El estaado al que se mueve lo encontre en base a la comparacion de index
                        transition = (current_state, symbol, set_states.index(new_state.get_content()))
                        transitions.append(transition)
        
        # Solo nos queda encontrar los estados de aceptación
        acceptance_states = {}
        for ac_state in set_states:
        # print(PersonalSet(ac_state))
        # print(self.__acceptance_states)
            if (PersonalSet(ac_state).intersection(self.__acceptance_states) != PersonalSet([])):
                acceptance_states[set_states.index(PersonalSet(ac_state).get_content())] = PersonalSet(ac_state)

        print("Estados:")
        for state in dfa_states:
            print(state, dfa_states[state])
            print("transiciones:")
            print(transitions)
            print("Estado inicial: ")
            print(set_states.index(initial_state.get_content()), initial_state)
            print("Estados de aceptacion: ")
            for state in acceptance_states:
                print(state, acceptance_states[state])

        return [list(dfa_states.keys()),
        transitions,
        self.__alphabet, set_states.index(initial_state.get_content()),
    list(acceptance_states.keys())]