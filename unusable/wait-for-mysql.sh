#!/bin/bash

set -e

host="$1"
shift
port="$1"
shift
mysql_user="$1"
shift
mysql_password="$1"
shift
cmd="$@"

until mysql -u ${mysql_user} "-p$mysql_password" -h "$host" -p ${port} -e 'show databases' 2> /dev/null; do
  >&2 echo "ops... mysql down - sleeping"
  sleep 1
done
  
>&2 echo "mysql is up - executing command"
>&2 echo "exec migrations"

python3 /usr/src/app/manage.py makemigrations --merge
python3 /usr/src/app/manage.py makemigrations
python3 /usr/src/app/manage.py migrate
python3 /usr/src/app/manage.py collectstatic --no-input

$cmd