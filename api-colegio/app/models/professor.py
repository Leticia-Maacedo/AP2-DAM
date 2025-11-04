from app import db
from datetime import datetime

class Professor(db.Model):
    __tablename__ = 'professores'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer)
    materia = db.Column(db.String(100))
    observacoes = db.Column(db.Text)
    
    turmas = db.relationship('Turma', backref='professor', lazy=True)
    
    def __repr__(self):
        return f'<Professor {self.nome}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'idade': self.idade,
            'materia': self.materia,
            'observacoes': self.observacoes,
        }