Dado um arquivo de configuração vazio, os seguintes comandos::

    $ mng configure set address_api 10.0.1.100
    $ aws configure set port_api 8080

irá produzir o seguinte arquivo de configuração ``~/.config/mng.ini``::

    [default]
    address_api = 10.0.1.100
    port_api = 8080
