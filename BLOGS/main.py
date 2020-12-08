from flask import Flask,render_template,request
app = Flask (__name__)
@app.route('/')

def principal():
    return render_template('login.html')

@app.route('/crearEntrada',methods=["POST"])

def loginPost():
    usuario= request.form['usuario']
    clave=request.form['password']
    if request.method=="POST":
        if usuario=="edwin@hotmail.com" and clave=="123":
            return render_template('crearEntrada.html')
        else:
            return "Acceso Invalido"
    else:
        return "Metodo no permitido"
if __name__ == "__main__":
    app.run(debug=True)