from flask import Flask, render_template, request, redirect
import MySQLdb

app = Flask(__name__)

# Configuração do Banco de Dados
db = MySQLdb.connect(
    host="127.0.0.1",
    user="root",
    passwd="labinfo",
    db="moda"
)

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/index")
def home():
    return render_template("index.html")

@app.route("/registrar", methods=["POST"])
def registrar():
    nome = request.form["username"]
    email = request.form["email"]
    senha_fornecida = request.form["password"]

    cursor = db.cursor()
    

    cursor.execute("SELECT senha FROM usuarios WHERE email = %s", (email,))
    usuario = cursor.fetchone()

    if usuario:
        senha_do_banco = usuario[0]
        
        if senha_fornecida == senha_do_banco:
            return redirect("/index")
        else:
            return "Senha incorreta!", 401 

    sql = "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)"
    valores = (nome, email, senha_fornecida)

    cursor.execute(sql, valores)
    db.commit()

    return redirect("/index")

if __name__ == "__main__":

    app.run(debug=True)
