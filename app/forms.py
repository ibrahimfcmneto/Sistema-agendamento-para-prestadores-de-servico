from flask_wtf import FlaskForm
# Importamos novos tipos de campos: DecimalField para preço e IntegerField para duração
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, IntegerField 
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from app.models import User, Service # Importa o modelo Service

# --- Formulários de Autenticação (Mantidos) ---
class RegistrationForm(FlaskForm):
    username = StringField('Usuário', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Senha', 
                                     validators=[DataRequired(), EqualTo('password', message='As senhas devem ser iguais.')])
    submit = SubmitField('Registrar')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Este nome de usuário já está em uso.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este email já está cadastrado.')

class LoginForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember = BooleanField('Lembrar-me')
    submit = SubmitField('Login')


# --- NOVO: Formulário de Serviço ---
class ServiceForm(FlaskForm):
    # Nome do Serviço
    name = StringField('Nome do Serviço', 
                       validators=[DataRequired(), Length(min=3, max=100)])
    
    # Preço: Deve ser um número decimal, não negativo
    price = DecimalField('Preço (R$)', 
                         validators=[DataRequired(), NumberRange(min=0.01, message='O preço deve ser maior que zero.')])
    
    # Duração: Deve ser um número inteiro, não negativo
    duration_minutes = IntegerField('Duração (minutos)', 
                                    validators=[DataRequired(), NumberRange(min=5, message='A duração deve ser de no mínimo 5 minutos.')])
    
    submit = SubmitField('Salvar Serviço')

    # Validação customizada: Evitar serviços com o mesmo nome
    def validate_name(self, name):
        service = Service.query.filter_by(name=name.data).first()
        if service:
            # Esta validação é importante, mas deve ser ajustada para edição (Update)
            # Por enquanto, mantemos assim para a criação (Create).
            raise ValidationError('Já existe um serviço com este nome.')