#!/bin/bash
echo "Initializing application"
redis-server --daemonize yes
echo $(redis-cli ping)


var=$(echo "select * from configurations_configuration;" | sqlite3 db.sqlite3)
zero=0
if [ ${#var} == $zero ]
then
    cat config.sql | sqlite3 db.sqlite3
fi


python manage.py runserver 0.0.0.0:8000