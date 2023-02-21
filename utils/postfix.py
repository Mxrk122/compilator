from AFN import *

def add_concatenation(regex):
    new_regex = ''

    for i in range(len(regex)):
        # Agregar el caracter actual
        new_regex += regex[i]

        # Comprobar si es necesario agregar el operador de concatenación
        if i < len(regex) - 1 and regex[i] not in '|(' and regex[i + 1] not in '|*)?+':
            new_regex += '.'
    return new_regex

def precedence(symbol, other):
    operadores = ["|",".", "+", "*", "?", "("]

    if symbol in "?+*" and other in "?+*":
        return False
    
    if operadores.index(symbol) < operadores.index(other):
        return True
    
    return False

def postfix(regex):
    # Pila de operadores y expresión resultante
    postfix = ""
    op_stack = []

    operadores = ["?","|",".", "+", "*", "("]

    regex = list(regex)
    regex.insert(0, "(")
    regex.append(")")
 
    for symbol in regex:
        # REvisar que no se trate de una operacion
        if symbol not in operadores:    
            # SI se trata del inicio de parentesis, añadirlo al stack de operadores
            if symbol == "(":
                op_stack += symbol
            # Si encontramos el fin del parentesis, agregar todos los operadores dentro del resultado
            elif symbol == ")":
                while(op_stack[-1]!="("):
                    postfix += op_stack.pop()
                # Eliminar el parentesis
                op_stack.pop()
            else:
                # Si se trata de una letra, añadirlo a la expresion
                postfix += symbol

        # Si se trata de un operador, revisar la jerarquia
        else:
            # Si no hay operadores, agregarlos al stack, de igual forma pasa con el (
            if len(op_stack)==0 or op_stack[-1]=="(":
                op_stack += symbol
            else:
                # si la prioridad es mayor, simplemente meterlo al stack de operadores
                if precedence(op_stack[-1], symbol):
                    op_stack += symbol
                # Si la prioridad es menor o igual, sacar     
                else:
                    postfix += op_stack.pop()
                    op_stack += symbol
            
    return postfix