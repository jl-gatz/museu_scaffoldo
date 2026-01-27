# Museu API (scaffold)

API REST para gestão do Museu de Informática.

Este projeto tem como finalidade fornecer uma interface centralizada para o gerenciamento de informações do museu, incluindo usuários do sistema, equipamentos em exposição e registros de visitas. A API foi projetada para servir como base para aplicações web, mobile ou sistemas institucionais que necessitem acessar ou manter esses dados de forma estruturada.

## Escopo do projeto

A API contempla, entre outros, os seguintes domínios:

- Gestão de usuários
- Cadastro e controle de equipamentos do acervo
- Registro e consulta de visitas realizadas
- Organização de dados históricos do museu
- Base arquitetural para futuras expansões do sistema

## Stack tecnológica

### Stack atual

- Linguagem: **Python 3.10+**
- Framework web: **FastAPI**
- Validação e serialização de dados: **Pydantic**
- Servidor ASGI: **Uvicorn**
- Gerenciamento de dependências e ambiente virtual: **Poetry**
- Arquitetura orientada a APIs REST

### Stack planejada (em evolução)

- ORM: **SQLAlchemy**
- Migrations: **Alembic**
- Banco de dados: **PostgreSQL**

Essas tecnologias serão incorporadas progressivamente à medida que o projeto evoluir.

## Estrutura do projeto

O projeto segue boas práticas de organização para aplicações FastAPI, com separação clara de responsabilidades, incluindo:

- Rotas (endpoints da API)
- Schemas (validação e contratos de dados com Pydantic)
- Serviços (regras de negócio)
- Camada de persistência (a ser expandida com SQLAlchemy)
- Configurações e dependências

## Como executar o projeto

### Pré-requisitos

- Python 3.10 ou superior
- Poetry

### Passos

1. Clone o repositório:

    ```bash
    git clone https://github.com/jl-gatz/museu_scaffoldo.git
    ```

2. Acesse o diretório do projeto:

    ```bash
    cd museu_scaffoldo
    ```

3. Instale as dependências e crie o ambiente virtual:

    ```bash
    poetry install
    ```

4. Ative o ambiente virtual:

    ```bash
    poetry shell
    ```

5. Execute a aplicação:

    ```bash
    fastapi dev museu_scaffoldo/main.py
    ```

    Alternativamente, execute diretamente via Poetry:

    ```bash
    poetry run fastapi dev museu_scaffoldo/main.py
    ```

6. A API estará disponível em:

    ```
    http://localhost:8000
    ```

## Documentação da API

A documentação interativa dos endpoints é gerada automaticamente pelo FastAPI e pode ser acessada em:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)


## Contribuição

Contribuições são bem-vindas e incentivadas.

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature ou correção
3. Implemente as alterações
4. Envie um Pull Request descrevendo claramente o que foi modificado

## Licença

Este projeto está licenciado sob a licença **MIT**.  
Consulte o arquivo `LICENSE` para mais informações.

## Autor

Projeto mantido por [jl-gatz](https://github.com/jl-gatz)
