# Librerias XML
import xml.dom.minidom as miniDom
import xml.etree.ElementTree as ET

# Para graficos
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D

# Libreria NLTK
import nltk
from nltk.metrics.distance import edit_distance

# Nummpy
import numpy as np

# LECTURA XML
# ------------------------------
# Cargar versos de Documento XML
def cargarVersos (ruta_archivo):
    # Variable para versos
    ary_verses = []
    # Cargar/Parsear documento
    doc = miniDom.parse(ruta_archivo)
    # Recupera nodos verso
    list_verses = doc.getElementsByTagName("seg")
    # Recorrer nodos verso
    for temp_verse in list_verses:
        # Limpiar texto de nodo versos pasarlos a letras minusculas
        temp_texver = temp_verse.childNodes[0].nodeValue.strip().lower()
        # Validar si agregar texto a lista de versos
        if temp_texver not in ary_verses:
            # Agregar verso a lista de versos
            ary_verses.append(temp_texver)
    # Regresar lista de versos
    return ary_verses

# GENERAR CADENA: VERBO - NÚMERO
# ------------------------------
# Generar cadena de relación VERBO - NÚMERO
def generarStrEQ (dicc_eq):
    # Variables
    eq_text = ""
    # Recorrer diccionario de equivalencias
    for verbo, numero in dicc_eq.items():
        # Armar cadena de equivalencias
        eq_text += verbo + ":" +  str(numero) + "\n"
    # Regresar resultado
    return eq_text

# GENERAR CSV
# ------------------------------
# Generar archivo CSV
def generarStrCSV (dicc_verses):
    # Variables
    csv_line = ""
    csv_text = ""
    # Recorrer diccionario
    for num_doc, data_doc in dicc_verses.items():
        csv_line += str(num_doc) + "\t"
        dicc_verbos = data_doc["Verbos"]
        ary_segmentos = data_doc["Segmentos"]
        # Validar diccionario de verbos
        if len(dicc_verbos) > 0:
            # Recorrer verbos
            for verbo, data_verbo in dicc_verbos.items():
                csv_line += str(verbo) + "_" + str(data_verbo["Apariciones"]) + "_"
                # Validar diccionario de formas de verbo
                if len(data_verbo["Formas"]) > 0:
                    # Recorrer formas del verbo
                    for frm_vrb in data_verbo["Formas"]:
                        csv_line += str(frm_vrb) + "@"
                    # Remover el último caracter
                    csv_line = csv_line[:-1]
                # Agregar separador
                csv_line += "|"
            # Remover el último caracter
            csv_line = csv_line[:-1]
        else:
            # Agregar linea falsa
            csv_line += "_" + str(0) + "_"
        # Agregar divisor
        csv_line += "\t"
        # Validar diccionario segmentos
        if len(ary_segmentos) > 0:
            # Recorrer segmentos
            for sentence in ary_segmentos:
                # Agregar separador
                csv_line += sentence + "|"
            # Remover el último caracter
            csv_line = csv_line[:-1]
        # Agregar linea a texto final
        csv_text += csv_line + "\n"
        csv_line = ""
    # Devolver resultado
    return csv_text

# LECTURA CSV
# ------------------------------
# Cargar Documento CSV
def cargarDocumentoCSV(ruta_archivo):
    # Variables
    dicc_versos = {}
    dicc_verbos = {}
    list_corpus = []
    # Leer documento # open(archivo, encoding="latin-1")
    with open(ruta_archivo, 'r', encoding="utf-8") as myFile:
        # Recuperar lineas del archivo
        lineas_archivo = myFile.readlines()
        # Cerrar archivo
        myFile.close()
        # Recorrer lineas del archivo
        for linea_data in lineas_archivo:
            # Dividir lineas en sus partes
            linea_partes = linea_data.split("\t")
            # Partes de la linea
            doc_id = int(linea_partes[0].strip())
            doc_ary_verb = linea_partes[1].strip()
            doc_ary_corpus = linea_partes[2].strip()
            # Dividir
            doc_ary_verb = doc_ary_verb.split("|")
            doc_ary_corpus = doc_ary_corpus.split("|")
            # Asignar contenido en diccionario
            dicc_versos[doc_id] = {}
            dicc_versos[doc_id]["Verbos"] = {}
            dicc_versos[doc_id]["Corpus"] = []
            # -- Recorrer verbos
            for data_verb in doc_ary_verb:
                # Dividir data de verbo en partes
                data_ary_verb = data_verb.split("_")
                # Variables temporales con data de verbo
                temp_verb_value = data_ary_verb[0].strip()
                temp_verb_repit = data_ary_verb[1].strip()
                temp_verb_forms = data_ary_verb[2].strip()
                # Asignar contenido en diccionario
                dicc_versos[doc_id]["Verbos"][temp_verb_value] = {}
                dicc_versos[doc_id]["Verbos"][temp_verb_value]["Apariciones"] = int(temp_verb_repit)
                temp_ary_forms = dicc_versos[doc_id]["Verbos"][temp_verb_value]["Formas"] = temp_verb_forms.split("@")
                # Validar existencia en diccionario de verbos
                if temp_verb_value not in dicc_verbos:
                    # Agregar forma de un verbo al diccionario de verbos
                    dicc_verbos[temp_verb_value] = temp_ary_forms
                else:
                    # Agregar forma de un verbo al diccionario de verbos
                    dicc_verbos[temp_verb_value] = list(set().union(dicc_verbos[temp_verb_value], temp_ary_forms))
            #-- Recorrer corpus
            for data_token in doc_ary_corpus:
                # Limpiar data token
                data_tkn = data_token.strip()
                # Asignar contenido en diccionario
                dicc_versos[doc_id]["Corpus"].append(data_tkn)
            # Asignar corpus
            list_corpus.append(dicc_versos[doc_id]["Corpus"])
    # Regresar diccionario
    return dicc_versos, dicc_verbos, list_corpus

# CARGAR DOCUMENTO DE TEXTO
# ------------------------------
# Cargar Documento de texto
def cargarDocumentoTXT(ruta_archivo):
    # Variables
    txt_data = ""
    # Leer documento # open(archivo, encoding="latin-1")
    with open(ruta_archivo, 'r', encoding="utf-8") as myFile:
        # Recuperar contenido del archivo
        txt_data = myFile.read()
        # Cerrar archivo
        myFile.close()
        # Ajustar texto recuperado
        txt_data = txt_data.strip()
    # Devolver resultado
    return txt_data

# LECTURA DE EQUIVALENCIAS
# ------------------------------
# Cargar Documento de equivalencias
def cargarDocumentoEQ(ruta_archivo):
    # Variables
    dicc_eq = {}
    # Leer documento # open(archivo, encoding="latin-1")
    with open(ruta_archivo, 'r', encoding="utf-8") as myFile:
        # Recuperar lineas del archivo
        lineas_archivo = myFile.readlines()
        # Cerrar archivo
        myFile.close()
        # Recorrer lineas del archivo
        for linea_data in lineas_archivo:
            # Validar linea
            if linea_data != "":
                # Recupera valores de linea
                ary_data = linea_data.split(":")
                verbo = ary_data[0].strip()
                num = int(ary_data[1].strip())
                # Agregar a diccionario de equivalencias
                dicc_eq[verbo] = num
    # Regresar diccionario
    return dicc_eq

# CALCULAR MATRIZ DE RofV
# ------------------------------
# Generar Matriz de RofV (Revisión de Verbos)
def generarColeccionesRofV(list_obj_verbs, dicc_verbos, list_corpus):
    # Variables - VERBO y FORMAS
    dicc_vf = {} # Formato {verbo1:{Forma1: [{col1:valor, col2:valor}],... } }
    # Variables - Trabaja conformas del verbo
    dicc_rv = {} # Formato {Forma1:[{col1:valor, col2:valor}] }
    list_rv = [] # Formato [{col1:valor, col2:valor},{col1:valor, col2:valor}]
    dicc_cl = {} # Formato {Forma1: [pos1 de list_rv, pos2 de list_rv]
    list_cl = [] # Formato [{col1:verbo, col2: formas_verbo}] # Dice: [posX de list_rv] es de VERBO X
    # Variables
    num_fila = 0
    # Revisión de Verbos
    for list_tokens in list_corpus:
        # Recorrer diccionario de verbos
        for verbo, formas in dicc_verbos.items():
            # -------------------------------
            # Validar si es un verbo objetivo
            if verbo in list_obj_verbs:
                # Validar existencia de verbo en diccionario VERBO-FORMA
                if verbo not in dicc_vf:
                    # Se inicializa con verbo diccionario VERBO-FORMA
                    dicc_vf[verbo] = {}
                # Variable de forma
                strFrms = ""
                # Recorrer Formas del verbo
                for frm in formas:
                    # Validar existencia de forma en diccionario VERBO-FORMA
                    if frm not in dicc_vf[verbo]:
                        # Se inicializa con forma diccionario VERBO-FORMA
                        dicc_vf[verbo][frm] = []
                    # Validar inicialización de verbo en diccionario RV
                    if frm not in dicc_rv:
                        # Inicialización de verbo en diccionario RV
                        dicc_rv[frm] = []
                    # Validar inicialización de verbo en diccionario CL
                    if frm not in dicc_cl:
                        # Inicialización de verbo en diccionario CL
                        dicc_cl[frm] = []
                    # Concatenar forma
                    strFrms += (frm + "|")
                # Remover el último caracter
                strFrms = strFrms[:-1]
                # Recorrer Formas del verbo
                for frm in formas:
                    # Validar si existe forma en lista de tokens
                    if frm in list_tokens:
                        # Variables de apoyo
                        str_tkns_left = ""
                        # Recorrer lista de tokens
                        for i in range(len(list_tokens)):
                            # Recupera valor del token segun posicion
                            tkn_i = list_tokens[i]
                            # Validar si token es igual que la forma del verbo
                            if tkn_i == frm:
                                # Variables de apoyo
                                str_tkns_right = ""
                                # Sub-Recorrido de lista de tokens
                                for j in range(len(list_tokens)):
                                    # Validar
                                    if j >= (i + 1):
                                        # Incrementar aservo derecho
                                        tkn_j = list_tokens[j]
                                        # Incrementar aservo izquierdo
                                        str_tkns_right += tkn_j
                                # Calcular distancia de verbo vs texto (step 1)
                                dista_left = edit_distance(str_tkns_left, frm)
                                dista_right = edit_distance(frm, str_tkns_right)
                                # Incrementar aservo izquierdo y derecho
                                str_tkns_left = str_tkns_left + tkn_i
                                str_tkns_right = tkn_i + str_tkns_right
                                # Calcular distancia de verbo vs texto (step 1)
                                dista_lv = edit_distance(str_tkns_left, frm)
                                dista_rv = edit_distance(frm, str_tkns_right)
                                # Agregar resultado a diccionario RV
                                fila_rv = {}
                                fila_rv["DLsv"] = dista_left
                                fila_rv["DLcv"] = dista_lv
                                fila_rv["DRcv"] = dista_rv
                                fila_rv["DRsv"] = dista_right
                                # Agregar fila a diccionario RV
                                dicc_rv[frm].append(fila_rv)
                                dicc_vf[verbo][frm].append(fila_rv)
                                # Agregar fila a lista RV
                                list_rv.append(fila_rv)
                                list_cl.append({"Verbo": verbo, "Formas": strFrms})
                                # Agregar fila a diccionario CL
                                dicc_cl[frm].append(num_fila)
                                num_fila += 1
                            else:
                                # Incrementar aservo izquierdo
                                str_tkns_left += tkn_i
    # Regresar resultado
    return dicc_vf, dicc_rv, list_rv, dicc_cl, list_cl

# CALCULAR OBJETO CON DISTANCIAS
# ------------------------------
# Generar objeto con distancias
def genColeccionDeDists(ary_spv, ary_tkns):
    # Variables
    dicc_dist = {}
    # Recorrer tokens
    for v in range(len(ary_spv)):
        # Recuperar valor de supuesto verbo
        supuesto_v = ary_spv[v]
        # Validar existencia en diccionario de distancias
        if supuesto_v not in dicc_dist:
            # Inicializar supuesto verbo en diccionario
            dicc_dist[supuesto_v] = []
        # Variables de apoyo
        str_tkns_left = ""
        # Recorrer lista de tokens
        for i in range(len(ary_tkns)):
            # Recupera valor del token segun posicion
            tkn_i = ary_tkns[i]
            # Validar si token es igual que la forma del verbo
            if tkn_i == supuesto_v:
                # Variables de apoyo
                str_tkns_right = ""
                # Sub-Recorrido de lista de tokens
                for j in range(len(ary_tkns)):
                    # Validar
                    if j >= (i + 1):
                        # Incrementar aservo derecho
                        tkn_j = ary_tkns[j]
                        # Incrementar aservo izquierdo
                        str_tkns_right += tkn_j
                # Calcular distancia de verbo vs texto (step 1)
                dista_left_sv = edit_distance(str_tkns_left, supuesto_v)
                dista_right_sv = edit_distance(supuesto_v, str_tkns_right)
                # Incrementar aservo izquierdo y derecho
                str_tkns_left = str_tkns_left + tkn_i
                str_tkns_right = tkn_i + str_tkns_right
                # Calcular distancia de verbo vs texto (step 1)
                dista_left_cv = edit_distance(str_tkns_left, supuesto_v)
                dista_right_cv = edit_distance(supuesto_v, str_tkns_right)
                # Generar fila con distancias
                fila_cd = []
                fila_cd.append(dista_left_sv) # DLsv
                fila_cd.append(dista_left_cv) # DLcv
                fila_cd.append(dista_right_cv) # DRcv
                fila_cd.append(dista_right_sv) # DRsv
                # Agregar fila a diccionario de distancias
                dicc_dist[supuesto_v].append(fila_cd)
            else:
                # Incrementar aservo izquierdo
                str_tkns_left += tkn_i
    # Regresar resultado
    return dicc_dist

# MÉTODOS PARA GRÁFICOS
# ------------------------------
# Corregir ejes X y Y
def corregirEjesXY (dicc_vf):
    # Variables
    aryVerbs = []
    aryXsv = [] # Tam: 4 * n, [[v1,v2,...,vn], [v1,v2,...,vn], [v1,v2,...,vn], [v1,v2,...,vn]]
    aryYsv = [] # Tam: 4 * n, [[v1,v2,...,vn], [v1,v2,...,vn], [v1,v2,...,vn], [v1,v2,...,vn]]
    aryXcv = [] # Tam: 4 * n, [[v1,v2,...,vn], [v1,v2,...,vn], [v1,v2,...,vn], [v1,v2,...,vn]]
    aryYcv = [] # Tam: 4 * n, [[v1,v2,...,vn], [v1,v2,...,vn], [v1,v2,...,vn], [v1,v2,...,vn]]
    maxInXY = 0
    # Recorrer diccionario RofV
    for verbo_x, dicc_f in dicc_vf.items():
        # Variables
        ejeXsv = []
        ejeYsv = []
        ejeXcv = []
        ejeYcv = []
        # Salvar verbo actual
        aryVerbs.append(verbo_x)
        # Recorrer diccionario de Formas
        for formaX, datosY in dicc_f.items():
            # Recorrer datos de matriz Y
            for diccD in datosY:
                # Recuperar valores
                ejeXsv.append(diccD["DRsv"])
                ejeYsv.append(diccD["DLsv"])
                ejeXcv.append(diccD["DRcv"])
                ejeYcv.append(diccD["DLcv"])
        # Ajuste de tamaño o loguitud
        if maxInXY < len(ejeXsv):
            # Actualizar maximo
            maxInXY = len(ejeXsv)
        # Resguardar valores X y Y
        aryXsv.append(ejeXsv)
        aryYsv.append(ejeYsv)
        aryXcv.append(ejeXcv)
        aryYcv.append(ejeYcv)
    # Recorrer ejes X y Y
    for i in range(len(aryXsv)):
        # Validar longitud
        while maxInXY > len(aryXsv[i]):
            # Ajustar de longitud
            aryXsv[i].append(0)
            aryYsv[i].append(0)
            aryXcv[i].append(0)
            aryYcv[i].append(0)
    # Regresar resultados
    return aryXsv, aryYsv, aryXcv, aryYcv, aryVerbs

'''
# Generar matriz de colores
def generarMatrizColores(nx, ny):
# Variables
    vcolors = []
    tam_x = len(nx)
    tam_y = len(nx[0])
    # Recorrer eje X
    for i in range(tam_x):
        # Arreglo auxiliar
        vaxcolrs = []
        coloraux = np.random.sample()
        # Recorrer eje Y
        for j in range(tam_y):
            # Agregar color en arreglo de colores
            vaxcolrs.append(coloraux)
        # Salvar colores
        vcolors.append(vaxcolrs)
    # Regresar colores
    return vcolors
'''

# Generar Scatterplot
def construirScatterPlot2D (vc, nx, ny, label_x, label_y, titulo, ruta_archivo):
    # ScatterPlot
    fig = plt.figure()
    # Recorrer verbos
    for i in range(len(nx)):
        # Agregar conjuntos
        plt.scatter(nx[i], ny[i], c=vc[i])
    # Detalles
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.title(titulo)
    fig.savefig(ruta_archivo, dpi=300, quality=80, optimize=True, progressive=True)

# LECTURA CSV
# ------------------------------
# Cargar Documento CSV con listaRV
def cargarListaRV(ruta_archivo):
    # Variable de listaRV
    list_rv = []
    num_fila = 0
    # Leer documento # open(archivo, encoding="latin-1")
    with open(ruta_archivo, 'r', encoding="utf-8") as myFile:
        # Recuperar lineas del archivo
        lineas_archivo = myFile.readlines()
        # Cerrar archivo
        myFile.close()
        # Recorrer lineas del archivo
        for linea_data in lineas_archivo:
            # Validar, para no contar la primer fila
            if num_fila > 0:
                # Dividir lineas en sus partes
                valores_rv = linea_data.split(",")
                # Preparar filaRV
                fila_rv = {}
                # Asignar valores a fila
                fila_rv["DLsv"] = int(valores_rv[0].strip())
                fila_rv["DLcv"] = int(valores_rv[1].strip())
                fila_rv["DRcv"] = int(valores_rv[2].strip())
                fila_rv["DRsv"] = int(valores_rv[3].strip())
                # Agregar fila a listaRV
                list_rv.append(fila_rv)
            # Incrementar numero de fila
            num_fila += 1
    # Regresar resultado
    return list_rv

# Cargar Documento CSV con listaCL
def cargarListaCL(ruta_archivo):
    # Variable de listaCL
    list_cl = []
    num_fila = 0
    # Leer documento # open(archivo, encoding="latin-1")
    with open(ruta_archivo, 'r', encoding="utf-8") as myFile:
        # Recuperar lineas del archivo
        lineas_archivo = myFile.readlines()
        # Cerrar archivo
        myFile.close()
        # Recorrer lineas del archivo
        for linea_data in lineas_archivo:
            # Validar, para no contar la primer fila
            if num_fila > 0:
                # Dividir lineas en sus partes
                valores_cl = linea_data.split(",")
                # Preparar filaCL
                fila_cl = {}
                # Asignar valores a fila
                fila_cl["Verbo"] = valores_cl[0].strip()
                fila_cl["Formas"] = valores_cl[1].strip()
                # Agregar fila a listaCL
                list_cl.append(fila_cl)
            # Incrementar numero de fila
            num_fila += 1
    # Regresar resultado
    return list_cl

# GENERAR OBJETO RofV
# ------------------------------
# Generar objeto RofV
def generarObjetoRofV(list_rv, list_cl):
    # Variables
    dicc_rv = {}
    dicc_eq = {}
    x_base = []
    y_base = []
    num_clases = 0
    # Recorrer listas
    for i in range(len(list_rv)):
        # Recupera objeto RV y CL
        objRV = list_rv[i]
        objCL = list_cl[i]
        # Recuperar verbo objetivo
        temp_verbo = objCL["Verbo"]
        # Validar contenido de diccionario
        if temp_verbo not in dicc_rv:
            # Inicializar contenedor
            num_clases += 1
            dicc_rv[temp_verbo] = []
            dicc_eq[temp_verbo] = num_clases
        # Crear arreglo de datos RV
        temp_data = [objRV["DLsv"], objRV["DLcv"], objRV["DRcv"], objRV["DRsv"]]
        # Agregar datos en diccionario
        dicc_rv[temp_verbo].append(temp_data)
        # Agregar datos a X y Y train
        x_base.append(temp_data)
        y_base.append(dicc_eq[temp_verbo])
    # Regresar resultados
    return dicc_rv, dicc_eq, x_base, y_base


# GENERAR DICCIONARIO DE PREDICCIONES
# ------------------------------
# Generar diccionario de predicciones
def generarDiccPredicciones(x_data, y_data, dicc_eq, modelo_rna):
    # Variables
    dicc_predict = {}
    # Recorrer lista de distancias
    for i in range(len(x_data)):
        # Recupera arreglo de distancias
        fila_dist = x_data[i]
        # Generar vector para evaluación
        v_xData = np.array(fila_dist)
        # Ajustar vector para evaluación
        v_xData = v_xData.astype('float32')
        v_xData = v_xData.reshape(1, 4)
        # Realizar evaluación a travez del modelo
        predi = modelo_rna.predict(v_xData)
        clase = modelo_rna.predict_classes(v_xData)
        # Variable de verbo:
        vlr_verbo = ""
        num_clas = 0
        # Validar origen del valor verbo
        if y_data != None and len(y_data) > 0:
            # Recupera clase
            num_clas = y_data[i]
            # Recupera verbo que corresponde a clase
            vlr_verbo = obtenerVerb_PorNum(dicc_eq, num_clas)
        # Validar existencia de supuesto verbo en diccionario de predicciones
        if vlr_verbo not in dicc_predict:
            # Inicializar supuesto verbo en diccionario de predicciones
            dicc_predict[vlr_verbo] = {}
            dicc_predict[vlr_verbo]["Num"] = num_clas
            dicc_predict[vlr_verbo]["Res"] = {}
        # Validar existencia de clase en diccionario de predicciones
        if clase[0] not in dicc_predict[vlr_verbo]["Res"]:
            # Inicializar sclase en diccionario de predicciones
            dicc_predict[vlr_verbo]["Res"][clase[0]] = []
        # Agregar datos de prediccion a diccionario de predicciones
        dicc_predict[vlr_verbo]["Res"][clase[0]].append(predi.max())
    # Resultados
    return dicc_predict

# Función que obtien el verbo y su clase/número
def obtenerVerb_PorNum(dicc_eq, num_clas):
    # Variable de verbo:
    vlr_verbo = ""
    # Recorrer diccionario de equivalencias
    for vl_eq, nm_eq in dicc_eq.items():
        # Validar si se encuentra equivalencia
        if num_clas == nm_eq:
            # Asignar valor de verbo
            vlr_verbo = vl_eq
    # Regresar resultado
    return vlr_verbo