# app.py (Versão Simples com PyMySQL)
# ***************************************************************
# Parte 1: Imports e Inicialização
# ***************************************************************

from flask import Flask, render_template, url_for, flash, redirect, request, abort
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from dotenv import load_dotenv
import os
import pymysql
import pymysql.cursors
from datetime import datetime

# Carrega as variáveis do arquivo .env
load_dotenv()

app = Flask(__name__)

# Configurações
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Inicialização das Extensões
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'

# ------------------------------------------------------------------
# NOVO: Função de Conexão com PyMySQL (Lendo do .env)
# ------------------------------------------------------------------
def get_db_connection():
    try:
        return pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            cursorclass=pymysql.cursors.DictCursor
        )
    except Exception as e:
        # Se a conexão falhar, garantimos que o erro é visível
        print(f"ERRO FATAL DE CONEXÃO COM O BANCO DE DADOS: {e}")
        return None

# ***************************************************************
# Parte 2: Estrutura de Dados (Não mais Models de SQLAlchemy)
# ***************************************************************

# Usamos UserMixin para compatibilidade com Flask-Login
class User(UserMixin):
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
    
    # Função que o Flask-Login usa para carregar o usuário
    @login_manager.user_loader
    def load_user(user_id):
        conn = get_db_connection()
        if conn is None: return None
        with conn.cursor() as cursor:
            # Seleciona todos os campos, incluindo a senha
            cursor.execute("SELECT id, username, email, password FROM user WHERE id = %s", (user_id,))
            user_data = cursor.fetchone()
        conn.close()

        if user_data:
            return User(
                id=user_data['id'],
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password']
            )
        return None

# ***************************************************************
# Parte 3: Formulários (Forms)
# ***************************************************************

# A lógica de validação de duplicidade (validate_username/email) agora usará PyMySQL
class RegistrationForm(FlaskForm):
    # ... Campos de Registro (mantidos) ...
    username = StringField('Usuário', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Senha', 
                                     validators=[DataRequired(), EqualTo('password', message='As senhas devem ser iguais.')])
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        conn = get_db_connection()
        if conn is None: raise ValidationError('Erro de conexão com o banco de dados.')
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM user WHERE username = %s", (username.data,))
            if cursor.fetchone():
                raise ValidationError('Este nome de usuário já está em uso.')
        conn.close()

    def validate_email(self, email):
        conn = get_db_connection()
        if conn is None: raise ValidationError('Erro de conexão com o banco de dados.')
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM user WHERE email = %s", (email.data,))
            if cursor.fetchone():
                raise ValidationError('Este email já está cadastrado.')
        conn.close()

class LoginForm(FlaskForm):
    # ... Campos de Login (mantidos) ...
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember = BooleanField('Lembrar-me')
    submit = SubmitField('Login')

class ServiceForm(FlaskForm):
    # ... Campos de Serviço (mantidos) ...
    name = StringField('Nome do Serviço', 
                       validators=[DataRequired(), Length(min=3, max=100)])
    price = DecimalField('Preço (R$)', 
                         validators=[DataRequired(), NumberRange(min=0.01, message='O preço deve ser maior que zero.')])
    duration_minutes = IntegerField('Duração (minutos)', 
                                    validators=[DataRequired(), NumberRange(min=5, message='A duração deve ser de no mínimo 5 minutos.')])
    submit = SubmitField('Salvar Serviço')

# ***************************************************************
# Parte 4: Rotas (Application Logic)
# ***************************************************************

@app.route("/")
@app.route("/dashboard")
@login_required 
def dashboard():
    return render_template('dashboard.html', title='Dashboard')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        
        # NOVO: Lógica de INSERT com PyMySQL
        conn = get_db_connection()
        if conn is None:
            flash('Erro de conexão com o banco de dados ao registrar.', 'danger')
            return redirect(url_for('register'))
            
        with conn.cursor() as cursor:
            sql = "INSERT INTO user (username, email, password) VALUES (%s, %s, %s)"
            cursor.execute(sql, (form.username.data, form.email.data, hashed_password))
        conn.commit()
        conn.close()
        
        flash(f'Conta criada com sucesso para {form.username.data}! Agora você pode fazer o login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Registrar', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        # NOVO: Lógica de SELECT com PyMySQL
        conn = get_db_connection()
        if conn is None:
            flash('Erro de conexão com o banco de dados.', 'danger')
            return redirect(url_for('login'))
            
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, username, email, password FROM user WHERE email = %s", (form.email.data,))
            user_data = cursor.fetchone()
        conn.close()

        if user_data and bcrypt.check_password_hash(user_data['password'], form.password.data):
            # Cria o objeto User que o Flask-Login precisa
            user = User(
                id=user_data['id'],
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password']
            )
            login_user(user, remember=form.remember.data)
            
            next_page = request.args.get('next')
            flash('Login bem-sucedido!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login sem sucesso. Verifique o email e a senha.', 'danger')
            
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('dashboard'))

# CRUD de Serviços (Agora totalmente em PyMySQL)

@app.route("/services")
@login_required
def services():
    conn = get_db_connection()
    services_list = []
    if conn is not None:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, name, price, duration_minutes FROM service ORDER BY name")
            services_list = cursor.fetchall()
        conn.close()
    
    return render_template('servicos/lista.html', title='Serviços', services=services_list)

@app.route("/service/new", methods=['GET', 'POST'])
@login_required
def new_service():
    form = ServiceForm()
    if form.validate_on_submit():
        conn = get_db_connection()
        if conn is None:
            flash('Erro de conexão com o banco de dados.', 'danger')
            return redirect(url_for('new_service'))

        # Lógica de validação de unicidade (manual)
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM service WHERE name = %s", (form.name.data,))
            if cursor.fetchone():
                flash('Já existe um serviço com este nome.', 'danger')
                conn.close()
                return render_template('servicos/form.html', title='Novo Serviço', form=form, legend='Criar Novo Serviço')

        # Lógica de INSERT
        with conn.cursor() as cursor:
            sql = "INSERT INTO service (name, price, duration_minutes) VALUES (%s, %s, %s)"
            cursor.execute(sql, (form.name.data, form.price.data, form.duration_minutes.data))
        conn.commit()
        conn.close()
        
        flash(f'Serviço "{form.name.data}" criado com sucesso!', 'success')
        return redirect(url_for('services'))
    
    return render_template('servicos/form.html', title='Novo Serviço', form=form, legend='Criar Novo Serviço')

@app.route("/service/<int:service_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_service(service_id):
    conn = get_db_connection()
    if conn is None:
        flash('Erro de conexão com o banco de dados.', 'danger')
        return redirect(url_for('services'))
    
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, name, price, duration_minutes FROM service WHERE id = %s", (service_id,))
        service_data = cursor.fetchone()
    
    if service_data is None:
        conn.close()
        abort(404)
        
    form = ServiceForm()
    
    if form.validate_on_submit():
        # Lógica de UPDATE
        with conn.cursor() as cursor:
            sql = "UPDATE service SET name=%s, price=%s, duration_minutes=%s WHERE id=%s"
            cursor.execute(sql, (form.name.data, form.price.data, form.duration_minutes.data, service_id))
        conn.commit()
        conn.close()

        flash(f'Serviço "{form.name.data}" atualizado com sucesso!', 'success')
        return redirect(url_for('services'))

    elif request.method == 'GET':
        # Preenche o formulário com os dados do banco
        form.name.data = service_data['name']
        form.price.data = service_data['price']
        form.duration_minutes.data = service_data['duration_minutes']
        conn.close()
        
    return render_template('servicos/form.html', title='Editar Serviço', form=form, legend=f'Editar Serviço: {service_data["name"]}')

@app.route("/service/<int:service_id>/delete", methods=['POST'])
@login_required
def delete_service(service_id):
    conn = get_db_connection()
    if conn is None:
        flash('Erro de conexão com o banco de dados.', 'danger')
        return redirect(url_for('services'))
        
    with conn.cursor() as cursor:
        # Lógica de DELETE
        cursor.execute("DELETE FROM service WHERE id = %s", (service_id,))
    conn.commit()
    conn.close()
    
    flash(f'Serviço excluído com sucesso!', 'success')
    return redirect(url_for('services'))

# ***************************************************************
# Parte 5: Execução
# ***************************************************************

if __name__ == '__main__':
    # O PyMySQL não cria as tabelas. Garanta que você rodou o script SQL manualmente.
    app.run(debug=True)