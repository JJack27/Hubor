#!/bin/bash
echo "Deploying the web application"

# check arguments
if [[ "$#" -lt 4 ]] ; then 
    echo "Invalid number of arguments."
    echo "Please follow the following format:"
    echo "  deploy.sh <absolute-dir-of-the-project> <name-of-the-project> <username> <domain-to-host>"
else
    echo "Directory of the project: $1"
    echo "Name of the project: $2"
    echo "Username: $3"
    echo "Domain: $4"
fi

# create virtual env of python
sudo apt update
sudo apt install -y python3-pip
sudo apt-get install -y sqlite3

# install required libraries
pip3 install virtualenv
cd ~
~/.local/bin/virtualenv -p python3 "$2"
source ~/$2/bin/activate
cd $1
pip install -r requirements.txt

# migrate the database
python manage.py makemigrations
python manage.py migrate 

# initialize the project
./init.sh

# create environment for frontend project
curl --silent --location https://deb.nodesource.com/setup_12.x  | sudo bash -
sudo apt-get install -y nodejs
sudo apt-get install -y npm

# build the frontend project
cd frontend
npm install
npm run build

# collect static files
cd $1
echo 'yes' | python manage.py collectstatic

# write <project-name>.socket
rm gunicorn.socket
echo "[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target" >> ./gunicorn.socket
sudo mv gunicorn.socket /etc/systemd/system/gunicorn.socket

# write <project-name>.service
rm gunicorn.service
echo "[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=$3
Group=www-data
WorkingDirectory=$1
ExecStart=/home/$3/$2/bin/gunicorn \
--access-logfile - \
--workers 3 \
--bind unix:/run/gunicorn.sock \
$2.wsgi:application

[Install]
WantedBy=multi-user.target" >> gunicorn.service
sudo mv gunicorn.service /etc/systemd/system/gunicorn.service

# start the gunicorn service
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
curl --unix-socket /run/gunicorn.sock localhost
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
echo "Finished deploying gunicorn"

# write <project-name> nginx conf
remove ./$2.conf
echo "Installing and deploying nginx"
sudo apt-get install -y nginx

echo "
upstream your-gunicorn {
    server unix:/run/gunicorn.sock;
}


server {
    listen 80 default_server;
    server_name _;
    return 301 https://\$host\$request_uri;
}

server {
    listen 443;

    server_name $4;

    # Root directory
    root $1;

    location = /favicon.ico { access_log off; log_not_found off; }

    # Allocating static files
    location /static/ {
        autoindex on;
        alias $1frontend/dist/static/;
        expires 1M;
        access_log off;
        add_header Cache-Control \"public\";
        proxy_ignore_headers \"Set-Cookie\";
    }

    location /media/ {
        autoindex on;
        alias $1media;
    }

    location @proxy_to_app {
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header Host \$http_host;
        proxy_redirect off;
        proxy_pass   http://your-gunicorn;
    }
    location / {
        try_files \$uri @proxy_to_app;
    }
}" >> $2.conf

sudo mv $2.conf /etc/nginx/sites-available/$2.conf
sudo rm /etc/nginx/sites-enabled/$2.conf
sudo ln -s /etc/nginx/sites-available/$2.conf /etc/nginx/sites-enabled/$2.conf  

# start the project
sudo systemctl restart nginx


# certbot
sudo apt-get install -y certbot python-certbot-nginx
sudo certbot
sudo certbot renew --dry-run