from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import pymysql
pymysql.install_as_MySQLdb()

# Adicionando imports para o teste de conexão
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://nathalia:12345@localhost/projeto_impacta'

# Teste de conexão com o banco de dados
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
if not database_exists(engine.url):
    create_database(engine.url)
print(f"Database exists: {database_exists(engine.url)}")

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)

@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    nome = request.form['nome']
    quantidade = int(request.form['quantidade'])
    preco = float(request.form['preco'])
    new_item = Item(nome=nome, quantidade=quantidade, preco=preco, ativo=True)
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_item(id):
    item = Item.query.get_or_404(id)
    if request.method == 'POST':
        item.nome = request.form['nome']
        item.quantidade = int(request.form['quantidade'])
        item.preco = float(request.form['preco'])
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', item=item)

@app.route('/toggle/<int:id>')
def toggle_item(id):
    item = Item.query.get_or_404(id)
    item.ativo = not item.ativo
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print("Conexão com o banco de dados estabelecida com sucesso!")
        except SQLAlchemyError as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
    
    # Adicionando logs para depuração
    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    app.run(debug=True)
