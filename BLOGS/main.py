from flask import *

import sqlite3
import yagmail as yagmail
import utils
import os
import hashlib
from markupsafe import escape
from werkzeug.security import generate_password_hash, check_password_hash
from formularios import *

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
    form = formRegistroUsuario()
    return render_template('registroUsuario.html', form = form)

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

#Anderson: Ruta una vez creado el usuario ser dirigido a la pagina del login y guardar usuario
@app.route('/login',methods=["POST","GET"])
def crearUsuario():
    form = formRegistroUsuario()
    if request.method == "POST":
        error = None
        # Se obtienen los datos desde el formulario
        usuario = escape(form.usuario.data)
        correo = escape(form.correo.data)
        password1 = escape(form.password1.data)
        password2 = escape(form.password2.data)
        if usuario != "" and correo != "" and password1 != "" and password2 != "":
            # No reconoce la clase utils con WTForms
            '''if not utils.isUsernameValid(usuario):
                error = "El usuario debe de ser alfanumerico"
                flash(error)
                return render_template('registroUsuario.html', form = form)
            if not utils.isEmailValid(correo):
                error = "El correo no es valido"
                flash(error)
                return render_template('registroUsuario.html', form = form)
            if not utils.isPasswordValid(password1):
                error = "La contraseña 1 no es valida"
                flash(error)
                return render_template('registroUsuario.html', form = form)
            if not utils.isPasswordValid(password2):
                error = "La contraseña 2 no es valida"
                flash(error)
                return render_template('registroUsuario.html', form = form)'''
            if password1 == password2:
                try:
                    #Conexión a la base de datos para guardar el usuario
                    encriptada = generate_password_hash(password1)
                    with sqlite3.connect('Blogs.db') as con:
                        con.row_factory = sqlite3.Row 
                        cursor = con.cursor()
                        #busco si el correo ya existe
                        cursor.execute("SELECT usr,em FROM tbl_001_u WHERE em = ?",[correo]) 
                        row = cursor.fetchone()
                        if row is None:
                            #si el correo no esta en la base de datos guardo el usuario
                            cursor.execute("INSERT INTO tbl_001_u(usr, em, cla, tip_u, est_u) VALUES(?,?,?,?,?)",(usuario,correo,encriptada, 1,"inactivo"))
                            con.commit()
                            yag = yagmail.SMTP("pruebatk.8912@gmail.com","prueba123")
                            yag.send(to = correo, subject="Correo de activación", contents="Bienvenido al blog")
                            return render_template('login.html')
                        else:
                            error = "El correo ya existe"
                            flash(error)
                            return render_template('registroUsuario.html', form = form)
                except:
                    con.rollback()
                    error = "No se pudo insertar el usuario"
                    flash(error)
                    return render_template('registroUsuario.html', form = form)
            else:
                error = "Las contraseñas no son iguales"
                flash(error)
                return render_template('registroUsuario.html', form = form)
        else:
            error = "Todos los campos son obligatorios"
            flash(error)
            return render_template('registroUsuario.html', form = form)
    else:
        error = "Metodo invalido"
        flash(error)
        return render_template('registroUsuario.html', form = form)

#Anderson: Ruta para ver el blog que ya esta publicado
@app.route('/blogPublicado',methods=["GET","POST"])
def crearBlog():
    if "usuario" in session:
        user_id = session['usuario']    
        titulo = request.args.get('titulo')
        cuerpo = request.args.get('cuerpo')
        error = None
        if request.method=="GET":
            if titulo != "" and cuerpo != "":
                try:
                    with sqlite3.connect('Blogs.db') as con:
                        con.row_factory = sqlite3.Row 
                        cur = con.cursor()
                        cur.execute("select * from tbl_003_c where id_b = 1")    
                        row = cur.fetchall()
                        return render_template('blogPublicado.html',row = row)
                except: 
                    return "No se pudo recuperar comentarios"
            else:
                error = "Los campos titulo y cuerpo no pueden estar en blanco"
                flash(error)
                return render_template('crearEntrada.html')
        else:
            if request.method == "POST":
                comentario = escape(request.form["Comments"])
                try:
                    with sqlite3.connect('Blogs.db') as con: 
                        cur = con.cursor()
                        cur.execute("INSERT INTO tbl_003_c(id_b,id_u,cuer_c)VALUES(?,?,?)",(1,user_id,comentario))
                        con.commit()
                except: 
                    con.rollback()
                    return "No se pudo guardar"

            try:
                with sqlite3.connect('Blogs.db') as con:
                    con.row_factory = sqlite3.Row 
                    cur = con.cursor()
                    cur.execute("select * from tbl_003_c where id_b = 1")    
                    row = cur.fetchall()
                    return render_template('blogPublicado.html',row = row)
            except:
                return "No se pudo recuperar comentarios"

@app.route('/crearBlog')
def crearBlog2():
    if "usuario" in session:
        form = formCrearBlog()
        return render_template('crearEntrada.html', form = form)
    else:
        return render_template('login.html')

#Anderson: Guardar Blog
@app.route('/blog')
def crearBlog3():
    if "usuario" in session:
        form = formCrearBlog()
        if request.method == "GET":
            idUsuario = session['usuario']    
            titulo = escape(request.args.get('titulo'))
            cuerpo = escape(request.args.get('cuerpo'))
            estado = request.args.get('privacidad')
            if estado == "0":
                blog = "publico"
            else:
                blog = "privado"
            error = None
            if titulo != "" and cuerpo != "":
                try:
                    with sqlite3.connect('Blogs.db') as con: 
                        cursor = con.cursor()
                        #borrar id del usuario
                        cursor.execute("INSERT INTO tbl_002_b(id_u, tit, cuer_b, est_b, fecha_cb)VALUES(?,?,?,?,?)",(idUsuario, titulo, cuerpo, blog,""))
                        con.commit()
                        return render_template('vistaBlog.html')
                except:
                    con.rollback()
                    error = "No se pudo crear el blog"  
                    flash(error)
                    return render_template('crearEntrada.html', form = form)
            else:
                error = "Los campos no pueden estar vacios"
                flash(error)
                return render_template('crearEntrada.html', form = form)
        else:
            error = "Metodo invalido"
            flash(error)
            return render_template('crearEntrada.html', form = form)
    else:
        return render_template('login.html')

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
    #app.run(host='127.0.0.1', port = 443, ssl_context= ('micertificado.pem','llaveprivada.pem'),debug=True)
    app.run(debug=True)