#!/bin/bash
var=$(echo "select * from configurations_configuration;" | sqlite3 db.sqlite3)
zero=0
if [ ${#var} -gt $zero ]
then
    echo "Greater"
fi