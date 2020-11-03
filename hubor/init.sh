#!/bin/bash
redis-server --daemonize yes
redis-cli ping
cat config.sql | sqlite3 db.sqlite3