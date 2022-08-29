import regex as re

class ParserObject():
  """
  * Este Objeto Valida Uma Determinada Expressao Dado as carcteristicas Apresentadas
    - Formula=Constante|Proposicao|FormulaUnaria|FormulaBinaria.  
    - Constante="T"|"F". 
    - Proposicao=[a-z0-9]+ 
    - FormulaUnaria=AbreParen OperadorUnario Formula FechaParen 
    - FormulaBinaria=AbreParen OperatorBinario Formula Formula FechaParen 
    - AbreParen="(" 
    - FechaParen=")" 
    - OperatorUnario="¬" 
    - OperatorBinario="∨"|"∧"|"→"|"↔" 
  """
  
  def __init__(self):

    #Variavies que definem o escopo das nossas expressoes
    self.prepPattern = "[a-z0-9]+"
    self.constante = ["T","F"]
    self.abreParen = ["("]
    self.fechaParen = [")"]
    self.operUnario = ["¬"]
    self.operBinario = ["∨","∧","→","↔"]

    # As variaveis abaixo foram criadas com o escopo global para
    # facilitar a manipulacao e evitar uma alta passagem de parametros nas funcoes
    self.parenIsPair = 0
    self.index = 0
    self.arrOfValues = []
    self.isValid = False

  
  def __isPreposition(self, value):
    return bool(re.match(self.prepPattern, value))
  
  def __isConstant(self, value):
    return True if value in self.constante else False
  
  def __isOperUnario(self, value):
    return True if value in self.operUnario else False
  
  def __isOperBinario(self, value):
    return True if value in self.operBinario else False
    

  #Formulas Unarias
  def __isFormulaUnaria(self, value):
    """
      Essa Funcao verifica se o Value faz parte do escopo da nossa expressao,
      caso seja o inicio de Nova Formula(definido por "("), 
      chamamos a funcao de ValidateFormula
    """
    isUnaria = False
    if value in self.abreParen:
      self.__validateFormula(value)

    elif self.__isPreposition(value) or self.__isConstant(value):
      isUnaria = True

    return isUnaria

  #Formulas Binarias
  def __isFormulaBinaria(self, value):
    """
      Semelhante a Funcao isFormulaUnaria,
      porem Verifica tambem o elemento Value + 1
    """
    isBinaria = False
    if value in self.abreParen:
      self.__validateFormula(value)
      
    elif self.__isPreposition(value) or self.__isConstant(value):
      self.index += 1
      if self.arrOfValues[self.index] in self.abreParen:
        self.__validateFormula(self.arrOfValues[self.index])
        
      elif (self.__isPreposition(self.arrOfValues[self.index])) or (self.__isConstant(self.arrOfValues[self.index])):
        isBinaria = True

    return  isBinaria
  
  def isFormula(self, value):
    """
      Funcao de Entrada do Nosso Objeto de verificacao
    """
    self.parenIsPair = 0
    self.index = 0
    self.arrOfValues = []
    self.isValid = False
    self.arrOfValues = value.split(" ")

    #formulas de Apenas uma constante ou Apenas uma Proposicao
    if (self.__isConstant(self.arrOfValues[self.index]) and len(self.arrOfValues) == 1) or (self.__isPreposition(self.arrOfValues[self.index])
                       and len(self.arrOfValues) == 1):
         print(f"{value} is valid")

    #Verificacao das Demais formulas
    elif self.__validateFormula(self.arrOfValues[self.index]):
         print(f"{value} is valid")

    #Formulas nao reconhecidas como validas
    else:
      print(f"{value} is invalid")

  
  def __validateFormula(self, value):
    
    #Formulas que iniciam com "("
    if value in self.abreParen:
      self.parenIsPair += 1
      self.index += 1
      
      if self.__isOperUnario(self.arrOfValues[self.index]):
        self.index += 1
        if(self.__isFormulaUnaria(self.arrOfValues[self.index])):
          self.index += 1
          self.isValid = True

      elif self.__isOperBinario(self.arrOfValues[self.index]):
        self.index += 1
        if(self.__isFormulaBinaria(self.arrOfValues[self.index])):
          self.isValid = True
          self.index += 1
          
      else: 
        self.isValid = False

    #Logica de ")"
    if (self.arrOfValues[self.index] in self.fechaParen) and (self.parenIsPair > 0):
        self.parenIsPair -= 1
        if(self.index != len(self.arrOfValues) - 1):
          self.index += 1
          if(self.arrOfValues[self.index] in self.abreParen):
            self.__validateFormula(self.arrOfValues[self.index])
          else:
            if(self.__isPreposition(self.arrOfValues[self.index])) or (self.__isConstant(self.arrOfValues[self.index])):
              self.index += 1
              self.__validateFormula(self.arrOfValues[self.index])
          
           
    #Validacao final
    #1- Caso as expressoes sejam valida
    #2- Para todo "(" haja um respectivo ")"
    #3- Ate o ultimo elemento da expressao tenha sido validado      
    if (self.isValid)          and \
       (self.parenIsPair == 0) and \
       (self.index == len(self.arrOfValues) - 1):
      
      return True

    else:
      
      return False