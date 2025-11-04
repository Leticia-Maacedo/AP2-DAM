from app.database import db
from datetime import datetime

class Atividade(db.Model):
    __tablename__ = 'atividades'

    id = db.Column(db.Integer, primary_key=True)
    nome_atividade = db.Column(db.String(50), nullable=False) # Adicionado conforme novo diagrama
    descricao = db.Column(db.String(100), nullable=True)
    peso_porcento = db.Column(db.Integer, nullable=True) 
    data_entrega = db.Column(db.Date, nullable=True)
    turma_id = db.Column(db.Integer, nullable=False)
    professor_id = db.Column(db.Integer, nullable=False)

    # Relacionamento com Notas (One-to-Many)
    notas = db.relationship('Nota', backref='atividade', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'nome_atividade': self.nome_atividade,
            'descricao': self.descricao,
            'peso_porcento': self.peso_porcento,
            'data_entrega': self.data_entrega.strftime('%d/%m/%Y') if self.data_entrega else None,
            'turma_id': self.turma_id,
            'professor_id': self.professor_id
        }

    @staticmethod
    def from_dict(data):
        data_entrega = None
        if data.get('data_entrega'):
             data_entrega = datetime.strptime(data['data_entrega'], '%d/%m/%Y').date()
        
        return Atividade(
            nome_atividade=data['nome_atividade'], # Adicionado
            descricao=data.get('descricao'),
            peso_porcento=data.get('peso_porcento'),
            data_entrega=data_entrega,
            turma_id=data['turma_id'],
            professor_id=data['professor_id']
        )