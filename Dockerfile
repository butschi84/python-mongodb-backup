# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /usr/src/app

# copy the dependencies file to the working directory
COPY requirements.txt ./

# install dependencies
RUN pip install -r requirements.txt

# https://linuxize.com/post/how-to-install-mongodb-on-debian-9/
RUN apt update && apt install -y software-properties-common dirmngr
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
RUN add-apt-repository 'deb http://repo.mongodb.org/apt/debian stretch/mongodb-org/4.0 main'
RUN apt update && apt install mongodb-org-tools -y

# copy the content of the local src directory to the working directory
COPY src/ .

# command to run on container start
CMD [ "python", "/usr/src/app/main.py" ]