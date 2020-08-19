# Portal Dashboard

DESCRIPTION...

### INSTALAÇÃO

#### CONFIGURAÇÃO DA APLICAÇÃO WEB

Iniciamos configurando o arquivo variáveis de ambiente, para isso copie o arquivo 
``.env.example`` para ``.env``, em seguida preencha com as informações
necessárias. **tanto no root do projeto quanto na pasta /portald/**

#### INSTALAÇÃO COM ``Docker``

Copie o arquivo ``.env.example`` para ``.env`` (*o que está no root do projeto*), onde contém credenciais de acesso do mysql.
Após ter o arquivo ``.env`` preenchido com as informações necessárias você já pode fazer o build (*deverá ter feito a etapa anterior que é a de configurar a aplicação*) com o comando ``docker-compose build`` e para subir os contêiners ``docker-compose up [-d]``

#### INFORMAÇÕES SOBRE CONTAINERS

* **ports**
  * 3306 (``MySQL``)
  * 8080:80 (``PortalD``)
  * 8100:8100 (``PortalD``)

* **volumes**
  * /var/lib/mysql (``MySQL``)
  * /var/www/portald/ (``PortalD``)

* **network**: us-east-1:bridge

### INSTALAÇÃO DO PROJETO EM LINUX/WINDOWS (*versão de desenvolvimento*)

Você deve ter previamente instalado o **Python3.8.*** (versão utilizada no desenvolvimento) e um banco de dados MySQL (atualmente com SQLite).

> Se sua distribuição Linux for Ubuntu deverar instalar o pacote ``libmysqlclient-dev`` para que não dê erro na instalação do conector MySQL.

Após fazer o clone do projeto, instale as bibliotecas do python com o ``pip`` que o projeto depende:

```
pip install Django==3.0.8 \
    django-environ==0.4.5
```

> **ATENÇÃO** se você estiver usando ``windows`` deve instalar o ``mysqlclient``, faça download [nesse site](https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient)

```
[client]
host = 
database = 
user = 
password = 
default-character-set = utf8
```

Realize as migrações com os comandos:

```
python manage.py makemigrations
python manage.py migrate
```

> você deve está na pasta ``portald/``

E agora só subir o servidor com o comando ``python manage.py runserver``
