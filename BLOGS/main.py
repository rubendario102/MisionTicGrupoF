from flask import Flask,render_template,request,flash, url_for, redirect
import utils 
import os

app = Flask (__name__)
app.secret_key = os.urandom(24)

@app.route('/') # Incluido por Edwin Polo. Abre la Vista de login

def principal():
    return render_template('login.html')

@app.route('/crearEntrada',methods=['POST','GET']) # Incluido por Edwin Polo, para ir de Login a Vista Crear entrada

def loginPost():
    if request.method=="POST":
        usuario= request.form['usuario']
        clave=request.form['password']
        if usuario=="edwin@hotmail.com" and clave=="123":
            return render_template('crearEntrada.html')
        else:
            return "Acceso Invalido"
    else:
        return "Metodo no permitido"

@app.route('/actualizarContraseña',methods=['POST','GET'])
def actualizar():
    try:
        if request.method=='POST':
            clave1 = request.form["password1"]
            clave2 = request.form["password2"]
            error = None

            if not utils.isPasswordValid(clave1):
                error = "La contraseña es inválida"
                flash(error)
                return render_template("ActualizarContraseña.html")
            
            if not utils.isPasswordValid(clave2):
                error = "La contraseña es inválida"
                flash(error)
                return render_template("ActualizarContraseña.html")

            if clave1==clave2:
                return render_template('vistaBlog.html')
            else:
                return render_template("ActualizarContraseña.html")
        return render_template("ActualizarContraseña.html")
    except:
         return render_template("ActualizarContraseña.html")

@app.route('/registro') #incluido por Edwin Polo . ruta para ir de Vista Login a Vista Crear Usuario
def registroUsuario():
    return render_template('registroUsuario.html')


if __name__ == "__main__":
    app.run(debug=True)