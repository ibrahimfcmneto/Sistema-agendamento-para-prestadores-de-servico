from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

# Inicializa as extensões (Instâncias globais)
# Elas não precisam do app ainda, evitando problemas de importação circular.
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

# Configurações do Flask-Login
login_manager.login_view = 'login' # Nome da função da rota de login
login_manager.login_message_category = 'info'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'


def create_app():
    """
    Função Fábrica de Aplicações do Flask.
    """
    app = Flask(__name__)

    # --- Configurações do App ---
    # Chave Secreta para segurança de sessões e formulários (Flask-WTF)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    
    # String de Conexão com o MySQL (Lida do .env)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # --- Inicializa as Extensões com a Aplicação ---
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # --- Importa e Registra as Rotas ---
    # Este import precisa ficar dentro da função para evitar erros de importação circular.
    from app import routes

    return app

# A variável 'app' é definida aqui fora, mas é um 'proxy' para o app criado.
# Isso é um detalhe técnico necessário para que o 'db' e outras extensões funcionem
# fora da função create_app (como no models.py ou no run.py).
app = create_app()