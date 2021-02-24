
# -*- coding: utf-8 -*-

import pandas as pd #importar libreria pandas
#import matplotlib.pyplot as plt #importar libreria graficos
import numpy as np # importar Numpy
import csv #importar libreria manejo archivos csv
import json #imoportcion libreria para leer json
from pymongo import MongoClient  # libreria para BBDD Mongo db
import wget  # enlace a url
from flask import Flask  # libreria para servir en web
from flask import request,render_template
import os # libreria para operaciones en S.O.
import pyttsx3 # sinterizador de voz
import webbrowser #libreria para redirigir a url
import cv2 # libreria para analisis imagenes
import uuid # libreria para darle nombre con codigo unico a archivos generados
#import pygame
import msvcrt #libreria para pausar
import threading
import time
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request
import wx

from flask_pymongo import  PyMongo


url = "https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19VacunasAgrupadas.csv"


wget.download(url, 'C:/Users/54112/Desktop/spark/vacunas2.csv')



#LECTURA DOCUMENTO CSV
vacunas = pd.read_csv('vacunas2.csv')

#CSV A DICCIONARIO DE PYTHON
vacunas.to_dict('records')
vacunas.head()

os.system ("cls")

print("--------------------------------------------------------")
print("--------------------------------------------------------")
print("          'VACUNAS APLICADAS POR PROVINCIA'. ")
print("   FUENTE: 'MINISTERIO DE SALUD. REPUBLICA ARGENTINA ' ")
print("           https://www.datos.gob.ar/dataset/")
print("--------------------------------------------------------")
print("--------------------------------------------------------")
print('\n'* 3)





engine = pyttsx3.init()
engine.setProperty('rate', 145)
engine.setProperty('voice' [1], 'spanish')
#engine.setProperty ('voice', voices [0] .id) #cambiar índice, cambiar voces. o para hombre
engine.setProperty('volume', 8)


# It's just a text to speech function..
def saySomething(somethingToSay):
    engine.say(somethingToSay)
    engine.runAndWait()


saySomething("informe de vacunas aplicadas por provincia, primera y segunda dosis. Fuente    ministerio de salud de la república argentina")
saySomething("Presione una tecla para continuar...")
print("Presione una tecla para continuar...")
msvcrt.getch()


#PRESENTACION DEL DOCUMENTO COMO DATAFRAME
saySomething("presentación de la tabla de datos ")
print("INFO DEL DATAFRAME:  ")
print(vacunas.info())
print('\n'* 3)
print(vacunas.describe())
print('\n'* 3)


print("Presione una tecla para continuar...")
msvcrt.getch()




#convertir csv a json

def csv_json(csvFilePath1, jsonFilePath1): 
	
	# CREAMOS DICCIONARIO
	data = {} 
	
	# ABRIMOS Y LEEMOS CSV
	with open(csvFilePath1, encoding='utf-8') as csvf: 
		csvReader = csv.DictReader(csvf) 
		
		
		for rows in csvReader: 
			
		 
			key = rows['jurisdiccion_nombre'] 
			data[key] = rows 


	with open(jsonFilePath1, 'w', encoding='utf-8') as jsonf: 
		jsonf.write(json.dumps(data, indent=4)) 
		

csvFilePath1 = r'vacunas.csv'
jsonFilePath1 = r'vacunas2.json'

csv_json(csvFilePath1, jsonFilePath1)




      
print('\n'* 3)
saySomething("Tabla de datos preprocesados")
info=vacunas[['jurisdiccion_nombre','primera_dosis_cantidad','segunda_dosis_cantidad']]
print(info)
provincias =vacunas[['jurisdiccion_nombre']]





dosis_1 =vacunas[['primera_dosis_cantidad']]


dosis_2 =vacunas[['segunda_dosis_cantidad']]


print('\n'* 3)
saySomething("Presione una tecla para continuar...")
print("Presione una tecla para continuar...")
msvcrt.getch()
'''
#GRAFICO  PRIMERA DOSIS POR PROVINCIA
saySomething("presentación de gráficos")
info.plot.bar(x="jurisdiccion_nombre", y="primera_dosis_cantidad",color="#f44265", lw=3)




plt.xlabel("PROVINCIA", 
           family='sans-serif', 
           color='r', 
           weight='normal', 
           size = 16,
           labelpad = 6)
plt.ylabel('1ra DOSIS',
           family='fantasy', 
           color='g', 
           weight='normal', 
           size = 12,
           labelpad = 6)
           
plt.title("VACUNA COVID 19. PRIMERA DOSIS ",
          position=( 0.5,0.9),
          fontdict={'family': 'serif', 
                    'color' : 'darkblue',
                    'weight': 'bold',
                    'size': 10,
                    })



plt.text(15, 4500, "Hecho en Python y Pandas",fontsize=6,color='r',rotation=270)
plt.savefig('DOSIS1_2.jpg')



#plt.figure(figsize=(10,6))
plt.legend()
plt.show()






#GRAFICO  PRIMERA DOSIS POR PROVINCIA

info.plot.bar(x="jurisdiccion_nombre", y="segunda_dosis_cantidad",color="red", lw=3)

#uso de tabla



plt.xlabel("PROVINCIA", 
           family='sans-serif', 
           color='r', 
           weight='normal', 
           size = 16,
           labelpad = 6)
plt.ylabel('1ra DOSIS',
           family='fantasy', 
           color='g', 
           weight='normal', 
           size = 12,
           labelpad = 6)
           
plt.title("VACUNA COVID 19. SEGUNDA DOSIS ",
          position=( 0.5,0.9),
          fontdict={'family': 'serif', 
                    'color' : 'darkblue',
                    'weight': 'bold',
                    'size': 10,
                    })



plt.text(15, 4500, "Hecho en Python y Pandas",fontsize=6,color='r')
plt.savefig('DOSIS2_2.jpg')



#plt.figure(figsize=(10,6))
plt.legend()
plt.show()

'''
saySomething("creación de colección vacunas aplicadas en base de datos covid 19, de mongo db")
  
#CONEXION A LA BASE DE MONGO DB 
myclient = MongoClient("mongodb://localhost:27017/")  
   
# SELECCION DE BASE DE DATOS
db = myclient["covid"] 
   
#SELECCION DE COLECCON
 
Collection = db["vacunas_aplicadas"] 
  
# CARGA Y LECTURA DE JSON
with open('vacunas.json') as file: 
    file_data = json.load(file) 
      
#INSERTAMOS JSON EN DB
if isinstance(file_data, list): 
    Collection.insert_many(file_data)   
else: 
    Collection.insert_one(file_data) 
    



saySomething("Sirviendo datos a la aplicación web")



app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'
saySomething("gracias por su consulta")







#Se configura el acceso a la base de datos mongodb


app.config['covid'] = 'vacunas_aplicadas'


app.config['MONGO_URI'] = 'mongodb://mongo:27017/empleados'





#Se asocia la configuración pasando la app


mongo = PyMongo(app)





#Se define la ruta raiz con metodo POST


@app.route('/vacunas')


def index():


    #Se realiza la conexion a la coleccion empleados


   vacunas_aplicadas= db.vacunas_aplicadas


    #Se hace la consulta y se devuelve  en formato json_util


   resultados = db.vacunas_aplicadas.find()


   return dumps(resultados)


@app.route('/graficos')


def graficos():
     
    return render_template('graficos.html')








if __name__ == "__main__":


    #Se corre la aplicacion en modo debug


    app.run(debug=True)


