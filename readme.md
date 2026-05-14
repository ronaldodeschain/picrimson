comando para subir a imagem do postgres

docker run --name crimson-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=crimson_db -p 5432:5432 -d postgres

docker compose build 

autenticação de usuário <- Etapa atual>
camadas de serviço
testes de integração
testes de unidade