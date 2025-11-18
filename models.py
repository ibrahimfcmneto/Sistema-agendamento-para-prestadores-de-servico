from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

# Função auxiliar para o Flask-Login carregar o usuário
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 1. Modelo de Usuário (Para o Gestor acessar o sistema)
# Herda de UserMixin para funcionar com o Flask-Login (requirements.txt)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False) # Senha será hash
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# 2. Modelo de Cliente
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False) # Telefone para contato/WhatsApp
    email = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relacionamento: Um cliente pode ter vários agendamentos
    appointments = db.relationship('Appointment', backref='client', lazy=True)

    def __repr__(self):
        return f"Client('{self.name}', '{self.phone}')"

# 3. Modelo de Serviço (Corte, Barba, Consulta, etc.)
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False) # Duração em minutos para calcular agenda
    
    # Relacionamento: Um serviço aparece em vários agendamentos
    appointments = db.relationship('Appointment', backref='service', lazy=True)

    def __repr__(self):
        return f"Service('{self.name}', R$ {self.price})"

# 4. Modelo de Agendamento (O coração do sistema)
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_scheduled = db.Column(db.DateTime, nullable=False) # Data e Hora do agendamento
    
    # Status para KPI de No-Show (Conforme README: Concluído, Cancelado, Falta)
    status = db.Column(db.String(20), nullable=False, default='Agendado') 
    
    # Chaves Estrangeiras (Foreign Keys)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    
    note = db.Column(db.Text, nullable=True) # Obs: "Cliente pediu para adiantar"

    def __repr__(self):
        return f"Appointment('{self.date_scheduled}', '{self.status}')"