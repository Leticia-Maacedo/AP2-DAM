from flask import Blueprint, request, jsonify
from app.models.reserva import Reserva
from app.database import db
import requests

reserva_bp = Blueprint('reserva_bp', __name__)

GERENCIAMENTO_URL = "http://api-colegio:5000"  # nome do serviço no docker-compose

@reserva_bp.route('/reservas', methods=['POST'])
def criar_reserva():
    data = request.json
    turma_id = data.get('turma_id')

    # Valida turma no microsserviço de gerenciamento
    response = requests.get(f"{GERENCIAMENTO_URL}/turmas/{turma_id}")
    if response.status_code != 200:
        return jsonify({"erro": "Turma inválida"}), 400

    reserva = Reserva(
        num_sala=data['num_sala'],
        lab=data.get('lab', False),
        data=data.get('data'),
        turma_id=turma_id
    )
    db.session.add(reserva)
    db.session.commit()
    return jsonify(reserva.to_dict()), 201


@reserva_bp.route('/reservas', methods=['GET'])
def listar_reservas():
    reservas = Reserva.query.all()
    return jsonify([r.to_dict() for r in reservas])


@reserva_bp.route('/reservas/<int:id>', methods=['GET'])
def obter_reserva(id):
    reserva = Reserva.query.get_or_404(id)
    return jsonify(reserva.to_dict())


@reserva_bp.route('/reservas/<int:id>', methods=['PUT'])
def atualizar_reserva(id):
    reserva = Reserva.query.get_or_404(id)
    data = request.json
    reserva.num_sala = data.get('num_sala', reserva.num_sala)
    reserva.lab = data.get('lab', reserva.lab)
    reserva.data = data.get('data', reserva.data)
    db.session.commit()
    return jsonify(reserva.to_dict())


@reserva_bp.route('/reservas/<int:id>', methods=['DELETE'])
def deletar_reserva(id):
    reserva = Reserva.query.get_or_404(id)
    db.session.delete(reserva)
    db.session.commit()
    return jsonify({"mensagem": "Reserva deletada com sucesso!"})
