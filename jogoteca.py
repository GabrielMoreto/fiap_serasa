from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Substitua pela sua chave secreta

# Dicionário de usuários para fins de demonstração
usuarios = {
    "mari": "67890",
    "usuario2": "senha2"
}

# Limite de tentativas de login
LIMITE_TENTATIVAS = 3

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'tentativas' not in session:
        session['tentativas'] = 0

    if request.method == 'POST':
        if session['tentativas'] >= LIMITE_TENTATIVAS:
            return "Você excedeu o número de tentativas de login. Tente novamente mais tarde.", 403
        
        username = request.form['username']
        password = request.form['password']
        
        if username in usuarios and usuarios[username] == password:
            session.pop('tentativas', None)  # Resetar tentativas na sessão após login bem-sucedido
            session['username'] = username
            return redirect(url_for('index'))
        else:
            session['tentativas'] += 1
            return "Nome de usuário ou senha incorretos.", 401

    return render_template('login.html')

@app.route('/')
def index():
    if 'username' in session:
        return f'Bem-vindo, {session["username"]}! <br><a href="/logout">Logout</a>'
    return 'Você não está logado. <br><a href="/login">Login</a>'

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)