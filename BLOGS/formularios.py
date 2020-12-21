from flask_wtf import FlaskForm
from wtforms import *
from wtforms import StringField, SelectField, BooleanField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import *

class forEstudiantes(FlaskForm):
    documento = StringField("Documento",validators = [DataRequired(message="No dejar vacío, completar")], render_kw={"placeholder":"IDENTIFICACION"})
    nombre = StringField("Nombre",validators=[DataRequired(message="no dejar vacio, completar")],render_kw={"placeholder":"NOMBRE"})
    ciclo = SelectField("Ciclo",choices=[("python"),("java"),("desarrollo web")])        
    sexo = StringField("Sexo",validators=[DataRequired(message="no dejar vacio, completar")],render_kw={"placeholder":"SEXO"})
    estado = BooleanField("Estado")
    enviar = SubmitField("Enviar",render_kw={"onmouseover":"guardarEst()"})
    consultar = SubmitField("Consultar",render_kw={"onmouseover":"consultarEst()"})
    listar = SubmitField("Listar",render_kw={"onmouseover":"listarEst()"})
    actualizar = SubmitField("Actualizar",render_kw={"onmouseover":"actualizarEst()"})
    eliminar = SubmitField("Eliminar",render_kw={"onmouseover":"eliminarEst()"})          

class formLogin(FlaskForm):
    documento = StringField("Usuario",validators = [DataRequired(message="No dejar vacío, completar")], render_kw={"placeholder":"USUARIO"})
    clave = PasswordField("Clave",validators=[DataRequired(message="no dejar vacio, completar")],render_kw={"placeholder":"CONTRASEÑA"})
    enviar = SubmitField("Enviar",render_kw={"onmouseover":"guardarEst()"})
    insertar = SubmitField("insertar",render_kw={"onmouseover":"insertar()"})
    guardar = SubmitField("Guardar", render_kw={"onmouseover":"insertar()"})

class formActualizar(FlaskForm):
    clave1 = PasswordField("Contraseña:*",validators = [DataRequired(message="No dejar vacío, completar"), Length(min=5, max=20),Regexp('[0-9A-Za-z_]+')],render_kw={"placeholder":"Ingresa tu contraseña"})
    clave2 = PasswordField("Confirmar contraseña:*",validators = [DataRequired(message="No dejar vacío, completar"), Length(min=6,message="Debe tener mínimo 6 caracteres")],render_kw={"placeholder":"Confirma tu contraseña"})

class formBlog(FlaskForm):
    comentarios = StringField("Comments",validators = [DataRequired(message="No dejar vacío, completar")], render_kw={"placeholder":"COMENTARIOS"})
    comentar = SubmitField("Comentar", render_kw={"onmouseover":"crearBlog2()"})

class formRegistroUsuario(FlaskForm):
    usuario = StringField("Usuario:*",validators = [DataRequired(message="Debes de ingresar un usuario"), Length(min=5, max=20),Regexp('[0-9A-Za-z_]+')], render_kw={"placeholder":"Ingresa tu usuario"})
    correo = StringField("Correo:*", validators=[DataRequired(message="Debes de ingresar un correo"), Length(min=6,message="Debe tener mínimo 6 caracteres")], render_kw={"placeholder":"Ingresa tu correo"})
    password1 = PasswordField("Contraseña:*",validators=[DataRequired(message="Debes de ingresar una contraseña")],render_kw={"placeholder":"Ingresa tu contraseña"})
    password2 = PasswordField("Confirmar contraseña:*",validators=[DataRequired(message="Debes confirmar tu contraseña")],render_kw={"placeholder":"Ingresa tu contraseña de nuevo"})
    crearUsuario = SubmitField("CREAR USUARIO",render_kw={"onmouseover":"crearUsuario()"})

class formCrearBlog(FlaskForm):
    titulo = StringField(label = None, validators = [DataRequired(message="Debes de ingresar un título")], render_kw={"placeholder":"Título*"})
    cuerpo = TextAreaField(label = None, validators = [DataRequired(message="Debes de ingresar algún texto")])
    privacidad = SelectField("Privacidad:", choices= [("publico"),("privado")])
    nuevoBlog = SubmitField("Publicar",render_kw={"onmouseover":"crearBlog()"})