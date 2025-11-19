from flask import render_template, url_for, flash, redirect, request, abort
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, ServiceForm # Importamos ServiceForm
from app.models import User, Client, Service, Appointment
from flask_login import login_user, current_user, logout_user, login_required

# --- ROTAS DE AUTENTICAÇÃO (MANTIDAS) ---

# Rota para a página inicial (pode ser o Dashboard para o MVP)
@app.route("/")
@app.route("/dashboard")
@login_required 
def dashboard():
    # Esta será a tela que mostrará a Taxa de No-Show e outros KPIs
    return render_template('dashboard.html', title='Dashboard')

# Rota de Registro
@app.route("/register", methods=['GET', 'POST'])
def register():
    # ... código de registro mantido ...
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Conta criada com sucesso para {form.username.data}! Agora você pode fazer o login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Registrar', form=form)

# Rota de Login
@app.route("/login", methods=['GET', 'POST'])
def login():
    # ... código de login mantido ...
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
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
    return redirect(url_for('dashboard'))

# ----------------------------------------------------------------------
# --- NOVAS ROTAS PARA CRUD DE SERVIÇOS (REQUISITO 2) ---
# ----------------------------------------------------------------------

# 1. Rota de Listagem de Serviços (Read All)
@app.route("/services")
@login_required
def services():
    all_services = Service.query.order_by(Service.name).all()
    # MUDANÇA AQUI: Renderiza o arquivo dentro da pasta 'servicos/'
    return render_template('servicos/lista.html', title='Serviços', services=all_services) 

# 2. Rota de Criação de Serviço (Create)
@app.route("/service/new", methods=['GET', 'POST'])
@login_required
def new_service():
    form = ServiceForm()
    # ... lógica de validação ...
    
    # MUDANÇA AQUI: Renderiza o arquivo dentro da pasta 'servicos/'
    return render_template('servicos/form.html', title='Novo Serviço', form=form, legend='Criar Novo Serviço')

# 3. Rota de Edição de Serviço (Update)
@app.route("/service/<int:service_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_service(service_id):
    # ... lógica de edição ...
    
    # MUDANÇA AQUI: Renderiza o arquivo dentro da pasta 'servicos/'
    return render_template('servicos/form.html', title='Editar Serviço', form=form, legend=f'Editar Serviço: {service.name}')