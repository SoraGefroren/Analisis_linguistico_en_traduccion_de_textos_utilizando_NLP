# Librerias
import re
import sys
import string
import math

# Codificación a utilizar
sys.stdout.encoding
'UTF-8'

# Import PANDAS y SKLEARN
import pandas as pd

# Libreria adicional - Funciones adicionales
from zLibs.Funciones import cargarDocumentoCSV
from zLibs.Funciones import generarColeccionesRofV
# Libreria adicional - Funciones adicionales
from zLibs.Funciones import corregirEjesXY
from zLibs.Funciones import construirScatterPlot2D
# from zLibs.Funciones import generarMatrizColores


# VARIABLES DE OBJETIVO
# ------------------------------
# Lista de verbos objetivo
listObjVerbsEng = ["give", "say", "have", "come"]
listObjVerbsSpa = ["dar", "decir", "tener", "venir"]

# Cargar, generar y recuperar diccionario
diccVersosEng, diccVerbosEng, listCorpusEng = cargarDocumentoCSV("./2_Resultados/1_1_bibliaDataTab-Eng.csv")
diccVersosSpa, diccVerbosSpa, listCorpusSpa = cargarDocumentoCSV("./2_Resultados/1_1_bibliaDataTab-Spa.csv")

# Generar matriz RofV
diccVF_Eng, diccRofV_Eng, listRofV_Eng, diccCLRV_Eng, listCLRV_Eng = generarColeccionesRofV(listObjVerbsEng, diccVerbosEng, listCorpusEng)
diccVF_Spa, diccRofV_Spa, listRofV_Spa, diccCLRV_Spa, listCLRV_Spa = generarColeccionesRofV(listObjVerbsSpa, diccVerbosSpa, listCorpusSpa)

# Generar y salvar tabla RofV de datos calculados
datFrm = pd.DataFrame(listRofV_Eng)
export_csv = datFrm.to_csv ('./2_Resultados/2_1_Eng_bibliaRofV_Datos.csv', index = None, header=True)

# Generar y salvar tabla RofV de correspondencias por fila
datFrm = pd.DataFrame(listCLRV_Eng)
export_csv = datFrm.to_csv ('./2_Resultados/2_1_Eng_bibliaRofV_Verbos.csv', index = None, header=True)

# Generar y salvar tabla RofV de datos calculados
datFrm = pd.DataFrame(listRofV_Spa)
export_csv = datFrm.to_csv ('./2_Resultados/2_1_Spa_bibliaRofV_Datos.csv', index = None, header=True)

# Generar y salvar tabla RofV de correspondencias por fila
datFrm = pd.DataFrame(listCLRV_Spa)
export_csv = datFrm.to_csv ('./2_Resultados/2_1_Spa_bibliaRofV_Verbos.csv', index = None, header=True)

# Corregir datos de ejes X y Y
aryXsv_Eng, aryYsv_Eng, aryXcv_Eng, aryYcv_Eng, aryVrbsEng = corregirEjesXY(diccVF_Eng)
aryXsv_Spa, aryYsv_Spa, aryXcv_Spa, aryYcv_Spa, aryVrbsSpa = corregirEjesXY(diccVF_Spa)

'''
# Matriz de colores
# Eje = [[v1,v2,...,vn], [v1,v2,...,vn], [v1,v2,...,vn], [v1,v2,...,vn]]
aryColoresEng = generarMatrizColores(aryXsv_Eng, aryYsv_Eng)
aryColoresSpa = generarMatrizColores(aryXsv_Spa, aryYsv_Spa)
'''

# Colores para matriz
aryColors = ['red', 'blue', 'green', 'orange']

# Colores - Verbo:
#   * Rojo: say y decir
#   * Azul: give y tener
#   * Verde: have y tomar
#   * Naranja: come y venir

# Generar PLOT Eng
construirScatterPlot2D (aryColors, aryXsv_Eng, aryYsv_Eng, "Distancia a la derecha", "Distancia a la izquierda", "Gráfico de puntos sobre distancias a verbos - Inglés", "./2_Resultados/2_2_Eng_GraficoDePuntos.png")
# Generar PLOT Spa
construirScatterPlot2D (aryColors, aryXsv_Spa, aryYsv_Spa, "Distancia a la derecha", "Distancia a la izquierda", "Gráfico de puntos sobre distancias a verbos - Español", "./2_Resultados/2_2_Spa_GraficoDePuntos.png")

# Variable
strNota = ""

# Recorrer verbos y mostrar color
for i in range(len(aryVrbsEng)):
    # Anunciar relación de color
    strNota += ("Eng: Para \"" + aryVrbsEng[i] + "\" corresponde el color \"" + aryColors[i] + "\"\n")
    strNota += ("Spa: Para \"" + aryVrbsSpa[i] + "\" corresponde el color \"" + aryColors[i] + "\"\n")
    strNota += ("---------------------------------------------\n")

# Guardar diccionarios de frecuencias
with open('./2_Resultados/2_3_NotaColoresM.txt', 'w', encoding="utf-8") as myFile:
	# Finalizar texto
	myFile.write(strNota)
	myFile.close()