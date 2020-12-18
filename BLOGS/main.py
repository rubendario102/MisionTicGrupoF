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
    usuario= escape(request.form["usuario"])
    clave= escape(request.form["clave"])
    message=None
    with sqlite3.connect('Blogs.db') as con:   # Aqui se abre la base de datos
        cur = con.cursor()
        #cur.execute("SELECT * from Usuario WHERE username = '"+usuario+"' AND clave= '"+clave+"'") de esta forma se puede realizar inyección de codigo....
        user=cur.execute(f"SELECT cla,id_u,est_u FROM tbl_001_u WHERE em = '{usuario}'").fetchone() # Sentencia preparada no acepta inyección de codigo ....
        if user != None:
            clave_hash= user[0]
            id_usuario= user[1]
            est_us= user[2]
            if est_us=="activo":
                if check_password_hash(clave_hash,clave):
                    session["usuario"]=id_usuario  # es un array que determina quien esta logueado.
                    variable = redirect(url_for('vistaBlog'))
                    return variable

                else:
                    message="Contraseña incorrecta, verifique nuevamente"
                    return render_template('login.html', message=message)
            else:
                message="Usuario inactivo"
                return render_template('login.html', message=message)

        else:
            message="Usuario y/o contraseña incorrectos"
            return render_template('login.html', message=message)

@app.route('/registro') #incluido por Edwin Polo . ruta para ir de Vista Login a Vista Crear Usuario
def registroUsuario():
    form = formRegistroUsuario()
    return render_template('registroUsuario.html', form = form)

#Andrea: Ruta para cambiar contraseña       
#@app.route('/actualizarPassword',methods=['POST','GET'])
@app.route('/actualizarPassword/<int:id_user>',methods=['GET','POST'])
#def actualizar():
def actualizar(id_user):
    
    if request.method=='GET':
        form = formActualizar()
        return render_template("ActualizarContraseña.html",id_user=id_user,form=form)
    else: 
        form = formActualizar()
        clave1 = form.clave1.data
        clave2 = form.clave2.data
        error = None
        if clave1==clave2:
            hashclave = generate_password_hash(clave1)
            try:
                with sqlite3.connect('Blogs.db') as con: 
                    cur = con.cursor()
                    cur.execute("UPDATE tbl_001_u SET cla =? WHERE id_u = ?",[hashclave,id_user])
                    con.commit()
                    #return "Guardado satisfactoriamente"
                    return render_template("login.html")
            except: 
                con.rollback()
            return render_template('login.html')
        else:
            return render_template("ActualizarContraseña.html", form=form, id_user=id_user)
    
#Anderson: Ruta una vez creado el usuario ser dirigido a la pagina del login
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
                            yag.send(to = correo, subject='Activar usuario', contents='Bienvenido al Blog para activar su usuario <a href='+url_for('activar',_external=True)+'>Click aqui para activar usuario</a>')
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


#Anderson: Ruta para ver el blog que se acaba de publicar
@app.route('/blogPublicado/<int:post_id>',methods=["GET","POST"])
def crearBlog(post_id):
 
    if "usuario" in session:
        user_id = session['usuario']
        try:
            with sqlite3.connect('Blogs.db') as con:
                con.row_factory = sqlite3.Row 
                cur = con.cursor()
                cur.execute("SELECT tit,cuer_b,fecha_cb FROM tbl_002_b WHERE id_b=? AND id_u = ?",[post_id,user_id]) 
                row = cur.fetchone()
                if row is None:
                    flash("El blog no se encuentra")
                titulo = row["tit"]
                cuerpo = row["cuer_b"]
                fecha = row["fecha_cb"]
                error = None
                if request.method=="GET":
                    if titulo != "" and cuerpo != "":
                        try:
                            with sqlite3.connect('Blogs.db') as con:
                                con.row_factory = sqlite3.Row 
                                cur = con.cursor()
                                cur.execute(f"select * from tbl_003_c where id_b = {post_id}")    
                                row = cur.fetchall()
                                return render_template('blogPublicado.html',row = row,titulo=titulo, cuerpo=cuerpo,fecha=fecha, user=user_id)
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
                                cur.execute("INSERT INTO tbl_003_c(id_b,id_u,cuer_c,fecha_cc,est_c)VALUES(?,?,?,CURRENT_TIMESTAMP,1)",(post_id,user_id,comentario))
                                con.commit()
                        except: 
                            con.rollback()
                            return "No se pudo guardar"
                    try:
                        with sqlite3.connect('Blogs.db') as con:
                            con.row_factory = sqlite3.Row 
                            cur = con.cursor()
                            cur.execute(f"select * from tbl_003_c where id_b = {post_id}")    
                            row = cur.fetchall()
                            return render_template('blogPublicado.html',row = row,titulo=titulo, cuerpo=cuerpo,fecha=fecha, user=user_id)
                    except:
                        return "No se pudo recuperar comentarios"
        except:
            return "No se pudo recuperar blogs"               
    else:
        return "Acción no permitida <a href='/'>adios</a>"

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
                        cursor.execute("INSERT INTO tbl_002_b(id_u, tit, cuer_b, est_b, fecha_cb)VALUES(?,?,?,?,CURRENT_TIMESTAMP)",(idUsuario, titulo, cuerpo, blog))
                        con.commit()
                        variable = redirect(url_for('vistaBlog'))
                        return variable
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
    estado = 0
    try:
        with sqlite3.connect('Blogs.db') as con: 
            cur = con.cursor()
            cur.execute("UPDATE tbl_002_b SET eli_b = ? WHERE id_b = ?",[estado,post_id])
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
@app.route('/vistaBlog', methods=['GET', 'POST'])
def vistaBlog():
    # session["usuario"]=1
    user_id = session['usuario']
    try: 
        with sqlite3.connect('Blogs.db') as con:
            con.row_factory = sqlite3.Row 
            cur = con.cursor()
            cur.execute("SELECT * from tbl_002_b where id_u = ? AND eli_b = 1",[user_id]) 
            row = cur.fetchall()
            return render_template('vistaBlog.html',row = row, user_id = user_id)
    except:
        return "No se pudo listar"

@app.route('/buscarVistaBlog', methods=['GET', 'POST'])
def buscarVistaBlog():
    user_id = session['usuario']
    if request.method=="POST":
        data = request.form['txtBuscar']
        try:
            with sqlite3.connect('Blogs.db') as con:
                con.row_factory = sqlite3.Row 
                cur = con.cursor()
                cur.execute("SELECT * FROM tbl_002_b WHERE tit_b LIKE '%"+data+"%' AND id_u = ? AND eli_b = 1",[user_id]) 
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
                    cur.execute("SELECT tit,cuer_b FROM tbl_002_b WHERE id_b=? AND id_u = ?",[post_id,user_id]) 
                    row = cur.fetchone()
                    if row is None:
                        flash("El blog no se encuentra")
                    titulo = row["tit"]
                    cuerpo = row["cuer_b"]
                    return render_template("actualizarEntrada.html", post_id=post_id, titulo=titulo, cuerpo=cuerpo)
                    # return render_template('vista_estudiante.html',row = row)
            except: 
                con.rollback() 
                return "error consulta"
            return "No se pudo consultar"
        else:
            titulo = request.form['txtTitulo']
            cuerpo = request.form['txtCuerpo']
            try:
                with sqlite3.connect('Blogs.db') as con: 
                    cur = con.cursor()
                    cur.execute("UPDATE tbl_002_b SET tit =?,cuer_b=? WHERE id_b = ?",[titulo,cuerpo,post_id])
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

@app.route('/recuperarContraseña', methods=['POST','GET'])
def recuperar():
    correo= escape(request.form["correo"])
    message=None
    error=None
    with sqlite3.connect('Blogs.db') as con:   # Aqui se abre la base de datos
        cur = con.cursor()
        #cur.execute("SELECT * from Usuario WHERE username = '"+usuario+"' AND clave= '"+clave+"'") de esta forma se puede realizar inyección de codigo....
        user=cur.execute(f"SELECT id_u FROM tbl_001_u WHERE em= '{correo}'").fetchone() # Sentencia preparada no acepta inyección de codigo ....
        if user != None:
            id_usuario= user[0]
            #cur.execute("SELECT email from Usuario where email=?", (correo,)) # Sentencia preparada no acepta inyección de codigo ....
            #session["email"]=email  # es un array que determina quien esta logueado.
            yag = yagmail.SMTP("pruebatk.8912@gmail.com","prueba123")
            yag.send(to=correo,subject='Recuperar contraseña',contents='Bienvenido al link para recuperar contraseña <a href='+url_for('actualizar',id_user=id_usuario,_external=True)+'>Click aqui para recuperar contraseña</a>')
            message="El acceso para recuperar tu contraseña se ha enviado al correo. Ahora puedes volver a Login:"
            return render_template('Recuperar.html',message=message)
        else:
            error="Este correo no esta registrado"
            return render_template('Recuperar.html',error=error)

#Ruta para activar el usuario
@app.route('/activar', methods=['POST','GET'])
def activar():
    if request.method == "POST":
        error = None
        correo = escape(request.form["correo"])
        if correo != "":
            try:
                with sqlite3.connect('Blogs.db') as con:
                    con.row_factory = sqlite3.Row 
                    cursor = con.cursor()
                    #busco si el correo ya existe
                    cursor.execute("SELECT id_u FROM tbl_001_u WHERE em = ?",[correo]) 
                    row = cursor.fetchone()
                    if row != None:
                        id_usuario= row[0]
                        cursor.execute("UPDATE tbl_001_u SET est_u =? WHERE id_u = ?",["activo",id_usuario])
                        con.commit()
                        variable = redirect(url_for('principal'))
                        return variable
                    else:
                        error = "Este correo no esta guardado en la base de datos"
                        flash(error)
                        return render_template('activar.html')
            except:
                error = "No se pudo activar el usuario"
                flash(error)
                return render_template('activar.html')
        else:
            error = "El campo no puede estar vacio"
            flash(error)
            return render_template('activar.html')
    else:
        error = "Metodo invalido"
        flash(error)
        return render_template('activar.html')

if __name__ == "__main__":
    #app.run(host='127.0.0.1', port = 443, ssl_context= ('micertificado.pem','llaveprivada.pem'),debug=True)
    app.run(debug=True)