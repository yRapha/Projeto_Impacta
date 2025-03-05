from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
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
        db.create_all()
    app.run(debug=True)