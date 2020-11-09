Comando para manipulação do *objeto* ``Serice`` na aplicação web **PortalD**.

Onde é possível criar um **Serviço** que pode ser composto por várias
*instâncias* ou está em apenas um ``Host``.

Uma instância Host contém as informações:

    * name
    * ip
    * port
    * dns

Você pode criar um serviço apenas com um nome, já que é o uníco parametro
obrigatório e relacionar ele posteriomente com um ``Host`` ou ``Instance``.

Lembrando que o relacionamento deverá ser feito não no objeto *Service* mas
sim no *Host* ou *Instance*.