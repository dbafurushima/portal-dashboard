# CHANGELOG.md

## v0.1

* Novo arquivo `Dockerfile.dev` com imagem a partir do `python:3.8.6` sem o `apache2`.
* Mudança no script shell `wait-for-mysql.sh` para receber como argumento o usuário de login para teste de comunicação.
* Mudança na lib de carregamento de variaveis, agora é utilizado o `python-dotenv`.
* Carregamento de credenciais de acesso ao banco `MySQL` a partir de variáveis de ambiente.
* Arquivo `portald/example.env` com variáveis de acesso ao banco.
* Novo arquivo `Makefile` para ajudar no deploy e inicialização da aplicação. Possui os seguintes comandos:
    * `make compose` faz deploy da aplicação com `docker-compose` a partir do `docker-compose.dev.yml`
    * `make createsuperuser` cria um usuário admin na aplicação.
    * `make migrate` cria migrações no banco.
