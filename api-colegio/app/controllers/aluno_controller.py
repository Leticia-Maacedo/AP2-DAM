from flask import Blueprint, request, jsonify
from app import db
from app.models.aluno import Aluno
from app.models.turma import Turma
from datetime import datetime

aluno_bp = Blueprint('alunos', __name__, url_prefix='/api/alunos')


@aluno_bp.route('/', methods=['GET'])
def listar_alunos():
    alunos = Aluno.query.all()
    return jsonify([a.to_dict() for a in alunos]), 200


@aluno_bp.route('/<int:id>', methods=['GET'])
def buscar_aluno(id):
    aluno = Aluno.query.get(id)
    
    if not aluno:
        return jsonify({'erro': 'Aluno nao encontrado'}), 404
    
    return jsonify(aluno.to_dict()), 200


@aluno_bp.route('/', methods=['POST'])
def criar_aluno():
    dados = request.get_json()
    
    if not dados.get('nome'):
        return jsonify({'erro': 'Nome e obrigatorio'}), 400
    if not dados.get('data_nascimento'):
        return jsonify({'erro': 'Data de nascimento e obrigatoria'}), 400
    if not dados.get('idade'):
        return jsonify({'erro': 'Idade e obrigatoria'}), 400
    
    if dados.get('turma_id'):
        turma = Turma.query.get(dados['turma_id'])
        if not turma:
            return jsonify({'erro': 'Turma nao encontrada'}), 404
    
    try:
        data_nasc = datetime.strptime(dados['data_nascimento'], '%d/%m/%Y').date()
        
        novo_aluno = Aluno(
            nome=dados['nome'],
            data_nascimento=data_nasc,
            idade=dados['idade'],
            nota_primeiro_semestre=dados.get('nota_primeiro_semestre'),
            nota_segundo_semestre=dados.get('nota_segundo_semestre'),
            media_final=dados.get('media_final'),
            turma_id=dados.get('turma_id')
        )
        
        db.session.add(novo_aluno)
        db.session.commit()
        
        return jsonify(novo_aluno.to_dict()), 201
        
    except ValueError:
        return jsonify({'erro': 'Data de nascimento invalida. Use o formato DD/MM/AAAA'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro ao criar aluno: {str(e)}'}), 500


@aluno_bp.route('/<int:id>', methods=['PUT'])
def atualizar_aluno(id):
    aluno = Aluno.query.get(id)
    
    if not aluno:
        return jsonify({'erro': 'Aluno nao encontrado'}), 404
    
    dados = request.get_json()
    
    try:
        if 'nome' in dados:
            aluno.nome = dados['nome']
            
        if 'data_nascimento' in dados:
            aluno.data_nascimento = datetime.strptime(dados['data_nascimento'], '%d/%m/%Y').date()
        
        if 'idade' in dados:
            aluno.idade = dados['idade']
        
        if 'nota_primeiro_semestre' in dados:
            aluno.nota_primeiro_semestre = dados['nota_primeiro_semestre']
            
        if 'nota_segundo_semestre' in dados:
            aluno.nota_segundo_semestre = dados['nota_segundo_semestre']

        if 'media_final' in dados:
            aluno.media_final = dados['media_final']
        
        if 'turma_id' in dados:
            if dados['turma_id']:
                turma = Turma.query.get(dados['turma_id'])
                if not turma:
                    return jsonify({'erro': 'Turma nao encontrada'}), 404
            aluno.turma_id = dados['turma_id']
        
        db.session.commit()
        return jsonify(aluno.to_dict()), 200
        
    except ValueError:
        return jsonify({'erro': 'Data de nascimento invalida. Use o formato DD/MM/AAAA'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro ao atualizar: {str(e)}'}), 500


@aluno_bp.route('/<int:id>', methods=['DELETE'])
def deletar_aluno(id):
    aluno = Aluno.query.get(id)
    
    if not aluno:
        return jsonify({'erro': 'Aluno nao encontrado'}), 404
    
    try:
        db.session.delete(aluno)
        db.session.commit()
        return jsonify({'mensagem': 'Aluno deletado com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': f'Erro ao deletar: {str(e)}'}), 500