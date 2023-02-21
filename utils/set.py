"""
- Unión
- Intersección
- Agregar cosas al conjunto
"""

class PersonalSet(object):
  
  __content = []
  
  def __init__(self, initial_content):
    self.__content = initial_content
  
  def get_content(self):
    return self.__content

  def add(self, element):
    if (element not in self.__content):
      self.__content.append(element)

  def union(self, other):
    temp = []
    union = []
    #recorrer el arreglo de cada conjunto
    for x in self.__content:
      temp.append(x)
    for y in other.get_content():
      temp.append(y)
    [union.append(unique) for unique in temp if unique not in union]

    return PersonalSet(union)

  def intersection(self, other):
    # funcion para hayar a interseccion de 2 conjuntos
    result = []

    for element in self.__content:
      if (element in other.get_content()):
        result.append(element)

    return PersonalSet(result)
  
  def __eq__(self, other):
    # Primero, si sin iguales, ambos deben tener la misma longitud
    if (len(self.get_content()) != len(other.get_content())):
      return False
    else:
      #Ahora, recorrer cada elemento y verificar si son iguales
      inter = self.intersection(other)
      # Aprovechando el metodo de interseccion, verificamos si
      # La interseccion es igual al conjunto
      if(self.get_content() == inter.get_content()):
        return True
      else:
        return False

  def __str__(self):
    return str(set(self.__content))