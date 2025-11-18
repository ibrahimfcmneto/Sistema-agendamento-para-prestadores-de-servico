from app import create_app, db
from app.models import User, Client, Service, Appointment # Importe os Models

app = create_app()

# Permite acessar o objeto 'db' e os Models no Flask Shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Client': Client, 'Service': Service, 'Appointment': Appointment}

if __name__ == '__main__':
    # Quando você rodar python run.py, ele vai iniciar o servidor web
    app.run(debug=True)

#deu certo a develop