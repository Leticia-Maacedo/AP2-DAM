from flask import Flask, jsonify
from app.database import db
from app.models.atividade import Atividade
from app.models.nota import Nota
from app.controllers.atividade_controller import atividade_bp
from app.controllers.nota_controller import nota_bp
import os
import json

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///atividades.db' 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    @app.route('/docs')
    def swagger_ui():
        html_content = """
        <!DOCTYPE html>
        <html lang="pt-br">
          <head>
            <meta charset="UTF-8" />
            <title>API Atividades / Notas</title>
            <link rel="stylesheet" type="text/css"
              href="https://unpkg.com/swagger-ui-dist/swagger-ui.css" />
          </head>
          <body>
            <div id="swagger-ui"></div>
            <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
            <script>
              window.onload = () => {
                SwaggerUIBundle({ url: '/swagger.json', dom_id: '#swagger-ui' });
              };
            </script>
          </body>
        </html>
        """
        return html_content

    @app.route('/swagger.json')
    def swagger_spec():
        try:
            file_path = os.path.join(app.root_path, 'swagger', 'swagger.json')
            with open(file_path) as f:
                return jsonify(json.load(f))
        except FileNotFoundError:
            return jsonify({'error': 'Swagger JSON file not found'}), 404
        except json.JSONDecodeError:
            return jsonify({'error': 'Invalid JSON in swagger.json'}), 500

    with app.app_context():
        # Cria as tabelas para Atividades e Notas
        db.create_all()

    app.register_blueprint(atividade_bp)
    app.register_blueprint(nota_bp) 

    return app
