# Changelog

## 0.0.2 (07-10-2020)

### Features

Mudança na organização dos parâmetros, foi adicionado um suporte a subcomandos,
help e usage mais robusto e customizado.

Agora o CLI é utilizado no seguinte padrão:
```
$ mng command subcommand [parameters]
       ^^^^     ^^^^^^
   [host,...] [list, create, ....] [--id, --key, ...]
```
Também foi adicionado funções para validar a utilização correta dos comandos e
uma pré definição que auxilia na lógica de negócio e rápida aprendizagem.
