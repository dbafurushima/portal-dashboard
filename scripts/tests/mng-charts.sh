#!/bin/bash

python mngcli.py create-chart ID_CLIENT mem_usage --about "Memória utilizada" -t "Mem Usage" --prefix "%" --columns 10 --data-format "m-d H:M"
python mngcli.py upd-chart ID_CHART --file "data.txt"
