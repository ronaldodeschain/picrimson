comando para subir a imagem do postgres

docker run --name crimson-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=crimson_db -p 5432:5432 -d postgres
