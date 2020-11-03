#!/bin/bash
echo "Initializing application"

redis-server --daemonize yes
echo $(redis-cli ping)
cat config.sql | sqlite3 db.sqlite3