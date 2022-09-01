from Parser.ParserObject import ParserObject
import os
#Programa Desenvolvido pelo Estudante Ivson Soares
#Para oBtencao de nota na "Disciplia de Construcao de Interpretadores"
#PUCPR.

# Repositório GitHub Link: https://github.com/IvsonSoares/LogicParser

    ######### IMPORTANTE #########
## Para que o programa funcione é preciso
## que o arquivo de texto 
## esteja dentro da pasta data e
## seja descrito como expressoes

parser = ParserObject()
n_arquivos = len(os.listdir(r"data"))
expressoes = open(f"./data/expressoes.txt",'r').read().splitlines()

n_exp = int(expressoes[0])
try:
  for i in range(n_exp):
    parser.isFormula(expressoes[i + 1])
    print("----------------------------------------------")
except IndexError as e:
  print(f"Erro: {e}")
  print(f"{n_exp} é maior que {i} seu último elemento")
