from flask import Blueprint, request, jsonify
from app import db
from app.models.turma import Turma
from app.models.professor import Professor

turma_bp = Blueprint('turmas', __name__, url_prefix='/api/turmas')


@turma_bp.route('/', methods=['GET'])
def listar_turmas():
    turmas = Turma.query.all()
    return jsonify([t.to_dict() for t in turmas]), 200


@turma_bp.route('/<int:id>', methods=['GET'])
def buscar_turma(id):
    turma = Turma.query.get(id)
    
    if not turma:
        return jsonify({'erro': 'Turma nao encontrada'}), 404
    
    return jsonify(turma.to_dict()), 200


@turma_bp.route('/', methods=['POST'])
def criar_turma():
    dados = request.get_json()
    
    if not dados.get('descricao'):
        return jsonify({'erro': 'Descricao e obrigatoria'}), 400
    
    if dados.get('professor_id'):
        professor = Professor.query.get(dados['professor_id'])
        if not professor:
            return jsonify({'erro': 'Professor nao encontrado'}), 404
    
    try:
        nova_turma = Turma(
            descricao=dados['descricao'],
            professor_id=dados.get('professor_id'),
            ativo=dados.get('ativo', True)
        )
        
        db.session.add(nova_turma)
        db.session.commit()
        
        return jsonify(nova_turma.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro ao criar turma: {str(e)}'}), 500


@turma_bp.route('/<int:id>', methods=['PUT'])
def atualizar_turma(id):
    turma = Turma.query.get(id)
    
    if not turma:
        return jsonify({'erro': 'Turma nao encontrada'}), 404
    
    dados = request.get_json()
    
    try:
        if 'descricao' in dados:
            turma.descricao = dados['descricao']
            
        if 'ativo' in dados:
            turma.ativo = dados['ativo']
        
        if 'professor_id' in dados:
            if dados['professor_id'] is not None:
                professor = Professor.query.get(dados['professor_id'])
                if not professor:
                    return jsonify({'erro': 'Professor nao encontrado'}), 404
            turma.professor_id = dados['professor_id']
        
        db.session.commit()
        return jsonify(turma.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro ao atualizar: {str(e)}'}), 500


@turma_bp.route('/<int:id>', methods=['DELETE'])
def deletar_turma(id):
    turma = Turma.query.get(id)
    
    if not turma:
        return jsonify({'erro': 'Turma nao encontrada'}), 404
    
    if turma.alunos:
        return jsonify({'erro': 'Nao e possivel deletar turma com alunos vinculados'}), 400
    
    try:
        db.session.delete(turma)
        db.session.commit()
        return jsonify({'mensagem': 'Turma deletada com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro ao deletar: {str(e)}'}), 500