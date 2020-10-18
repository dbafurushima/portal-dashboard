#!/bin/bash
# wait-for-mysql.sh

set -e

host="$1"
shift
mysql_root_password="$1"
shift
cmd="$@"

until mysql -u root "-p$mysql_root_password" -h "$host" -e 'show databases' 2> /dev/null; do
  >&2 echo "ops... mysql down - sleeping"
  sleep 5
done
  
>&2 echo "mysql is up - executing command"
>&2 echo "exec migrations"

python3 /var/www/portald/manage.py makemigrations
python3 /var/www/portald/manage.py migrate
python3 /var/www/portald/manage.py collectstatic --no-input

$cmd