from flask import Blueprint, request, jsonify
from app.models.nota import Nota
from app.models.atividade import Atividade
from app.database import db
from .atividade_controller import validar_entidade

nota_bp = Blueprint('notas', __name__, url_prefix='/api/notas')

@nota_bp.route('/', methods=['POST'])
def criar_nota():
    dados = request.get_json()
    
    if not dados.get('aluno_id') or not dados.get('atividade_id') or dados.get('nota') is None:
        return jsonify({'erro': 'aluno_id, atividade_id e nota sao obrigatorios'}), 400

    if not Atividade.query.get(dados['atividade_id']):
        return jsonify({'erro': f"Atividade com ID {dados['atividade_id']} nao existe"}), 404
        
    if not validar_entidade('aluno', dados['aluno_id']):
        return jsonify({'erro': f"Aluno com ID {dados['aluno_id']} nao encontrado"}), 404
        
    try:
        nova_nota = Nota(
            nota=dados['nota'],
            aluno_id=dados['aluno_id'],
            atividade_id=dados['atividade_id']
        )
        db.session.add(nova_nota)
        db.session.commit()
        return jsonify(nova_nota.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro ao registrar nota: {str(e)}'}), 500

@nota_bp.route('/', methods=['GET'])
def listar_notas():
    notas = Nota.query.all()
    return jsonify([n.to_dict() for n in notas]), 200

@nota_bp.route('/<int:id>', methods=['GET'])
def obter_nota(id):
    nota = Nota.query.get_or_404(id)
    return jsonify(nota.to_dict()), 200

@nota_bp.route('/<int:id>', methods=['PUT'])
def atualizar_nota(id):
    nota_existente = Nota.query.get_or_404(id)
    dados = request.get_json()

    if 'atividade_id' in dados or 'aluno_id' in dados:
        return jsonify({'erro': 'Nao e permitido alterar aluno ou atividade de uma nota existente'}), 400

    if 'nota' in dados:
        nota_existente.nota = dados['nota']
        
    try:
        db.session.commit()
        return jsonify(nota_existente.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro ao atualizar nota: {str(e)}'}), 500

@nota_bp.route('/<int:id>', methods=['DELETE'])
def deletar_nota(id):
    nota_existente = Nota.query.get_or_404(id)
    try:
        db.session.delete(nota_existente)
        db.session.commit()
        return jsonify({"mensagem": "Nota deletada com sucesso!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro ao deletar nota: {str(e)}'}), 500