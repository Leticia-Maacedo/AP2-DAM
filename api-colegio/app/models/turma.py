from app import db


class Turma(db.Model):
    __tablename__ = 'turmas'

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'))
    ativo = db.Column(db.Boolean, default=True)
    
    professor_responsavel = db.relationship('Professor', backref='turmas_que_leciona', lazy=True)
    alunos = db.relationship('Aluno', backref='turma', lazy=True)

    def __repr__(self):
        return f'<Turma {self.descricao}>'

    def to_dict(self):
        return {
            'id': self.id,
            'descricao': self.descricao,
            'professor_id': self.professor_id,
            'ativo': self.ativo,
        }