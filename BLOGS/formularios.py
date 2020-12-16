from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired

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
    clave1 = PasswordField("Contraseña:*",validators = [DataRequired(message="No dejar vacío, completar")],render_kw={"placeholder":"Ingresa tu contraseña"})
    clave2 = PasswordField("Confirmar contraseña:*",validators = [DataRequired(message="No dejar vacío, completar")],render_kw={"placeholder":"Confirma tu contraseña"})
