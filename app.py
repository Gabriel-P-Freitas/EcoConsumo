from flask import Flask
from config import Config
from extensions import db, JWTManager, oauth
from datetime import datetime

# Config
app = Flask(__name__)
app.config.from_object(Config)


# Extensions
db.init_app(app)
JWTManager(app)
oauth.init_app(app)


# Blueprints
from routes.user import bp as user_bp
app.register_blueprint(user_bp, url_prefix='/api/user')
from routes.product import bp as product_bp
app.register_blueprint(product_bp, url_prefix='/api/product')


@app.route('/')
def test_page():
    data_hora_formatada = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return f'<h1>API: {data_hora_formatada}</h1>'


# Run
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(port=1000, debug=True)