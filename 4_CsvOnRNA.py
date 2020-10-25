# Librerias
import re
import sys
import string
import math

# Lib RNA
import keras
from keras.models import load_model

# Nummpy
import numpy as np

# Libreria adicional - Funciones adicionales
from zLibs.Funciones import cargarListaRV
from zLibs.Funciones import cargarListaCL
from zLibs.Funciones import generarObjetoRofV
from zLibs.Funciones import generarDiccPredicciones

# Libreria adicional - Funciones adicionales
from zLibs.Funciones import construirScatterPlot2D

# Codificación a utilizar
sys.stdout.encoding
'UTF-8'

# CARGAR DATOS
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# Cargar, generar y recuperar diccionario
listRV_Eng = cargarListaRV("./2_Resultados/2_1_Eng_bibliaRofV_Datos.csv")
listCL_Eng = cargarListaCL("./2_Resultados/2_1_Eng_bibliaRofV_Verbos.csv")

listRV_Spa = cargarListaRV("./2_Resultados/2_1_Spa_bibliaRofV_Datos.csv")
listCL_Spa = cargarListaCL("./2_Resultados/2_1_Spa_bibliaRofV_Verbos.csv")

# Construir elementos RofV
diccRV_Eng, diccEQ_Eng, xDataEng, yDataEng = generarObjetoRofV(listRV_Eng, listCL_Eng)
diccRV_Spa, diccEQ_Spa, xDataSpa, yDataSpa = generarObjetoRofV(listRV_Spa, listCL_Spa)

# CARGAR RNA
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# Cargar RNA
modeloRNA = load_model('./2_Resultados/3_3_Modelo_RNA.h5')

# Ajutar modelo
modeloRNA.summary()

# ANÁLISIS RNA
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# Colores para matriz
aryColors = ['red', 'blue', 'green', 'orange']

# Colores - Verbo:
#   * Rojo: say y decir
#   * Azul: give y tener
#   * Verde: have y tomar
#   * Naranja: come y venir

# Diccionario -> { verb1: { 'Num': numEsperado, 'Res': { NumPredict1: [maxi1, maxi2, ..., maxiN], ..., NumPredictN: [maxi1, maxi2, ..., maxiN] } } }
diccPredictEng = generarDiccPredicciones(xDataEng, yDataEng, diccEQ_Eng, modeloRNA)
diccPredictSpa = generarDiccPredicciones(xDataSpa, yDataSpa, diccEQ_Spa, modeloRNA)

# Función para generar Scatter plot de resultados
def generarScattersPlotRNA(dicc_predict, ary_colors, titulo, nom_archivo):
    # Variables
    aryX_Data = []
    aryY_Data = []
    aryX_Colors = []
    # Recorrer diccionario de vectores
    for valVerbo, objV in dicc_predict.items():
        # Recuperar valores
        numEsperado = objV["Num"]
        resultsRNA = objV["Res"]
        # Variables de apoyo
        # Recorrer resultados RNA
        for numR, aryR in resultsRNA.items():
            # Agregar indice de color
            aryX_Colors.append(ary_colors[numEsperado - 1])
            # Agregar datos objetivo en X
            aryY_Data.append(aryR)
            listApy = []
            # Recorrer eje X
            for val_mx in aryR:
                # Agregar valor para eje Y
                listApy.append(numR)
            # Agregar datos objetivo en Y
            aryX_Data.append(listApy)
    # Generar Scatter Plot
    construirScatterPlot2D (aryX_Colors, aryX_Data, aryY_Data, "Verbo predicho", "Presición", titulo, (nom_archivo + ".png"))

# Construir Scatters Plot
generarScattersPlotRNA(diccPredictEng, aryColors, "Predicciones de verbos - Inglés", "./2_Resultados/4_1_Eng_GraficoDePuntos")
generarScattersPlotRNA(diccPredictSpa, aryColors, "Predicciones de verbos - Español", "./2_Resultados/4_1_Spa_GraficoDePuntos")