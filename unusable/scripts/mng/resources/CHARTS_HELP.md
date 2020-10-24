### create

Cria um gráfico customizado para um cliente. Para maior praticidade foram definidos apenas dois parâmetros obrigatórios, mas com os parâmetros opcionais pode obter maior customização.

Obrigatórios:
* `-cid` `or` `--clientid-to-chart`
* `-chn` `or` `--chart-name`

Exemplo:

Cria um gráfico do tipo linha para o cliente com **ID** 1 que informará o uso da CPU por segundo.

```
mng charts create -cid 1 -chn "usage_cpu" -t "Usage CPU per/s" \
    --prefix "%" -fmt "Y-m-d H:M:S" --type-chart line --type-data number \
    --about "USAGE CPU" --columns 12
```

### put

Alimenta um gráfico com novos dados passado pelo *CLI*. Você deve se ater ao formato dos dados, sempre deverá está acompanhado de uma data no formato predefinido na criação do gráfico, exemplo, para alimentar o gráfico criado no exemplo a cima você pode usar o seguinte comando:

Obrigatórios:

* `--chartid`
* `--value` `OR` `--file`

```
mng charts put --chartid CHART_ID --value "2020-10-19 18:16:00,20;2020-10-19 18:16:01,26"
```
Repare que são enviados dois dados, um com valor **20** e o outro com valor **26** na data *2020-10-19 18:16* em segundos diferentes, separado pelo carácter de ponto e virgula `;` mas também poderia ser apenas um espaço ` `

Outra forma poderia ser por um arquivo de texto, para isso crie um arquivo de exemplo com o nome `example-usege-cpu-data.txt` e insira os dados nele:

```
2020-10-19 18:16:02,30;2020-10-19 18:16:03,20
2020-10-19 18:16:04,35
2020-10-19 18:16:05,44
```

e utilize o comando:

```
mng charts put --chartid CHART_ID --file example-usege-cpu-data.txt
```

O separador nesse caso pode ser uma quebra de linha `\n`, o `;` ou um espaço em branco ` `

### list

Faz a listagem de todos os gráficos de todos os clientes, a consulta trás todos atributos, se você quer um filtro recomendo a utilização do comando `grep` ou `less` como pipeline já até no dia que foi escrito está wiki não existe um filtro na consulta.
