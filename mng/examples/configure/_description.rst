Configure as opções do MNG CLI. Ao chamar esse comando diretamente
será pedido para que informe as informações necessárias para que
a ferramenta funcione corretamente. Caso já tenha configurado os
valores anteriores serão usado como default. Ex: ``User Api [None]``
é exibido na primeira interação, se for preencido com *api* quando
o comando for invocado novamente irá aparecer ``User Api [api]``.

Nota: Todas as informações de configuração serão escritas no arquivo:
(``~/.aws/credentials``).

=========================
Variáveis de configuração
=========================

As seguintes variáveis de configuração são compatíveis com o arquivo de configuração:

* **address_api** - Endereço IPv4 ou nome de domínio do servidor da API.
* **port_api** - Porta em que a API está utilizando.
* **username_api** - Usuário para acessar a API da página web.
* **password_api** - Senha do usuário para login na API.
* **base64auth** - string em base64 para basic authetication. Apenas leitura, será gerado
automaticamente ao preencher usuário e senha da API.

Para obter mais informações sobre as opções de configuração, ver 
`[MNG CLI] configure`_ no *Github Wiki*.

.. _`[MNG CLI] configure`: https://github.com/dbafurushima/portal-dashboard/wiki/MNG-CLI#configure