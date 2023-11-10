from flask import Flask, redirect, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/login')
def login():
    return render_template('index.html')

    
@app.route('/autenticar', methods=['POST'])
def autenticar():
    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM usuarios WHERE email=? AND senha=?', (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return redirect('/logado')
    else:
        return redirect('/login')
    
@app.route('/cadastro')
def exibir_cadastro():
    return render_template('cadastro.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    email = request.form['email']
    password = request.form['senha']
    nome=request.form['nome']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Correção na instrução SQL
    try:
        cursor.execute('INSERT INTO usuarios (email, senha,nome) VALUES (?, ?, ?)', (email, password, nome))
        conn.commit()
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")
        conn.rollback()
    finally:
        conn.close()

    return redirect('/login')

app.run(debug=True)