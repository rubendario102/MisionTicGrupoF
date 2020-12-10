from flask import Flask,render_template,request,flash, url_for, redirect
import yagmail as yagmail
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
            return render_template('vistaBlog.html')
        else:
            return "Acceso Invalido"
    else:
        return "Metodo no permitido"
     
@app.route('/registro') #incluido por Edwin Polo . ruta para ir de Vista Login a Vista Crear Usuario
def registroUsuario():
    return render_template('registroUsuario.html')
      
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
 
#Anderson: Ruta una vez creado el usuario ser dirigido a la pagina del login
@app.route('/login',methods=["POST"])
def validarCampos():
    try:
        if request.method=="POST":
            usuario = request.form['usuarioNuevo']
            correo = request.form['correoUsuarioNuevo']
            password1 = request.form['passwordUsuarioNuevo']
            password2 = request.form['confirPasswordUsuarioNuevo']
            error = None
            if not utils.isUsernameValid(usuario):
                error = "El usuario debe de ser alfanumerico"
                flash(error)
                return render_template('registroUsuario.html')
            if not utils.isEmailValid(correo):
                error = "El correo no es valido"
                flash(error)
                return render_template('registroUsuario.html')
            if not utils.isPasswordValid(password1):
                error = "La contraseña 1 no es valida"
                flash(error)
                return render_template('registroUsuario.html')
            if not utils.isPasswordValid(password2):
                error = "La contraseña 2 no es valida"
                flash(error)
                return render_template('registroUsuario.html')
            yag = yagmail.SMTP("pruebatk.8912@gmail.com","prueba123")
            yag.send(to = correo, subject="Correo de activación", contents="Bienvenido al blog")
            flash("Revisa tu correo para activar tu cuenta")
            return render_template('login.html')
        return render_template('registroUsuario.html')
    except:
        return render_template('registroUsuario.html')

#Anderson: Ruta para ver el blog que se acaba de publicar
@app.route('/blogPublicado',methods=["GET"])
def crearBlog():
    titulo = request.args.get('titulo')
    cuerpo = request.args.get('cuerpo')
    error = None
    if request.method=="GET":
        if titulo != "" and cuerpo != "":
            return render_template('blogPublicado.html') 
        else:
            error = "Los campos titulo y cuerpo no pueden estar en blanco"
            flash(error)
            return render_template('crearEntrada.html')
    else:
        error = "Metodo no permitido"
        flash(error)
        return render_template('crearEntrada.html')

#Anderson: Ruta para ir a los blogs publicados desde crearEntrada
@app.route('/vistaBlog')
def vistaBlog():
    return render_template('vistaBlog.html') 

#Ruben: Ruta para actualizar blogs desde vistablogs
@app.route('/actualizarBlogs')
def actualizarBlogs():
    return render_template('actualizarEntrada.html') 

if __name__ == "__main__":
    app.run(debug=True)