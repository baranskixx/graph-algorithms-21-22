# Algorytmy Grafowe
# Piotr Faliszewski 2019
# Load graph in the DIMACS ascii format + weights


def loadCNFFormula( name ):
  """Load a CNF formula in the DIMACS ascii format from 
     the file "name" and return it as a list of clauses
     Returns (V,F)
     V -- highest variable number
     F -- list of clauses"""

  V = 0
  L = []  

  f = open( name, "r" )
  lines = f.readlines()
  for l in lines:
    s = l.split()
    if(len(s) < 1): continue
    if( s[0] == "c" ):
      print(s)
      continue
    elif( s[0] == "p" ):
      V = int(s[2])
    else:
      clause = [int(v) for v in s[:-1]]
      L.append(clause)

  f.close()
  return (V,L)



def loadWeightedGraph( name ):
  """Load a graph in the DIMACS ascii format (with weights) from 
     the file "name" and return it as a list of sets
     Returns (V,L)
     V -- number of vertices (1, ..., V)
     L -- list of edges in the format (x,y,w): edge between x and y with weight w (x<y)"""

  V = 0
  L = []  

  f = open( name, "r" )
  lines = f.readlines()
  for l in lines:
    s = l.split()
    if(len(s) < 1): continue
    if( s[0] == "c" ):
      continue
    elif( s[0] == "p" ):
      V = int(s[2])
    elif( s[0] == "e" ):
      (a,b,c) = (int(s[1]), int(s[2]), int(s[3]))
      (x,y,c) = (min(a,b), max(a,b), c)
      L.append((x,y,c))

  f.close()
  return (V,L)



def loadDirectedWeightedGraph( name ):
  """Load a directed graph in the DIMACS ascii format (with weights) from
     the file "name" and return it as a list of sets
     Returns (V,L)
     V -- number of vertices (1, ..., V)
     L -- list of edges in the format (x,y,w): edge between x and y with weight w"""

  V = 0
  L = []

  f = open( name, "r" )
  lines = f.readlines()
  for l in lines:
    s = l.split()
    if(len(s) < 1): continue
    if( s[0] == "c" ):
      continue
    elif( s[0] == "p" ):
      V = int(s[2])
    elif( s[0] == "e" ):
      (a,b,c) = (int(s[1]), int(s[2]), int(s[3]))
      L.append((a,b,c))

  f.close()
  return (V,L)


def readSolution(name):
    """Read the expected solution from the first line of the graph file"""
    with open(name, 'r') as f:
        line = f.readline()
        return line.split()[-1]

