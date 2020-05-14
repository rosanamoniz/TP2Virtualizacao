from flask import Flask, render_template, jsonify, request, redirect, url_for
import secrets
import json
from pymongo import MongoClient
import secrets
import json
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BASE_DE_DADOS.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Utilizador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Nome = db.Column(db.String(50))
    Apelido = db.Column(db.String(50))
    Login = db.Column(db.String(50))
    PalavraPasse = db.Column(db.String(50))
    Email = db.Column(db.String(50))
    Token = db.column(db.String(50))

    def data(self):
        return "Nome: {} | Aelido {} | Email {} <br>".format(self.Nome, self.Apelido, self.Email, self.Token)

def Adicionar(obj):
    db.session.add(obj)
    db.session.commit()
    
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/registar')
def register():
    return render_template("registar.html")

@app.route('/registar/', methods=['POST'])
def registarNaBaseDeDados():
    conseguiu = "O seu registo foi realizado com sucesso!"
    try:
        dadosDoFormulario = request.get_json(force=False)
        nome = dadosDoFormulario["nome"]
        apelido = dadosDoFormulario["apelido"]
        email = dadosDoFormulario["email"]
        login = dadosDoFormulario["login"]
        palavraPasse = dadosDoFormulario["palavraPasse"]
        
        utilizador = Utilizador(Nome=nome, Apelido=apelido,
                                Email=email, Login=login, PalavraPasse=palavraPasse)
        Adicionar(utilizador)
    except:
        conseguiu = "erro" + sys.exc_info()[0]
        raise

    return toJSON(conseguiu)

@app.route('/login')
def index():
    return render_template("login.html")

@app.route('/login/', methods=['POST'])
def login():
    dataR = request.get_json(force=False)
    login = dataR["login"]
    palavraPasse = dataR["palavraPasse"]

    existeUtilizador = Utilizador.query.filter_by(
        Login=login, PalavraPasse=palavraPasse).first()

    # existeUtilizador = Utilizador.query.all().filter(
    # Utilizador.Login == login, Utilizador.PalavraPasse == palavraPasse).first()

    if existeUtilizador != None:
        token = secrets.token_hex()
        ab = token
        existeUtilizador.Token
        db.session.commit()
        print('Exists')
        print("TOKEN:"+token)
        #return redirect("http://localhost:8001/?token="+ab)
        
        return toJSON(token)
    else:
        return toJSON(False)

@app.route('/VerUtilizadores')
def Select():
    result = Utilizador.query.all()
    html = ''

    for r in result:
        html += r.data()

    return html 

def toJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

if __name__ == "__main__":
    try:
        db.create_all()
    except:
        ...
    app.run(host='0.0.0.0', debug=True)
