import struct

def frombuffer(array, dtype):
    newarray = []
    for element in array:
        newarray.append(element)
    return newarray

def isMatrix(object):
    return isinstance(object, list)

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeternminant(m):
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    return determinant

def getMatrixInverse(m):
    determinant = getMatrixDeternminant(m)
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
        cofactors.append(cofactorRow)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant
    return cofactors
def mgrid(rango_x, rango_y):
    lista = []
    lista_mayor = []
    for i in rango_x:
        lista_menor = []
        for j in rango_y:            
            lista_menor.append(i)
        lista_mayor.append(lista_menor)
    lista.append(lista_mayor)
    lista_mayor = []
    for i in rango_x:
        lista_menor = []
        for j in rango_y:            
            lista_menor.append(j)
        lista_mayor.append(lista_menor)
    lista.append(lista_mayor)
    return lista

def reshape(m):
  m_l = len(m)
  m_r_l = len(m[0])
  m_c_l = len(m[0][0])
  x = m_l*m_r_l*m_c_l/2
  x = int(x)
  lista = []
  for i in m:
    for j in i:
      for k in j:
        lista.append(k)
  lista_nueva = []
  for i in range(0,2):
    lista_menor = []
    for j in range(0, x):
      lista_menor.append(lista[i*x + j])
    lista_nueva.append(lista_menor)
  return lista_nueva

def vstack(m):
    m_c_l = len(m[0])
    lista = m
    lista_de_1s = []
    for i in range(0,m_c_l):
        lista_de_1s.append(1.0)
    lista.append(lista_de_1s)
    return lista

def dot(m1, m2):
    if not isinstance(m1[0], list):
        m1 = [[i] for i in m1]
    if not isinstance(m2[0], list):
        m2 = [[i] for i in m2]
  
    c = []
    for i in range(0,len(m1)):
        temp=[]
        for j in range(0,len(m2[0])):
            s = 0
            for k in range(0,len(m1[0])):
                s += m1[i][k]*m2[k][j]
            temp.append(s)
        c.append(temp)
    return c

def transpose(matrix):
    rows = len(matrix)
    columns = len(matrix[0])

    matrix_T = []
    for j in range(columns):
        row = []
        for i in range(rows):
           row.append(matrix[i][j])
        matrix_T.append(row)

    return matrix_T
    