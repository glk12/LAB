from flask import Flask, redirect, render_template, request, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Defina uma chave secreta para o uso de flash messages

@app.route('/login')
def login():
    return render_template('login.html')

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
        return redirect('/inicio')
    else:
        flash('Credenciais inválidas. Tente novamente.', 'error')
        return redirect('/login')

@app.route('/inicio')
def exibir_inicio():
    return render_template("inicio.html")

@app.route('/cadastro')
def exibir_cadastro():
    return render_template('cadastro.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    email = request.form['email']
    password = request.form['senha']
    nome = request.form['nome']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO usuarios (email, senha, nome) VALUES (?, ?, ?)', (email, password, nome))
        conn.commit()
        flash('Usuário registrado com sucesso!', 'success')
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")
        conn.rollback()
        flash('Erro ao registrar usuário. Tente novamente.', 'error')
    finally:
        conn.close()

    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
