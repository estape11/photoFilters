from math import *
from scipy import signal
from scipy import misc
import numpy as numpy
import matplotlib.pyplot as plt

def printMatrix(m):
    for i in range(len(m)):
        print(m[i])
    print()
def convolucionAux(m1,m2):
    if len(m1)==len(m2):
        if len(m1[0])==len(m2[0]):
            temp=0
            for i in range(len(m1)):
                for j in range(len(m1[i])):
                    temp+=m1[i][j]*m2[i][j]
            return temp
    else:
        return None

def convolucionAuxRGB(m1,m2):
    t=[]
    for k in range(0,3):
        temp=0
        for i in range(len(m1)):
            for j in range(len(m1[i])):
                temp+=m1[i][j][k]*m2[i][j]
        t.append(temp)
    return t

def convolucion3x3(matrix,kernel):
    temp=[]
    mTemp=[]
    for i in range(len(matrix)):
        filaTemp=[]
        for j in range(len(matrix[i])):
            if i==0:
                if j==0:
                    mTemp=[
                            [0, 0, 0],
                            [0, matrix[i][j],   matrix[i][j+1]],
                            [0, matrix[i+1][j], matrix[i+1][j+1]]
                        ]
                    filaTemp.append(convolucionAux(mTemp,kernel))
                elif j==len(matrix[i])-1:
                    mTemp=[
                            [0, 0, 0],
                            [matrix[i][j-1],    matrix[i][j],   0],
                            [matrix[i+1][j-1],  matrix[i+1][j], 0]
                        ]
                    filaTemp.append(convolucionAux(mTemp,kernel))
                else:
                    mTemp=[
                            [0, 0,  0],
                            [matrix[i][j-1],    matrix[i][j],   matrix[i][j+1]],
                            [matrix[i+1][j-1],  matrix[i+1][j], matrix[i+1][j+1]]
                        ]
                    filaTemp.append(convolucionAux(mTemp,kernel))
            elif i==len(matrix)-1:
                if j==0:
                    mTemp=[
                            [0,  matrix[i-1][j], matrix[i-1][j+1]],
                            [0,    matrix[i][j],   matrix[i][j+1]],
                            [0, 0, 0]
                        ]
                    filaTemp.append(convolucionAux(mTemp,kernel))
                elif j==len(matrix[i])-1:
                    mTemp=[
                            [matrix[i-1][j-1],  matrix[i-1][j], 0],
                            [matrix[i][j-1],    matrix[i][j],   0],
                            [0, 0, 0]
                        ]
                    filaTemp.append(convolucionAux(mTemp,kernel))
                else:
                    mTemp=[
                            [matrix[i-1][j-1],  matrix[i-1][j], matrix[i-1][j+1]],
                            [matrix[i][j-1],    matrix[i][j],   matrix[i][j+1]],
                            [0, 0, 0]
                        ]
                    filaTemp.append(convolucionAux(mTemp,kernel))
            elif j==0:
                mTemp=[
                        [0,  matrix[i-1][j], matrix[i-1][j+1]],
                        [0,    matrix[i][j],   matrix[i][j+1]],
                        [0,  matrix[i+1][j], matrix[i+1][j+1]]
                    ]
                filaTemp.append(convolucionAux(mTemp,kernel))
            elif j==len(matrix[i])-1:
                mTemp=[
                        [matrix[i-1][j-1],  matrix[i-1][j], 0],
                        [matrix[i][j-1],    matrix[i][j],   0],
                        [matrix[i+1][j-1],  matrix[i+1][j], 0]
                    ]
                filaTemp.append(convolucionAux(mTemp,kernel))
            else:
                mTemp=[
                        [matrix[i-1][j-1],  matrix[i-1][j], matrix[i-1][j+1]],
                        [matrix[i][j-1],    matrix[i][j],   matrix[i][j+1]],
                        [matrix[i+1][j-1],  matrix[i+1][j], matrix[i+1][j+1]]
                    ]
                filaTemp.append(convolucionAux(mTemp,kernel))
            #printMatrix(mTemp)
        temp.append(filaTemp)
    return temp

def convolucion3x3RGB(matrix,kernel):
    temp=[]
    for i in range(len(matrix)):
        filaTemp=[]
        for j in range(len(matrix[i])):
            if i==0:
                if j==0:
                    mTemp=[
                            [[0,0,0], [0,0,0], [0,0,0]],
                            [[0,0,0], matrix[i][j],   matrix[i][j+1] ],
                            [[0,0,0], matrix[i+1][j], matrix[i+1][j+1] ]
                        ]
                    filaTemp.append(convolucionAuxRGB(mTemp,kernel))
                elif j==len(matrix[i])-1:
                    mTemp=[
                            [[0,0,0], [0,0,0], [0,0,0]],
                            [matrix[i][j-1],    matrix[i][j],   [0,0,0]],
                            [matrix[i+1][j-1],  matrix[i+1][j], [0,0,0]]
                        ]
                    filaTemp.append(convolucionAuxRGB(mTemp,kernel))
                else:
                    mTemp=[
                            [[0,0,0], [0,0,0], [0,0,0]],
                            [matrix[i][j-1],    matrix[i][j],   matrix[i][j+1]],
                            [matrix[i+1][j-1],  matrix[i+1][j], matrix[i+1][j+1]]
                        ]
                    filaTemp.append(convolucionAuxRGB(mTemp,kernel))
            elif i==len(matrix)-1:
                if j==0:
                    mTemp=[
                            [[0,0,0],  matrix[i-1][j], matrix[i-1][j+1]],
                            [[0,0,0],    matrix[i][j],   matrix[i][j+1]],
                            [[0,0,0], [0,0,0], [0,0,0]]
                        ]
                    filaTemp.append(convolucionAuxRGB(mTemp,kernel))
                elif j==len(matrix[i])-1:
                    mTemp=[
                            [matrix[i-1][j-1],  matrix[i-1][j], [0,0,0]],
                            [matrix[i][j-1],    matrix[i][j],   [0,0,0]],
                            [[0,0,0], [0,0,0], [0,0,0]]
                        ]
                    filaTemp.append(convolucionAuxRGB(mTemp,kernel))
                else:
                    mTemp=[
                            [matrix[i-1][j-1],  matrix[i-1][j], matrix[i-1][j+1]],
                            [matrix[i][j-1],    matrix[i][j],   matrix[i][j+1]],
                            [[0,0,0], [0,0,0], [0,0,0]]
                        ]
                    filaTemp.append(convolucionAuxRGB(mTemp,kernel))
            elif j==0:
                mTemp=[
                        [[0,0,0],  matrix[i-1][j], matrix[i-1][j+1]],
                        [[0,0,0],    matrix[i][j],   matrix[i][j+1]],
                        [[0,0,0],  matrix[i+1][j], matrix[i+1][j+1]]
                    ]
                filaTemp.append(convolucionAuxRGB(mTemp,kernel))
            elif j==len(matrix[i])-1:
                mTemp=[
                        [matrix[i-1][j-1],  matrix[i-1][j], [0,0,0]],
                        [matrix[i][j-1],    matrix[i][j],   [0,0,0]],
                        [matrix[i+1][j-1],  matrix[i+1][j], [0,0,0]]
                    ]
                filaTemp.append(convolucionAuxRGB(mTemp,kernel))
            else:
                mTemp=[
                        [matrix[i-1][j-1],  matrix[i-1][j], matrix[i-1][j+1]],
                        [matrix[i][j-1],    matrix[i][j],   matrix[i][j+1]],
                        [matrix[i+1][j-1],  matrix[i+1][j], matrix[i+1][j+1]]
                    ]
                filaTemp.append(convolucionAuxRGB(mTemp,kernel))
            #printMatrix(mTemp)
        temp.append(filaTemp)
    return temp

img = misc.imread("l.png")
#convierto la imagen en un arreglo de Numpy
imgArr = numpy.asarray(img)
arr=[
        [[1,2,3],[3,4,5],[5,6,7]],
        [[7,8,9],[9,10,11],[11,12,13]],
        [[13,14,15],[15,16,17],[17,18,19]]
    ]
k=[[1/16,1/8,1/16],[1/8,1/4,1/8],[1/16,1/8,1/16]]
#m=convolucion3x3(imgArr,k)
m=convolucion3x3RGB(imgArr,k)
plt.imshow(m,interpolation='nearest')
plt.gray()
plt.show()
