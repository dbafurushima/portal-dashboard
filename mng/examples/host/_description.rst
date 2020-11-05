Comando para manipulação do *objeto* ``Host`` na aplicação web **PortalD**.

Onde é possível criar um **Host** que representa uma máquina física, VM ou
um container dentro de um ambiente (*Environment*).

Uma instância Host contém as informações:

    * private_ip
    * public_ip
    * os_name
    * arch
    * platform
    * processor
    * hostname
    * ram
    * cores
    * frequency
    * equipment
    * service

Informações de hardware serão coletadas da máquina, mas caso queria editar
alguma informação como **service** pode utilizar o *subcommand* ``update``.