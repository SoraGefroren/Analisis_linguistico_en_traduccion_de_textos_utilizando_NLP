# FUENTE DE DATOS
# -----------------------------------------------------------
rutaArchivoEng = "./1_BibliaParalelo/English.xml" # "./1_BibliaParalelo/__MiniEng.xml"
rutaArchivoSpa = "./1_BibliaParalelo/Spanish.xml" # "./1_BibliaParalelo/__MiniSpa.xml"

# -----------------------------------------------------------
# -----------------------------------------------------------
# -----------------------------------------------------------

# Sy
import spacy

# Load English tokenizer, tagger, parser, NER and word vectors
# python -m spacy download en_core_web_md
nlpEng = spacy.load("en_core_web_md")
# python -m spacy download es_core_news_md
nlpSpa = spacy.load("es_core_news_md")

# Librerias
import re
import sys
import json
import string

# Libreria NLTK
import nltk
from nltk.tokenize.toktok import ToktokTokenizer

# Libreria adicional
from zLibs.Funciones import cargarVersos
from zLibs.Funciones import generarStrCSV

# Codificación a utilizar
sys.stdout.encoding
'UTF-8'

# Iniciar Tokenizador
toktok = ToktokTokenizer()

# Recuperar versos de XML
listVersosEng = cargarVersos(rutaArchivoEng)
listVersosSpa = cargarVersos(rutaArchivoSpa)

# GENERAR OBJETO/DICCIONARIO
# ------------------------------
# Analizar y generar objeto/diccionario
def analizarVersos (nlpX, ary_verses):
    # Variables de diccionario
    num_verse = 0
    dicc_verses = {}
    dicc_frevbs = {}
    # Recorrer lista de versos
    for verso in ary_verses:
        # Procesar verso
        verDoc = nlpX(verso)
        # Variables
        ary_formas = []
        dicc_verbos = {}
        dicc_verses[num_verse] = {}
        # Analizar sintaxis
        for token in verDoc:
            # Si es un Verbo
            if token.pos_ == "VERB":
                # Recuperar verbo
                temp_verbo = token.lemma_
                tmp_r_verb = token.text
                # Validar existencia de verbo en el diccionario
                if temp_verbo not in dicc_verbos:
                    dicc_verbos[temp_verbo] = {}
                    dicc_verbos[temp_verbo]["Formas"] = []
                    dicc_verbos[temp_verbo]["Apariciones"] = 1
                else:
                    dicc_verbos[temp_verbo]["Apariciones"] += 1
                # Validar existencia de verbo en frecuencia de verbos
                if temp_verbo not in dicc_frevbs:
                    dicc_frevbs[temp_verbo] = {}
                    dicc_frevbs[temp_verbo]["Formas"] = []
                    dicc_frevbs[temp_verbo]["Apariciones"] = 1
                else:
                    dicc_frevbs[temp_verbo]["Apariciones"] += 1
                # Validar existencia de verbo en frecuencia de verbos
                if tmp_r_verb not in dicc_frevbs[temp_verbo]["Formas"]:
                    dicc_frevbs[temp_verbo]["Formas"].append(tmp_r_verb)
                # Guardar formas
                if tmp_r_verb not in ary_formas:
                    ary_formas.append(tmp_r_verb)
                    dicc_verbos[temp_verbo]["Formas"].append(tmp_r_verb)
        # Agregar conteo de verbos
        dicc_verses[num_verse]["Verbos"] = dicc_verbos
        # -----------------------------
        # Tokenizar verso
        ary_segmentos = []
        # verso_parrafo = verso
        list_tkns = toktok.tokenize(verso)
        # Recorrer tokens
        for tkn in list_tkns:
            # Agregar token
            ary_segmentos.append(tkn.strip())
        # Agregar segmentos
        dicc_verses[num_verse]["Segmentos"] = ary_segmentos
        # -----------------------------
        # Incrementar contador de verso
        num_verse += 1
    # Regresar resultado
    return dicc_verses, dicc_frevbs

# Analizar versos recuperados
diccVersosEng, diccFrecVerbEng = analizarVersos(nlpEng, listVersosEng)
diccVersosSpa, diccFrecVerbSpa = analizarVersos(nlpSpa, listVersosSpa)

# Generar archivo CSV
strCsvEng = generarStrCSV(diccVersosEng)
strCsvSpa = generarStrCSV(diccVersosSpa)

# Guardar resultados
with open('./2_Resultados/1_1_bibliaDataTab-Eng.csv', 'w', encoding="utf-8") as myFile:
    # Grabar diccionario ordenado en archivo de texto
    myFile.write(strCsvEng)
    myFile.close()

# Guardar resultados
with open('./2_Resultados/1_1_bibliaDataTab-Spa.csv', 'w', encoding="utf-8") as myFile:
    # Grabar diccionario ordenado en archivo de texto
    myFile.write(strCsvSpa)
    myFile.close()

# Función para apoyar la organización del diccionario
def keyFuncLambda(item):
    key, subDic = item
    return subDic["Apariciones"]

# Ordenar diccionario de frencuencias
diccFrOrdEng = sorted(diccFrecVerbEng.items(), key = keyFuncLambda, reverse = True)
diccFrOrdSpa = sorted(diccFrecVerbSpa.items(), key = keyFuncLambda, reverse = True)

# Guardar diccionarios de frecuencias
with open('./2_Resultados/1_2_verbosFrecuencia-Eng.json', 'w', encoding="utf-8") as myFile:
	# Finalizar texto
	myFile.write(json.dumps(diccFrOrdEng, indent=5, ensure_ascii=False))
	myFile.close()

# Guardar diccionarios de frecuencias
with open('./2_Resultados/1_2_verbosFrecuencia-Spa.json', 'w', encoding="utf-8") as myFile:
	# Finalizar texto
	myFile.write(json.dumps(diccFrOrdSpa, indent=5, ensure_ascii=False))
	myFile.close()