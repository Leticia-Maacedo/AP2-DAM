from app.database import db
from datetime import date

class Reserva(db.Model):
    __tablename__ = 'reservas'

    id = db.Column(db.Integer, primary_key=True)
    num_sala = db.Column(db.Integer, nullable=False)
    lab = db.Column(db.Boolean, default=False)
    data = db.Column(db.Date, default=date.today)
    turma_id = db.Column(db.Integer, nullable=False)  # ID vindo do serviço de gerenciamento

    def to_dict(self):
        return {
            "id": self.id,
            "num_sala": self.num_sala,
            "lab": self.lab,
            "data": self.data.strftime("%d/%m/%Y"),
            "turma_id": self.turma_id
        }
