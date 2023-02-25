from flask import Flask, render_template
from flask import request
from flask_wtf.csrf import CSRFProtect
from flask import make_response
from flask import flash
import json
import ast
import forms, cajasDinamicas, traductor


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



if __name__ == '__main__':
    # csrf.init_app(app)
    app.run(debug=True, port=3000)
    
