Microsserviços Colégio Porto

👥 Integrantes do Grupo

[Anna Julia Higa Farincho]

[Evelyn Mercês]

[Leticia Macedo]

🏗️ Arquitetura Utilizada

O sistema do Colégio Porto foi reestruturado utilizando a arquitetura de Microsserviços, orquestrada via Docker Compose. Cada serviço é totalmente independente, possui sua própria persistência de dados (SQLite/SQLAlchemy) e segue o padrão MVC (Model-View-Controller).

Descrição do Ecossistema e Integração

O sistema é composto por três microsserviços distintos, que se comunicam para garantir a integridade dos dados:

Serviço

Função Principal

Porta Host

Dependências Síncronas

Gerenciamento (api-colegio)

CRUD de Alunos, Professores e Turmas.

5000

Nenhuma.

Reservas (reservas)

Gerenciamento de reservas de salas.

5001

Valida a existência de Turma no Gerenciamento.

Atividades (atividades)

Gerenciamento de Atividades e Notas.

5002

Valida a existência de Professor, Turma e Aluno no Gerenciamento.

A comunicação é realizada de forma síncrona via chamadas HTTP (REST) entre os serviços, utilizando o nome do contêiner (http://api-colegio:5000/api) dentro da rede Docker.

🚀 Instruções de Execução (com Docker)

Pré-requisitos

Docker

Docker Compose

Passos para Inicialização

Estrutura de Pastas: Certifique-se de que a estrutura do seu projeto (docker-compose.yml e as pastas api-colegio, reservas, atividades) esteja correta.

Construção e Inicialização: Navegue até o diretório raiz do projeto e execute o comando:

docker-compose up --build


Este comando constrói e inicia os três microsserviços simultaneamente.

Verificação: Todos os serviços devem estar acessíveis pelas portas indicadas abaixo.

🌐 Descrição da API

Todos os microsserviços expõem suas rotas em /api/ e fornecem documentação interativa via Swagger UI na rota /docs.

Serviço

Entidades

Rotas Base

Swagger UI

Gerenciamento

Professor, Turma, Aluno

/api/professores, /api/turmas, /api/alunos

http://localhost:5000/docs

Reservas

Reserva

/api/reservas

http://localhost:5001/docs

Atividades

Atividade, Nota

/api/atividades, /api/notas

http://localhost:5002/docs

🧪 Explicação de Execução e Integração (Sequência de Teste)

Para demonstrar a integração e a dependência síncrona entre os serviços, siga esta sequência de requisições:

Passo 1: Criação de Entidades Base (Gerenciamento)

Devemos criar Turma e Professor no Gerenciamento para que as validações nos outros serviços funcionem.

POST http://localhost:5000/api/turmas (Crie uma Turma, ex: id=1).

POST http://localhost:5000/api/professores (Crie um Professor, ex: id=1).

Passo 2: Teste de Validação Síncrona (Atividades/Notas)

Teste POSITIVO: Tente criar uma Atividade usando o turma_id=1 e professor_id=1 criados acima.

Resultado Esperado: 201 Created (Comunicação Síncrona OK).

Teste NEGATIVO: Tente criar uma Atividade com turma_id=999.

Resultado Esperado: 404 Not Found (A validação síncrona impediu a criação).

Passo 3: Teste de Validação Síncrona (Reservas)

Teste POSITIVO: Tente criar uma Reserva usando o turma_id=1 criado no Passo 1.

Resultado Esperado: 201 Created (Comunicação Síncrona OK).