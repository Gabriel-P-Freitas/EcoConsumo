from flask import Flask
from config import Config

# Config
app = Flask(__name__)
app.config.from_object(Config)

# Blueprints
from routes.basic import bp as basic_bp
app.register_blueprint(basic_bp)

from routes.doador import bp as doador_bp
app.register_blueprint(doador_bp, url_prefix='/doador')
from routes.empresa import bp as empresa_bp
app.register_blueprint(empresa_bp, url_prefix='/empresa')
from routes.usuario import bp as usuario_bp
app.register_blueprint(usuario_bp, url_prefix='/usuario')


# run
if __name__ == '__main__':
    app.run(port=2000, debug=True)