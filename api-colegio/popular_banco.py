from app import create_app, db
from app.models.professor import Professor
from app.models.turma import Turma
from app.models.aluno import Aluno
from datetime import datetime 

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    
    print("Populando banco de dados....")
    prof1 = Professor(
        nome='Kleber Chiles',
        email='kleber.chiles@colegioporto.com.br',
        cpf='123.456.789-01',
        idade=32,
        materia='DevOps'
    )
    
    prof2 = Professor(
        nome='Giovani Bontempo',
        email='giovani.bontempo@colegioporto.com.br',
        cpf='123.456.789-02',
        idade=43,
        materia='API'
    )
    
    prof3 = Professor(
        nome='Odair Gabriel',
        email='odair.gabriel@colegioporto.com.br',
        cpf='123.456.789-03',
        idade=47,
        materia='Desenvolvimento Mobile'
    )
    
    db.session.add_all([prof1, prof2, prof3])
    db.session.commit()
    print("✓ Professores criados")
    
    turma = Turma(
        nome='SI 3A',
        ano=2025,
        periodo='noite',
        professor_id=prof3.id
    )
    
    db.session.add(turma)
    db.session.commit()
    print("✓ Turma criada")
    
    aluna1 = Aluno(
        nome='Anna Julia Higa Farincho',
        email='anna.farincho@email.com',
        cpf='987.654.321-01',
        data_nascimento=datetime.strptime('15/03/2004', '%d/%m/%Y').date(),
        idade=20,
        nota_final=7.8,
        situacao='aprovado',
        turma_id=turma.id
    )
    
    aluna2 = Aluno(
        nome='Letícia Macedo',
        email='leticia.macedo@email.com',
        cpf='987.654.321-02',
        data_nascimento=datetime.strptime('22/07/2004', '%d/%m/%Y').date(),
        idade=20,
        nota_final=8.2,
        situacao='aprovado',
        turma_id=turma.id
    )
    
    aluna3 = Aluno(
        nome='Evelyn Mercês',
        email='evelyn.merces@email.com',
        cpf='405.025.308-98',
        data_nascimento=datetime.strptime('10/02/2005', '%d/%m/%Y').date(),
        idade=20,
        nota_final=7.5,
        situacao='aprovado',
        turma_id=turma.id
    )
    
    db.session.add_all([aluna1, aluna2, aluna3])
    db.session.commit()
    print("✓ Alunas criadas")
    
    print("\n" + "="*50)
    print("Banco de dados populado com sucesso!")
    print("="*50)
    print(f"Professores: {Professor.query.count()}")
    print(f"Turmas: {Turma.query.count()}")
    print(f"Alunos: {Aluno.query.count()}")
    print("="*50)
