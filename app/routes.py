from flask import render_template, url_for, flash, redirect, request, abort
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, ServiceForm 
from app.models import User, Client, Service, Appointment
from flask_login import login_user, current_user, logout_user, login_required

# --- ROTAS DE AUTENTICAÇÃO E DASHBOARD ---

# Rota Principal: É o Dashboard, protegido pelo login
@app.route("/")
@app.route("/dashboard")
@login_required 
def dashboard():
    # Usuários não logados são redirecionados para o login (login_manager)
    return render_template('dashboard.html', title='Dashboard')

# Rota de Registro
@app.route("/register", methods=['GET', 'POST'])
def register():
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
    return redirect(url_for('login'))

# ----------------------------------------------------------------------
# --- ROTAS PARA CRUD DE SERVIÇOS (Corrigidas para subpasta) ---
# ----------------------------------------------------------------------

# 1. Rota de Listagem de Serviços (Read All)
@app.route("/services")
@login_required
def services():
    all_services = Service.query.order_by(Service.name).all()
    return render_template('servicos/lista.html', title='Serviços', services=all_services)

# 2. Rota de Criação de Serviço (Create)
@app.route("/service/new", methods=['GET', 'POST'])
@login_required
def new_service():
    form = ServiceForm()
    if form.validate_on_submit():
        service = Service(
            name=form.name.data,
            price=form.price.data,
            duration_minutes=form.duration_minutes.data
        )
        db.session.add(service)
        db.session.commit()
        flash(f'Serviço "{service.name}" criado com sucesso!', 'success')
        return redirect(url_for('services'))
    
    return render_template('servicos/form.html', title='Novo Serviço', form=form, legend='Criar Novo Serviço')

# 3. Rota de Edição de Serviço (Update)
@app.route("/service/<int:service_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_service(service_id):
    service = Service.query.get_or_404(service_id)
    form = ServiceForm()

    if form.validate_on_submit():
        service.name = form.name.data
        service.price = form.price.data
        service.duration_minutes = form.duration_minutes.data
        db.session.commit()
        flash(f'Serviço "{service.name}" atualizado com sucesso!', 'success')
        return redirect(url_for('services'))

    elif request.method == 'GET':
        form.name.data = service.name
        form.price.data = service.price
        form.duration_minutes.data = service.duration_minutes
        
    return render_template('servicos/form.html', title='Editar Serviço', form=form, legend=f'Editar Serviço: {service.name}')

# 4. Rota de Exclusão de Serviço (Delete)
@app.route("/service/<int:service_id>/delete", methods=['POST'])
@login_required
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    flash(f'Serviço excluído com sucesso!', 'success')
    return redirect(url_for('services'))