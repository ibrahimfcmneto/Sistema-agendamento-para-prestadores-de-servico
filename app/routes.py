from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User, Client, Service, Appointment
from flask_login import login_user, current_user, logout_user, login_required

# Rota para a página inicial (pode ser o Dashboard para o MVP)
@app.route("/")
@app.route("/dashboard")
@login_required # Garante que só usuários logados podem acessar
def dashboard():
    # Esta será a tela que mostrará a Taxa de No-Show e outros KPIs
    return render_template('dashboard.html', title='Dashboard')

# Rota de Registro
@app.route("/register", methods=['GET', 'POST'])
def register():
    # Se o gestor já estiver logado, redireciona para o Dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # 1. Faz o hash da senha usando Flask-Bcrypt
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        # 2. Cria o novo objeto User
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        
        # 3. Adiciona ao banco de dados e salva
        db.session.add(user)
        db.session.commit()
        
        flash(f'Conta criada com sucesso para {form.username.data}! Agora você pode fazer o login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Registrar', form=form)

# Rota de Login
@app.route("/login", methods=['GET', 'POST'])
def login():
    # Se o gestor já estiver logado, redireciona para o Dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        # 1. Busca o usuário pelo email
        user = User.query.filter_by(email=form.email.data).first()
        
        # 2. Verifica se o usuário existe E se a senha confere (usando bcrypt)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            
            # Redireciona para a página que o usuário tentou acessar antes, ou para o Dashboard
            next_page = request.args.get('next')
            flash('Login bem-sucedido!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login sem sucesso. Verifique o email e a senha.', 'danger')
            
    return render_template('login.html', title='Login', form=form)

# Rota de Logout
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('dashboard')) # Redireciona para o Dashboard (que pedirá o Login novamente)