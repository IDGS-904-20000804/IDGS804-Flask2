from flask import Flask, render_template
from flask import request
from flask_wtf.csrf import CSRFProtect

import forms, cajasDinamicas


app=Flask(__name__)
app.config['SECRET_KEY']="esta es una clave encriptada"
# csrf = CSRFProtect()


@app.route("/")
def formprueba():
    return render_template("formPrueba.html")


@app.route("/Alumnos", methods=['GET','POST'])
def Alumnos():
    reg_alum = forms.UserForm(request.form)
    if request.method == 'POST':
        print(reg_alum.matricula.data)
        print(reg_alum.nombre.data)
    return render_template('Alumnos.html', form = reg_alum)


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


if __name__ == "__main__":
    # csrf.init_app(app)
    app.run(debug=True,port=3000)

