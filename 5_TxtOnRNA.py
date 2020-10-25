# FUENTE DE DATOS
# -----------------------------------------------------------
rutaArchivoTXT = './1_BibliaParalelo/__TEXTO_Eng.txt'

# Librerias
import re
import sys
import json
import string
import math

# Lib RNA
import keras
from keras.models import load_model

# Libreria NLTK
import nltk
from nltk.tokenize.toktok import ToktokTokenizer

# Nummpy
import numpy as np

# Iniciar Tokenizador
toktok = ToktokTokenizer()

# Libreria adicional - Funciones adicionales
from zLibs.Funciones import cargarDocumentoEQ
from zLibs.Funciones import cargarDocumentoTXT
from zLibs.Funciones import genColeccionDeDists

# ELEMENTOS PARA ANÁLISIS
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# Cargar y generar diccionario de equivalencias
diccEQ_Eng = cargarDocumentoEQ('./2_Resultados/3_1_EQ_Eng_Verbo-Numero.txt')
diccEQ_Spa = cargarDocumentoEQ('./2_Resultados/3_1_EQ_Spa_Verbo-Numero.txt')

# Diccionario de disancias
diccDist = {}

# Diccionario de preducciones
diccPredict = {}

# CARGA Y ANÁLISIS DE TEXTO
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# Variables
aryTkns = []

# Cargar texto
txtData = cargarDocumentoTXT(rutaArchivoTXT)

# Tokenizar datos
listTkns = toktok.tokenize(txtData)

# Recorrer tokens
for aTkn in listTkns:
    # Agregar token
    aryTkns.append(aTkn.strip())

# Generar objeto con distancias
diccDist = genColeccionDeDists(aryTkns, aryTkns)

# APLICACIÓN DE LA RNA
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# Cargar y generar RNA
modeloRNA = load_model('./2_Resultados/3_3_Modelo_RNA.h5')

# Ajutar modelo
modeloRNA.summary()

# Recorrer diccionario de distancias
for supuesto_v, list_dist in diccDist.items():
    # Recorrer lista de distancias
    for fila_dist in list_dist:
        # Generar vector para evaluación
        v_xData = np.array(fila_dist)
        # Ajustar vector para evaluación
        v_xData = v_xData.astype('float32')
        v_xData = v_xData.reshape(1, 4)
        # Realizar evaluación a travez del modelo
        predi = modeloRNA.predict(v_xData)
        clase = modeloRNA.predict_classes(v_xData)
        # Validar existencia de supuesto verbo en diccionario de predicciones
        if supuesto_v not in diccPredict:
            # Inicializar supuesto verbo en diccionario de predicciones
            diccPredict[supuesto_v] = {}
        # Validar existencia de clase en diccionario de predicciones
        if clase[0] not in diccPredict[supuesto_v]:
            # Inicializar sclase en diccionario de predicciones
            diccPredict[supuesto_v][clase[0]] = []
        # Agregar datos de prediccion a diccionario de predicciones
        diccPredict[supuesto_v][clase[0]].append(predi.max())

# ANALIZAR RESULTADOS
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# Variable
diccCandis = {}
maxAcc = 1.01
minAcc = 0.25

# Recorrer diccionario de predicciones
for supuesto_v, obj_clases in diccPredict.items():
    # Es aceptado como posible candidato
    es_candidato = True
    # Recorrer clases predichas
    for clase_o, ary_maxis in obj_clases.items():
        # Ajuste
        clase_x = str(clase_o)
        # Suma de los elementos del arreglo
        sumAryM = sum(ary_maxis)
        # Validar si se acepta como candidato
        if sumAryM > 1:
            # No se acepta como candidato
            es_candidato = False
            break
        elif sumAryM >= maxAcc or sumAryM <= minAcc:
            # No se acepta como candidato
            es_candidato = False
            break
        else:
            # Recorrer arreglo
            for valor_m in ary_maxis:
                # Validar si se acepta como candidato
                if valor_m >= maxAcc or valor_m <= minAcc:
                    # No se acepta como candidato
                    es_candidato = False
                    break
            # Validar si salir de ciclo
            if not es_candidato:
                # Salir de ciclo
                break
        # Validar si puede ser candidato
        if es_candidato:
            # Se valida si existe candidato en diccionario
            if supuesto_v not in diccCandis:
                # Se inicializa candidato
                diccCandis[supuesto_v] = {}
            # Se valida si existe clase en diccionario
            if clase_x not in diccCandis:
                # Se inicializa candidato
                diccCandis[supuesto_v][clase_x] = []
            # Recorrer arreglo
            for valor_m in ary_maxis:
                # Se agrega valores de posible candidato
                diccCandis[supuesto_v][clase_x].append(float(valor_m))

# Imprimir candidatos
# print (diccCandis)

# Guardar diccionarios de frecuencias
with open('./2_Resultados/5_resultadoRNA.json', 'w', encoding="utf-8") as myFile:
	# Finalizar texto
	myFile.write(json.dumps(diccCandis, indent=10, ensure_ascii=False))
	myFile.close()