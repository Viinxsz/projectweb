from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)



class Tarefa(db.Model):
    __tablename__ = "tarefas"
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(200))
    feita = db.Column(db.Boolean)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        tarefa = Tarefa(conteudo=request.form['conteudo_tarefa'], feita=False)
        db.session.add(tarefa)
        db.session.commit()
    lista_de_tarefas = Tarefa.query.all()
    return render_template('index.html', lista_de_tarefas=lista_de_tarefas)

@app.route('/eliminar-tarefa/<id>')
def eliminar(id):
    tarefa = Tarefa.query.filter_by(id=int(id)).delete() # Pesquisa-se dentro da base de dados, aquele registro cujo id coincida com o proporcionado pelo parâmetro da rota. Quando se encontrar elimina-se
    db.session.commit() # Executar a operação pendente da base de dados
    return redirect(url_for('index')) # Redireciona-nos à função home() e se tudo correu bem, ao atualizar, a tarefa eliminada não vai aparecer na listagem



@app.route('/criar-tarefa', methods=['POST'])
def criar():
    if request.method == 'POST':
        tarefa = Tarefa(conteudo=request.form['conteudo_tarefa'], feita=False)
        db.session.add(tarefa)
        db.session.commit()
        return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        db.session.commit()
        from flask_migrate import upgrade
        upgrade()
    app.run(debug=True)