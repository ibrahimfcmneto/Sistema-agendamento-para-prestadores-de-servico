from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User # Importa o modelo User

# Formulário de Registro (Para criar o primeiro gestor)
class RegistrationForm(FlaskForm):
    username = StringField('Usuário', 
                           validators=[DataRequired(), Length(min=2, max=20)])
    
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    
    confirm_password = PasswordField('Confirmar Senha', 
                                     validators=[DataRequired(), EqualTo('password', message='As senhas devem ser iguais.')])
    
    submit = SubmitField('Registrar')

    # Validação para evitar usuários/emails duplicados no banco
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Este nome de usuário já está em uso.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este email já está cadastrado.')

# Formulário de Login
class LoginForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    
    password = PasswordField('Senha', validators=[DataRequired()])
    
    remember = BooleanField('Lembrar-me')
    
    submit = SubmitField('Login')