# FastAPI DDD

Este projeto é uma implementação de exemplo utilizando o [FastAPI](https://fastapi.tiangolo.com/) com os princípios de Domain-Driven Design (DDD). O objetivo é demonstrar como estruturar uma aplicação FastAPI de forma escalável e modular, aplicando os conceitos de DDD.

## Estrutura do Projeto

A estrutura do projeto é organizada da seguinte forma:

- **src/**: Contém o código-fonte da aplicação.
  - **core/**: Inclui configurações e utilitários centrais.
  - **domains/**: Cada domínio da aplicação possui seu próprio diretório, contendo suas entidades, repositórios, serviços e esquemas.
  - **api/**: Define os endpoints da API, organizados por domínio.
- **tests/**: Contém os testes automatizados da aplicação.

Essa organização segue as melhores práticas de DDD, separando claramente as responsabilidades de cada componente.

## Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e de alta performance para construção de APIs com Python.
- **SQLAlchemy**: ORM para interações com o banco de dados relacional.
- **Pydantic**: Validação de dados e gerenciamento de configurações.
- **PostgreSQL**: Banco de dados relacional utilizado na aplicação.
- **Docker**: Ferramenta para containerização da aplicação.

## Configuração e Execução

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/rafaelign/fastapi-ddd.git
   cd fastapi-ddd
   ```

2. **Configure as variáveis de ambiente:**

   Renomeie o arquivo `.env.example` para `.env` e ajuste as configurações conforme necessário.

3. **Construa e inicie os containers Docker:**

   ```bash
   docker-compose up --build
   ```

4. **Acesse a documentação interativa da API:**

   Após iniciar a aplicação, acesse `http://localhost:8000/docs` para visualizar a documentação gerada automaticamente pelo Swagger UI.

## Testes

Para executar os testes automatizados, utilize o seguinte comando:

```bash
docker-compose exec app pytest
```

Isso executará os testes definidos no diretório `tests/`.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests para melhorar este projeto.

