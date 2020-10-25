# Librerias
import re
import sys
import string
import math

# Lib RNA
import keras
from keras.models import Sequential
from keras.layers import Flatten
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop

# Nummpy
import numpy as np

# Libreria adicional - Funciones adicionales
from zLibs.Funciones import generarStrEQ
from zLibs.Funciones import cargarListaRV
from zLibs.Funciones import cargarListaCL
from zLibs.Funciones import generarObjetoRofV

# Codificación a utilizar
sys.stdout.encoding
'UTF-8'

# Cargar, generar y recuperar diccionario
listRV_Eng = cargarListaRV("./2_Resultados/2_1_Eng_bibliaRofV_Datos.csv")
listCL_Eng = cargarListaCL("./2_Resultados/2_1_Eng_bibliaRofV_Verbos.csv")

listRV_Spa = cargarListaRV("./2_Resultados/2_1_Spa_bibliaRofV_Datos.csv")
listCL_Spa = cargarListaCL("./2_Resultados/2_1_Spa_bibliaRofV_Verbos.csv")

# Construir elementos RofV
diccRV_Eng, diccEQ_Eng, xTrainBase, yTrainBase = generarObjetoRofV(listRV_Eng, listCL_Eng)
diccRV_Spa, diccEQ_Spa, xTestBase, yTestBase = generarObjetoRofV(listRV_Spa, listCL_Spa)

# Generar cadena con datos equivalencia: VERBO - NÚMERO
strEQ_Eng = generarStrEQ(diccEQ_Eng)
strEQ_Spa = generarStrEQ(diccEQ_Spa)

# Guardar documento de equivalencias
with open('./2_Resultados/3_1_EQ_Eng_Verbo-Numero.txt', 'w', encoding="utf-8") as myFile:
    # Grabar diccionario ordenado en archivo de texto
    myFile.write(strEQ_Eng)
    myFile.close()

# Guardar documento de equivalencias
with open('./2_Resultados/3_1_EQ_Spa_Verbo-Numero.txt', 'w', encoding="utf-8") as myFile:
    # Grabar diccionario ordenado en archivo de texto
    myFile.write(strEQ_Spa)
    myFile.close()

# Ajustes de X y Y, train y test
v_xTrain = np.array(xTrainBase)
v_yTrain = np.array(yTrainBase)
v_xTest = np.array(xTestBase)
v_yTest = np.array(yTestBase)

# Variables RNA
batchSize = 128
epochs = 24

# Cambiar el tipo a flotante para que se acepten números con punto decimal
v_xTrain = v_xTrain.astype('float32')
v_xTest = v_xTest.astype('float32')

'''
# Convertir digitos en arreglo, a su equivalente entre 0 y 1
v_xTrain /= 255
v_xTest /= 255
'''

# Variables de Ajuste
numClasses = 5

# Cambiar eje Y por su categoria
v_yTrain = keras.utils.to_categorical(yTrainBase, numClasses)
v_yTest = keras.utils.to_categorical(yTestBase, numClasses)

# Modelo RNA
model = Sequential()

# Definir modelo con 4 capas
model.add(Dense(64, activation='relu', input_shape=(4,)))
model.add(Dropout(0.2))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.6))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.6))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(numClasses, activation='softmax'))

# Formalizar modelo
model.summary()

# Determina la función de costo que utilizará para calcular la derivada del gradiente
model.compile(loss='categorical_crossentropy',
              optimizer=RMSprop(),
              metrics=['accuracy'])

# Entrenar modelo
history = model.fit(v_xTrain, v_yTrain,
                    batch_size=batchSize,
                    epochs=epochs,
                    verbose=1,
                    validation_data=(v_xTest, v_yTest))

# Evaluar entrenamiento
score = model.evaluate(v_xTest, v_yTest, verbose=0)

# Mostrar perdida y presición
strNota = ""
strNota += ("%s: %.2f%%" % ("Perdida:", score[0]*100)) + "\n"
strNota += ("%s: %.2f%%" % ("Presición", score[1]*100)) + "\n"

# Guardar diccionarios de frecuencias
with open('./2_Resultados/3_2_NotaRNA.txt', 'w', encoding="utf-8") as myFile:
	# Finalizar texto
	myFile.write(strNota)
	myFile.close()

# Salvar modelo
model.save("./2_Resultados/3_3_Modelo_RNA.h5")