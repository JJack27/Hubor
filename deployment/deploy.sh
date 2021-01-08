#!/bin/bash

echo "Deploying the web application"

# check arguments
if ["$#" == 0]; then 
    echo "Invalid number of arguments."
    echo "Please follow the following format:"
    echo "\tdeploy.sh <absolute-dir-of-the-project> <name-of-the-project>"
else
    echo "Directory of the project: $0"
    echo "Name of the project: $1"
fi

# create virtual env of python
sudo apt update
sudo apt install python3-pip

# install required libraries
pip3 install virtualenv
virtualenv -p python3 "$1"
source 

# migrate the database
# initialize the project
# build the frontend project
# collect static files
# write <project-name>.socket
# write <project-name>.service
# write <project-name> nginx conf
# start the project