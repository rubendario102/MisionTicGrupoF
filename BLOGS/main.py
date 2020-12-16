from flask import *

import sqlite3
import yagmail as yagmail
import utils 
import os
import hashlib
from markupsafe import escape
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask (__name__)
app.secret_key = os.urandom(24)

@app.route('/') # Incluido por Edwin Polo. Abre la Vista de login
def principal():
    return render_template('login.html')

@app.route('/vistaBlog1',methods=['POST','GET']) # Incluido por Edwin Polo, para ir de Login a VistaBlog
def loginPost():
    if request.method=="POST":
        usuario= request.form['usuario']
        clave=request.form['password']
        if usuario=="edwin@hotmail.com" and clave=="123":
            return redirect(url_for('vistaBlog'))
        else:
            return "Acceso Invalido"
    else:
        return "Metodo no permitido"

@app.route('/registro') #incluido por Edwin Polo . ruta para ir de Vista Login a Vista Crear Usuario
def registroUsuario():
    return render_template('registroUsuario.html')

#Andrea: Ruta para cambiar contraseña       
@app.route('/actualizarPassword/',methods=['POST','GET'])
def actualizar():
    try:
        form = formActualizar()
        if request.method=='POST':
            clave1 = form.clave1.data
            clave2 = form.clave2.data
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
        return render_template("ActualizarContraseña.html", form = form)

#Anderson: Ruta una vez creado el usuario ser dirigido a la pagina del login
@app.route('/login',methods=["POST","GET"])
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

@app.route('/crearBlog')
def crearBlog2():
    return render_template('crearEntrada.html')

@app.route('/eliminarBlog/<int:post_id>')
def eliminarBlog(post_id):
    mensaje_eliminar = 'no entro '
    estado = 'inactivo'
    try:
        with sqlite3.connect('Blogs.db') as con: 
            cur = con.cursor()
            cur.execute("UPDATE Blogs SET estadoBlog = ? WHERE idBlogs = ?",[estado,post_id])
            con.commit()
            if con.total_changes>0:
                mensaje_eliminar = "Blog modificado"
            else:
                mensaje_eliminar = "Blog no se pudo modificar"
    except:
        con.rollback()
    finally:
        # return mensaje_eliminar
        return redirect(url_for('vistaBlog'))
    # return render_template("vistaBlog.html")

#Anderson: Ruta para ir a los blogs publicados desde crearEntrada
@app.route('/vistaBlog')
def vistaBlog():
    session["usuario"]=1
    user_id = session['usuario']
    try: 
        with sqlite3.connect('Blogs.db') as con:
            con.row_factory = sqlite3.Row 
            cur = con.cursor()
            cur.execute("SELECT * from Blogs where estadoBlog = 'activo'") 
            row = cur.fetchall()
            return render_template('vistaBlog.html',row = row, user_id = user_id)
    except:
        return "No se pudo listar"

#Ruben: Ruta para actualizar blogs desde vistablogs
@app.route('/actualizarBlogs/<int:post_id>', methods=['GET', 'POST'])
def actualizarBlogs(post_id):
    if "usuario" in session:
        user_id = session['usuario']
        if request.method=="GET":
            try:
                with sqlite3.connect('Blogs.db') as con:
                    con.row_factory = sqlite3.Row 
                    cur = con.cursor()
                    cur.execute("SELECT titulo,cuerpo FROM Blogs WHERE idBlogs=? AND id_Usuario = ?",[post_id,user_id]) 
                    row = cur.fetchone()
                    if row is None:
                        flash("El blog no se encuentra")
                    titulo = row["titulo"]
                    cuerpo = row["cuerpo"]
                    return render_template("actualizarEntrada.html", post_id=post_id, titulo=titulo, cuerpo=cuerpo)
                    # return render_template('vista_estudiante.html',row = row)
            except: 
                con.rollback() 
            return "No se pudo consultar"
        else:
            titulo = request.form['txtTitulo']
            cuerpo = request.form['txtCuerpo']
            try:
                with sqlite3.connect('Blogs.db') as con: 
                    cur = con.cursor()
                    cur.execute("UPDATE Blogs SET titulo =?,cuerpo=? WHERE idBlogs = ?",[titulo,cuerpo,post_id])
                    con.commit()
                    if con.total_changes>0:
                        mensaje = "Blog modificado"
                    else:
                        mensaje = "Blog no se pudo modificar"
            except:
                con.rollback()
            finally:
                return redirect(url_for('vistaBlog'))
            #update en ala base de datos
            # return render_template("vistaBlog.html")

@app.route('/recuperar') ## Edwin Polo, para ir a la vista de recuperar contraseña
def recuperarContraseña():
    return render_template('Recuperar.html') 

if __name__ == "__main__":
    app.run(debug=True)