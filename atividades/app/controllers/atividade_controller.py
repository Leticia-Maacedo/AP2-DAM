from flask import Blueprint, request, jsonify
from app.models.atividade import Atividade
from app.database import db
import requests
import os
from datetime import datetime

atividade_bp = Blueprint('atividades', __name__, url_prefix='/api/atividades')

GERENCIAMENTO_API_URL = os.environ.get('GERENCIAMENTO_API_URL', 'http://gerenciamento_service:5000/api')

def validar_entidade(entity_name, entity_id):
    endpoint_map = {
        'turma': 'turmas',
        'professor': 'professores',
        'aluno': 'alunos'
    }
    endpoint = endpoint_map.get(entity_name)
    if not endpoint:
        return False
    try:
        response = requests.get(f"{GERENCIAMENTO_API_URL}/{endpoint}/{entity_id}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False
    except Exception:
        return False

# --- Rotas de Atividades (CRUD) ---

@atividade_bp.route('/', methods=['POST'])
def criar_atividade():
    dados = request.get_json()
    
    if not dados.get('nome_atividade') or not dados.get('turma_id') or not dados.get('professor_id'):
        return jsonify({'erro': 'nome_atividade, turma_id e professor_id sao obrigatorios'}), 400

    if not validar_entidade('turma', dados['turma_id']):
        return jsonify({'erro': f"Turma com ID {dados['turma_id']} nao encontrada"}), 404
    if not validar_entidade('professor', dados['professor_id']):
        return jsonify({'erro': f"Professor com ID {dados['professor_id']} nao encontrado"}), 404
        
    try:
        nova_atividade = Atividade.from_dict(dados)
        db.session.add(nova_atividade)
        db.session.commit()
        return jsonify(nova_atividade.to_dict()), 201
    except ValueError:
        return jsonify({'erro': 'Data de entrega invalida. Use o formato DD/MM/AAAA'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro ao criar atividade: {str(e)}'}), 500

@atividade_bp.route('/', methods=['GET'])
def listar_atividades():
    atividades = Atividade.query.all()
    return jsonify([a.to_dict() for a in atividades]), 200

@atividade_bp.route('/<int:id>', methods=['GET'])
def obter_atividade(id):
    atividade = Atividade.query.get_or_404(id)
    return jsonify(atividade.to_dict()), 200

@atividade_bp.route('/<int:id>', methods=['PUT'])
def atualizar_atividade(id):
    atividade = Atividade.query.get_or_404(id)
    dados = request.get_json()

    if 'turma_id' in dados and not validar_entidade('turma', dados['turma_id']):
        return jsonify({'erro': f"Turma com ID {dados['turma_id']} nao encontrada"}), 404
    if 'professor_id' in dados and not validar_entidade('professor', dados['professor_id']):
        return jsonify({'erro': f"Professor com ID {dados['professor_id']} nao encontrado"}), 404
        
    try:
        if 'nome_atividade' in dados: atividade.nome_atividade = dados['nome_atividade']
        if 'descricao' in dados: atividade.descricao = dados['descricao']
        if 'peso_porcento' in dados: atividade.peso_porcento = dados['peso_porcento']
        if 'data_entrega' in dados: 
            atividade.data_entrega = Atividade.from_dict({'data_entrega': dados['data_entrega'], 'nome_atividade': atividade.nome_atividade, 'turma_id': atividade.turma_id, 'professor_id': atividade.professor_id}).data_entrega

        if 'turma_id' in dados: atividade.turma_id = dados['turma_id']
        if 'professor_id' in dados: atividade.professor_id = dados['professor_id']

        db.session.commit()
        return jsonify(atividade.to_dict()), 200
    except ValueError:
        return jsonify({'erro': 'Data de entrega invalida. Use o formato DD/MM/AAAA'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro ao atualizar: {str(e)}'}), 500

@atividade_bp.route('/<int:id>', methods=['DELETE'])
def deletar_atividade(id):
    atividade = Atividade.query.get_or_404(id)
    try:
        db.session.delete(atividade)
        db.session.commit()
        return jsonify({'mensagem': 'Atividade deletada com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro ao deletar: {str(e)}'}), 500
