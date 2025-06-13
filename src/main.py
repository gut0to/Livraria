

from flask import Flask, send_from_directory, jsonify
from src.models.livraria import db
from src.routes.livraria import livraria_bp
from src.routes.user import user_bp 
import os

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='')

    #  app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://user:password@host/db"
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:root@localhost:3306/livraria_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SECRET_KEY'] = 'lica123' 

    db.init_app(app)

    # blueprints
    app.register_blueprint(livraria_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api') # Ativa as rotas de usuário

    @app.route('/')
    def serve_index():
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory(app.static_folder, path)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all() 
    app.run(debug=True)