from flask import Flask, render_template
from flask import request
from flask_wtf.csrf import CSRFProtect
from flask import make_response
from flask import flash
import json
import ast
import forms, cajasDinamicas, traductor


class Resistencia():
    colores = [
        [0, '#000000', 'Negro'],
        [1, '#A18262', 'Cafe'],
        [2, '#FF0000', 'Rojo'],
        [3, '#FF8000', 'Naranja'],
        [4, '#FFFF00', 'Amarillo'],
        [5, '#008F39', 'Verde'],
        [6, '#0000FF', 'Azul'],
        [7, '#4C2882', 'Violeta'],
        [8, '#808080', 'Gris'],
        [9, '#FFFFFF', 'Blanco']
    ]
    inputBanda1 = 0
    hexadecimalBanda1 = ''
    nombreBanda1 = ''
    inputBanda2 = 0
    hexadecimalBanda2 = ''
    nombreBanda2 = ''
    inputBanda3 = 0
    hexadecimalBanda3 = ''
    nombreBanda3 = ''
    tol = 0
    val = 0
    min = 0
    max = 0

    def __init__(self, b1, b2, b3, tol):
        self.inputBanda1 = int(b1)
        self.inputBanda2 = int(b2)
        self.inputBanda3 = int(b3)
        self.tol = float(tol)

    def calcularResistencia(self):
        self.val = ((self.inputBanda1 * 10) + self.inputBanda2) * (pow(10, self.inputBanda3))
        self.min = self.val * (1 - self.tol)
        self.max = self.val * (1 + self.tol)
        self.hexadecimalBanda1 = self.colores[self.inputBanda1][1]
        self.nombreBanda1 = self.colores[self.inputBanda1][2]
        self.hexadecimalBanda2 = self.colores[self.inputBanda2][1]
        self.nombreBanda2 = self.colores[self.inputBanda2][2]
        self.hexadecimalBanda3 = self.colores[self.inputBanda3][1]
        self.nombreBanda3 = self.colores[self.inputBanda3][2]
        return self.val
    
    def getinputBanda1(self):
        return self.inputBanda1
    
    def gethexadecimalBanda1(self):
        return self.hexadecimalBanda1
    
    def getnombreBanda1(self):
        return self.nombreBanda1
    
    def getinputBanda2(self):
        return self.inputBanda2
    
    def gethexadecimalBanda2(self):
        return self.hexadecimalBanda2
    
    def getnombreBanda2(self):
        return self.nombreBanda2
    
    def getinputBanda3(self):
        return self.inputBanda3
    
    def gethexadecimalBanda3(self):
        return self.hexadecimalBanda3
    
    def getnombreBanda3(self):
        return self.nombreBanda3
    
    def getTolerancia(self):
        return self.tol
    
    def getMax(self):
        return (self.val * (1 + self.tol))

    def getMin(self):
        return (self.val * (1 - self.tol))
    
    def getValue(self):
        return ((self.inputBanda1 * 10) + self.inputBanda2) * (pow(10, self.inputBanda3))


app = Flask(__name__)
# app.config['SECRET_KEY'] = 'esta es una clave encriptada'
# csrf = CSRFProtect()


@app.route("/")
def formprueba():
    return render_template("formPrueba.html")


@app.route("/Alumnos", methods=['GET','POST'])
def Alumnos():
    reg_alum = forms.UserForm(request.form)
    datos = list()
    if request.method == 'POST':
        datos.append(reg_alum.matricula.data)
        datos.append(reg_alum.nombre.data)
        print(reg_alum.matricula.data)
        print(reg_alum.nombre.data)
        return render_template('Alumnos.html', form = reg_alum, datos = datos, vista = 'post')
    return render_template('Alumnos.html', form = reg_alum, datos = datos, vista = 'get')


@app.route("/cookie", methods=['GET','POST'])
def cookie():
    reg_user = forms.LoginForm(request.form)
    response = make_response(render_template('cookie.html', form = reg_user))
    if reg_user.validate():
        user = reg_user.username.data
        password = reg_user.password.data
        datos = user + '@' + password
        success_message = 'Bienvenido {0}'.format(user)
        response.set_cookie('datis_usuario', datos)
        flash(success_message)
    return response


@app.route("/cajasDinamicas", methods=['POST','GET'])
def CajasDinamicas():
    if request.method == 'POST':
        reg_cajasDinamicas = cajasDinamicas.CajasDinamicasForm(request.form)
        btn = request.form.get("btn")
        if btn == 'Rellenar':
            cajas = int(request.form.get("cajas"))
            return render_template('cajasDinamicas.html',
                                vista = 'numeros',
                                form = reg_cajasDinamicas,
                                cajas = cajas)
        if btn == 'Registrar':
            cajas = request.form.getlist("cajas")
            maxim = max(cajas)
            minim = min(cajas)
            total = 0
            for caja in cajas:
                total = total + int(caja)
            prom = total / len(cajas)
            
            arrRep = []
            for n in cajas:
                arr = [ n, cajas.count(n) ]
                if arr not in arrRep:
                    arrRep.append( [n, cajas.count(n)] )
            arrMostrado = []
            for rep in arrRep:
                if rep[1] != 1:
                    arrMostrado.append(rep)
            textoMostradoDuplicados = 'No hay número duplicados'
            if len(arrMostrado) > 0:
                textoMostradoDuplicados = '<p>Los siguientes números se repiten</p>'
                for arr in arrMostrado:
                    textoMostradoDuplicados += '<p>El número {0} se repite {1} veces </p>'.format(arr[0], arr[1])
            return render_template('cajasDinamicas.html',
                                vista = 'resultados',
                                maxim = maxim,
                                minim = minim,
                                prom = prom,
                                textoMostradoDuplicados = textoMostradoDuplicados,
                                form = reg_cajasDinamicas)
    return render_template('cajasDinamicas.html', vista = 'cajas')


@app.route("/traductor", methods=['POST','GET'])
def Traductor():
    if request.method == 'POST':
        reg_traductor = traductor.TraslaterForm(request.form)
        btn = request.form.get("btn")
        if btn == 'Guardar':
            spanish = request.form.get("txtSpanish")
            english = request.form.get("txtEnglish")
            if spanish == '' or english == '':
                print('No se han rellenado los archivos')
            else:
                arr = []
                arr.append(spanish.upper())
                arr.append(english.upper())
                text = str(arr)
                f = open('diccionario.txt', 'a')
                f.write('\n')
                f.write(text)
                f.close()
            return render_template('traductor.html',
                                vista = 'Guardar',
                                form = reg_traductor)
        if btn == 'Traducir':
            textToTraslate = request.form.get("txtTextToTraslate").upper()
            optionToTraslate = request.form.get("rdLanguage")
            f = open('diccionario.txt', 'r')
            diccionario = f.readlines()
            diccionarioLimpio = []
            for item in diccionario:
                realItem = item.replace('\n', '')
                arrRealItem = realItem.split("'")
                if len(arrRealItem) > 1:
                    s = arrRealItem[1]
                    e = arrRealItem[3]
                    diccionarioLimpio.append([s, e])
            traduccion = ''
            if optionToTraslate == 'english':
                for d in diccionarioLimpio:
                    textoComparado = d[0]
                    if textToTraslate == textoComparado:
                        traduccion = d[1]
            if optionToTraslate == 'spanish':
                for d in diccionarioLimpio:
                    textoComparado = d[1]
                    if textToTraslate == textoComparado:
                        traduccion = d[0]
            textTraslated = 'No se ha encontrado traducción'
            if traduccion != '':
                textTraslated = 'El texto traducido es: ' + traduccion
            return render_template('traductor.html',
                                vista = 'Traducir',
                                textTraslated = textTraslated,
                                form = reg_traductor)
    return render_template('traductor.html')


@app.route("/resistencias", methods=['GET','POST'])
def Resistencias():
    if request.method == 'POST':
        btn = request.form.get("btn_submit")
        if btn == 'Evaluar':
            ibanda1 = int(request.form.get("banda1"))
            ibanda2 = int(request.form.get("banda2"))
            ibanda3 = int(request.form.get("banda3"))
            tol = float(request.form.get("tolerancia"))
            val = ((ibanda1 * 10) + ibanda2) * (pow(10, ibanda3))
            min = val * (1 - tol)
            max = val * (1 + tol)
            colores = [
                [0, '#000000', 'Negro'],
                [1, '#A18262', 'Cafe'],
                [2, '#FF0000', 'Rojo'],
                [3, '#FF8000', 'Naranja'],
                [4, '#FFFF00', 'Amarillo'],
                [5, '#008F39', 'Verde'],
                [6, '#0000FF', 'Azul'],
                [7, '#4C2882', 'Violeta'],
                [8, '#808080', 'Gris'],
                [9, '#FFFFFF', 'Blanco']
            ]
            banda1 = {
                "valor" : colores[ibanda1][0],
                "color" : colores[ibanda1][1],
                "nombre" : colores[ibanda1][2]
            }
            banda2 = {
                "valor" : colores[ibanda2][0],
                "color" : colores[ibanda2][1],
                "nombre" : colores[ibanda2][2]
            }
            banda3 = {
                "valor" : colores[ibanda3][0],
                "color" : colores[ibanda3][1],
                "nombre" : colores[ibanda3][2]
            }
            f = open('resisntencias.txt', 'a')
            texto = str(ibanda1) + '-' + str(ibanda2) + '-' + str(ibanda3) + '-' + str(tol)
            f.write(texto)
            f.write('\n')

            return render_template('resistencias.html', 
                                    banda1 = banda1,
                                    banda2 = banda2,
                                    banda3 = banda3,
                                    tol = tol,
                                    val = val,
                                    min = min,
                                    max = max,
                                    vista = 'calcular')
        if btn == 'Mostrar historial':
            f = open('resisntencias.txt', 'r')
            resistencias = f.readlines()
            resistenciasLimpias = []
            for item in resistencias:
                realItem = item.replace('\n', '')
                arrItem = realItem.split('-')
                resistencia = Resistencia(arrItem[0], arrItem[1], arrItem[2], arrItem[3])
                valor = resistencia.calcularResistencia()
                resistenciasLimpias.append([
                    resistencia.gethexadecimalBanda1(),
                    resistencia.getnombreBanda1(),
                    resistencia.gethexadecimalBanda2(),
                    resistencia.getnombreBanda2(),
                    resistencia.gethexadecimalBanda3(),
                    resistencia.getnombreBanda3(),
                    resistencia.getTolerancia(),
                    resistencia.getValue(),
                    resistencia.getMin(),
                    resistencia.getMax()
                ])
            return render_template('resistencias.html',
                                   vista = 'historial',
                                   resistencias = resistenciasLimpias)
    return render_template('resistencias.html', vista = 'bandas')


if __name__ == '__main__':
    # csrf.init_app(app)
    app.run(debug=True, port=3000)
    

