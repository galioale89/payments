from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from extensions import db
from main.views import main
from payment.views import payment
from login.views import logon

app = Flask(__name__)
app.config.from_pyfile('config.py')

db.init_app(app)

csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

# regsiter blueprints
app.register_blueprint(payment)
app.register_blueprint(main)
app.register_blueprint(logon)

if __name__ == '__main__':
    app.run(port='5001',debug=True)
