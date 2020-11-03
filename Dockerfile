FROM ubuntu:20.10
LABEL maintainer="yizhou4@ualberta.ca"

# Exposing ports
EXPOSE 80
EXPOSE 22
EXPOSE 433
EXPOSE 6379

# install python and pip
RUN apt-get update
RUN echo y | apt-get install python3
RUN echo y | apt-get install python3-pip
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

# install nginx, git, sqlite3
RUN echo y | apt-get install git
RUN echo y | apt-get install nginx
RUN echo y | apt-get install sqlite3

# install redis
WORKDIR /root
RUN echo y | apt-get install wget
RUN wget http://download.redis.io/redis-stable.tar.gz
RUN tar xvzf redis-stable.tar.gz
WORKDIR /root/redis-stable
RUN make
RUN make install

# download hubor
WORKDIR /root
RUN git clone https://github.com/JJack27/Hubor.git
WORKDIR /root/Hubor/hubor
RUN pip3 install -r ./requirements.txt
RUN python ./manage.py makemigrations accounts
RUN python ./manage.py makemigrations configurations
RUN python ./manage.py makemigrations data
RUN python ./manage.py makemigrations emergency
RUN python ./manage.py migrate
CMD [ "./init.sh" ]



