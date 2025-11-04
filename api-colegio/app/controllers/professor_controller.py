from flask import Blueprint, request, jsonify
from app import db
from app.models.professor import Professor

professor_bp = Blueprint('professores', __name__, url_prefix='/api/professores')


@professor_bp.route('/', methods=['GET'])
def listar_professores():
    professores = Professor.query.all()
    return jsonify([p.to_dict() for p in professores]), 200


@professor_bp.route('/<int:id>', methods=['GET'])
def buscar_professor(id):
    professor = Professor.query.get(id)
    
    if not professor:
        return jsonify({'erro': 'Professor nao encontrado'}), 404
    
    return jsonify(professor.to_dict()), 200


@professor_bp.route('/', methods=['POST'])
def criar_professor():
    dados = request.get_json()

    if not dados.get('nome'):
        return jsonify({'erro': 'Nome e obrigatorio'}), 400
    
    if dados.get('idade') is not None and not isinstance(dados['idade'], int):
        return jsonify({'erro': 'Idade deve ser um numero inteiro'}), 400

    novo = Professor(
        nome=dados['nome'],
        idade=dados.get('idade'),
        materia=dados.get('materia'),
        observacoes=dados.get('observacoes')
    )
    try:
        db.session.add(novo)
        db.session.commit()
        return jsonify(novo.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro ao criar professor: {str(e)}'}), 500


@professor_bp.route('/<int:id>', methods=['PUT'])
def atualizar_professor(id):
    professor = Professor.query.get(id)
    if not professor:
        return jsonify({'erro': 'Professor nao encontrado'}), 404

    dados = request.get_json()

    try:
        if 'nome' in dados:
            professor.nome = dados['nome']
            
        if 'idade' in dados:
            if not isinstance(dados['idade'], int) and dados['idade'] is not None:
                return jsonify({'erro': 'Idade deve ser um numero inteiro'}), 400
            professor.idade = dados['idade']
            
        if 'materia' in dados:
            professor.materia = dados['materia']
            
        if 'observacoes' in dados:
            professor.observacoes = dados['observacoes']

        db.session.commit()
        return jsonify(professor.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro ao atualizar: {str(e)}'}), 500


@professor_bp.route('/<int:id>', methods=['DELETE'])
def deletar_professor(id):
    professor = Professor.query.get(id)
    if not professor:
        return jsonify({'erro': 'Professor nao encontrado'}), 404

    try:
        db.session.delete(professor)
        db.session.commit()
        return jsonify({'mensagem': 'Professor deletado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro ao deletar: {str(e)}'}), 500