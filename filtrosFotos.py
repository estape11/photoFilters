from scipy import misc
from scipy import signal
import numpy as numpy
from math import *
import matplotlib.pyplot as plt

"""
    Realiza la operacion convolucion entre f y g
"""
def convolucion2D(f, g):
    # f es la imagen indexada (v, w)
    # g es el kernel del filtro indexada (s, t) DEBE SER IMPAR
    # h es la imagen de salida indexada (x, y),
    if g.shape[0] % 2 != 1 or g.shape[1] % 2 != 1:
        raise valorError("Error, las matrices deben ser impar")
    # sValor y tValor es el numero de pixeles entre el pixel de centro
    # El tamano de salida es calculado anadiendole sValor y tValor a cada
    # lado de las dimensiones del tamano de la imagen de salida
    vMax = f.shape[0]
    wMax = f.shape[1]
    sMax = g.shape[0]
    tMax = g.shape[1]
    sValor = sMax // 2
    tValor = tMax // 2
    xMax = vMax + 2*sValor
    ymax = wMax + 2*tValor
    # Arreglo de salida
    h = numpy.zeros([xMax, ymax], dtype=f.dtype)
    # Se realiza la convolucion
    for x in range(xMax):
        for y in range(ymax):
            s_from = max(sValor - x, -sValor)
            s_to = min((xMax - x) - sValor, sValor + 1)
            t_from = max(tValor - y, -tValor)
            t_to = min((ymax - y) - tValor, tValor + 1)
            valor = 0
            for s in range(s_from, s_to):
                for t in range(t_from, t_to):
                    v = x - sValor + s
                    w = y - tValor + t
                    valor += g[sValor - s, tValor - t] * f[v, w]
            h[x, y] = valor
    return h

"""
    Realiza el calculo de cada valor de la nueva matriz del kernel de Gauss
"""
def gaussCalculo(x,y,sigma):
    exponente=-(x**2+y**2)/(2*sigma**2)
    temp = e**exponente/(2*pi*sigma**2)
    return temp

"""
    Se encarga de generar el kernel del efecto blur gaussiano
    radio:radio del efecto
    sigma:valor de blur (borrosidad)
"""
def gaussKernel(radio,sigma):
    x=-radio
    y=-radio
    gauss=[]
    for i in range(0,radio*2+1):
        fila=[]
        for j in range(0,radio*2+1):
            fila.append(gaussCalculo(x,y,sigma))
            y+=1
        gauss.append(fila)
        y=-radio
        x+=1
    return numpy.array(gauss)

"""
    Se encarga de dividir la matriz mRGB en sus respectios canales R, G y B
"""
def separarRGB(mRGB):
    R=numpy.zeros((mRGB.shape[0],mRGB.shape[1]), dtype="uint8")
    G=numpy.zeros((mRGB.shape[0],mRGB.shape[1]), dtype="uint8")
    B=numpy.zeros((mRGB.shape[0],mRGB.shape[1]), dtype="uint8")
    R[:]=mRGB[:,:,0]
    G[:]=mRGB[:,:,1]
    B[:]=mRGB[:,:,2]
    return numpy.array([R,G,B])

"""
    Une los canales R, G y B en una sola matriz
"""
def unirRGB(R,G,B):
    mRGB=numpy.zeros((R.shape[0],R.shape[1],3), dtype="uint8")
    mRGB[:,:,0]=R[:]
    mRGB[:,:,1]=G[:]
    mRGB[:,:,2]=B[:]
    return mRGB

"""
    Funcion principal del efecto Gaussiano
    Imagen: nombre de la imagen a realizar el efecto
    Radio del efecto blur
    Sigma el grado del efecto
    Retorna un arreglo de la imagen con el efecto aplicado
"""
def blurGaussiano(imagen,radio,sigma):
    print("-Ejecutando efecto Blur Gaussiano en "+imagen+" con un radio de "+str(radio))
    img = misc.imread(imagen)
    #convierto la imagen en un arreglo de Numpy
    imgArr = numpy.asarray(img)
    #kernel de gauss
    kernel=gaussKernel(radio,sigma)
    if len(imgArr.shape)==2:
        # arreglo temporal para las multiples pasadas
        imgTmp=convolucion2D(imgArr,kernel)
        print("-Completado!")
        return imgTmp
    else:
        #Separa los canales de colores
        RGB=separarRGB(imgArr)
        #Efecto para cada color RGB
        Rtemp=convolucion2D(RGB[0],kernel)
        Gtemp=convolucion2D(RGB[1],kernel)
        Btemp=convolucion2D(RGB[2],kernel)
        #Une los canales RGB
        imgTmp=unirRGB(Rtemp,Gtemp,Btemp)
        print("-Completado!")
        return imgTmp

"""
    Funcion principal del efecto de bordes
    Imagen: nombre de la imagen a realizar el efecto
    Retorna un arreglo de la imagen con el efecto aplicado
"""
def detectorBordes(imagen):
    print("-Ejecutando efecto Edge Detection en "+imagen)
    laplaceKernel=numpy.array([
                                [0,0,-1,0,0],
                                [0,-1,-2,-1,0],
                                [-1,-2,16,-2,-1],
                                [0,-1,-2,-1,0],
                                [0,0,-1,0,0]
                                            ])
    laplaceKernel=laplaceKernel/50
    img = misc.imread(imagen)
    #convierto la imagen en un arreglo de Numpy
    imgArr = numpy.asarray(img)
    if len(imgArr.shape)==2:
        imgTmp=convolucion2D(imgArr,laplaceKernel)
        print("-Completado!")
        return imgTmp
    else:
        #Separa los canales de colores
        RGB=separarRGB(imgArr)
        #gris=RGB[0]+RGB[1]+RGB[2]
        #gris=gris/3
        imgTmp=convolucion2D(RGB[1],laplaceKernel)
        print("-Completado!")
        return imgTmp

"""
    Funcion para agregar la terminacion a las fotos
"""
def cambiarNombre(nombre,agregar):
    temp=""
    for letra in nombre:
        if letra==".":
            temp+=agregar+letra
        else:
            temp+=letra
    return temp

"""
    Funcion principal del programa
"""
def main():
    print("=======================================")
    print(">>>>>>>>>Filtros para imagenes<<<<<<<<<")
    print("=======================================")
    print("***************************************")
    print("*   La imagen debe estar dentro de la *")
    print("*   misma carpeta del programa, de lo *")
    print("*   contrario debe escribir la ruta   *")
    print("*   donde se encuentra y el nombre    *")
    print("***************************************")
    continuar=True
    entrada=0
    while(continuar):
        print("================ Menu ================")
        print("1-Blur Gaussiano (efecto borroso).")
        print("2-Detector de Bordes (dibujo de la imagen).")
        print("3-Salir.")
        try:
            entrada=int(input(">Ingrese un valor: "))
            if entrada==1:
                nombreImg=input(">Ingrese el nombre del archivo: (incluyendo extension) ")
                radio=int(input(">Ingrese el radio del efecto (recomendado 2): "))
                try:
                    imgTmp=blurGaussiano(nombreImg,radio,1)
                    entrada=input(">Desea guardar la foto con el efecto aplicado? (y/n): ")
                    if entrada=="y" or entrada=="Y":
                        misc.imsave(cambiarNombre(nombreImg,'_blurred'), imgTmp)
                        print("-Imagen guardada: "+cambiarNombre(nombreImg,'_blurred'))
                    entrada=input(">Desea ver la imagen resultado? (y/n): ")
                    if entrada=="y" or entrada=="Y":
                        if len(imgTmp.shape)==2:
                            plt.imshow(imgTmp,interpolation='nearest')
                            plt.gray()
                            plt.show()
                        else:
                            plt.imshow(imgTmp,interpolation='nearest')
                            plt.show()
                except:
                    print("Error: Imagen no encontrada.")
            elif entrada==2:
                nombreImg=input(">Ingrese el nombre del archivo: (incluyendo extension) ")
                try:
                    imgTmp=detectorBordes(nombreImg)
                    entrada=input(">Desea guardar la foto con el efecto aplicado? (y/n): ")
                    if entrada=="y" or entrada=="Y":
                        misc.imsave(cambiarNombre(nombreImg,'_edge'), imgTmp)
                        print("-Imagen guardada: "+cambiarNombre(nombreImg,'_edge'))
                    entrada=input(">Desea ver la imagen resultado? (y/n): ")
                    if entrada=="y" or entrada=="Y":
                        plt.imshow(imgTmp,interpolation='nearest')
                        plt.gray()
                        plt.show()
                except:
                    print("Error: Imagen no encontrada.")
            elif entrada==3:
                print("Saliendo...")
                continuar=False
            else:
                print("Error: Entrada invalida, intente de nuevo.")
        except:
            print("Error: Entrada invalida, intente de nuevo.")
            pass

main()