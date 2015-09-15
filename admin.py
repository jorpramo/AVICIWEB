__author__ = 'jpradas'

from flask_admin import Admin
from flask import Flask, redirect, request
from flask import render_template, jsonify
from flask import url_for, redirect
from bbdd import servicios
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from collections import defaultdict



app = Flask(__name__)
GoogleMaps(app)

admin = Admin(app, name='Avici', template_mode='bootstrap3')
# Add administrative views here


# Flask views
@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))

@app.route('/sistemas/')
def sistemas():
    items=[]
    s=servicios()
    items=s.LeeServicios()
    return render_template('sistemas.html', items=items)

@app.route('/_datos_total/<nombre>')
def comparativa(nombre):
    coordenadas=[]
    s=servicios()
    datos=s.obtencoordenadas(nombre)
    #datos=[{'disp': 1.0, '_id': {'nombre': 'Valenbisi', 'estacion': '006_GUILLEN_CASTRO_CON_CALLE_SAN_PEDRO_PASCUAL'}, 'lib': 11.0, 'total': 15.0},{'disp': 2.0, '_id': {'nombre': 'Madrid', 'estacion': '006_GUILLEN_CASTRO_CON_CALLE_SAN_PEDRO_PASCUAL'}, 'lib': 14.0, 'total': 15.0}]
    for d in datos:
        coordenadas.append([d['lib'],d['disp']])
    print(coordenadas)

    return jsonify(output=coordenadas)

@app.route('/compa/')
def Graph_global():
    items=[]
    s=servicios()
    items=s.LeeServicios()
    return render_template('grafica_global.html', items=items)

@app.route('/servicio/<nombre>')
def servicio(nombre):
    s=servicios()
    datos_servicio=s.LeeServicios(nombre, True)
    datos=s.LeeDatos(nombre)
    lista_marcas = defaultdict(list)

    for x in datos_servicio:
        ciudad= x['nombre']
        latitud = x['X']
        longitud = x['Y']

    saturado='/static/jpg/red.png'
    perfecto='/static/jpg/green.png'
    sinbicis='/static/jpg/blue.png'
    porc=0.10
    for d in datos:
        if float(d['disponibles'])<=(float(d['total'])*porc):
            lista_marcas[saturado].append([float(d['X']),float(d['Y'])])
        elif float(d['libres'])<=(float(d['total'])*porc):
            lista_marcas[sinbicis].append([float(d['X']),float(d['Y'])])
        else:
            lista_marcas[perfecto].append([float(d['X']),float(d['Y'])])

    sndmap = Map(
        identifier="sndmap",
        lat=latitud,
        lng=longitud,
        style="width: 100%; height: 80%",
        markers=lista_marcas)

    return render_template('servicio.html', datos_servicio=ciudad, sndmap=sndmap,porc=porc)

app.run(debug=True)