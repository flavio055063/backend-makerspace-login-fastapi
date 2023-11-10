Depois de instanciar as imagens do PostgresSQL e pgAdmin no docker, abra o pgAdmin e crie um banco de dados chamado makerDBv2.

Feito isso, no terminal do VSCode, execute o alembic conforme abaixo para a criação das tabelas:

    alembic revision --autogenerate -m "criando as tabelas"
    alembic upgrade head

Para executar o back-end e sua documentação (Swagger), execute no terminal VSCode:
    uvicorn app.main:app



