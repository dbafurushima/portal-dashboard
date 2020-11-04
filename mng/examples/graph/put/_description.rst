Adiciona dados a um gráfico em tempo real com informações a partir de um 
arquivo ou passando diretamente como argumento.

Os dados devem está em um padrão de DATE,VALUE
Caso você vá enviar mais de um valor deverá separar com ponto e vírgula ``;``
Ex: DATE_01,VALUE_01;DATE_02,VALUE_02;DATE_03,VALUE_03

O ``DATE`` deve está no padrão definido na criação do gráfico, o padrão
é ``Y-m-d H:M`` então deverá ser: ``2020-10-03 21:02,VALUE`` se for
mais de um dado: ``2020-11-03 21:02,VALUE; 2020-11-03 21:01,VALUE``