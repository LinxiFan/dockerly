FROM ubuntu:18.04

# Base dependency
RUN mkdir /mylibs
WORKDIR /mylibs
RUN apt-get update && apt-get install -y build-essential cmake unzip bzip2 curl git wget libglfw3 libglu1-mesa-dev libglew-dev libgl1-mesa-dev libgl1-mesa-glx libglew-dev libosmesa6-dev xserver-xorg-video-dummy xorg-dev patchelf libpoppler-cpp-dev pkg-config

# python deps
WORKDIR /mylibs
RUN curl -LO http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh \
	&& bash Miniconda3-latest-Linux-x86_64.sh -p /mylibs/miniconda -b
RUN rm /mylibs/Miniconda3-latest-Linux-x86_64.sh
ENV PATH=/mylibs/miniconda/bin:${PATH}

# required for imageio
RUN conda install -y ffmpeg -c conda-forge

# RUN conda install --yes pytorch-cpu torchvision -c pytorch
COPY requirements.txt /mylibs/
RUN pip install -r /mylibs/requirements.txt

RUN apt-get install -y sudo vim

# imagemagick is paranoid on permission, you need to set its policy explicitly
RUN apt-get install -y imagemagick
RUN sed -i 's/rights="none"/rights="read|write"/g' /etc/ImageMagick-6/policy.xml

# =============== INSTALL MONGODB ===============
# Follow official community edition installation on Ubuntu:
# https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/
# remove all sudos, because we will be setting USER and UID later
# run by `sudo mongod`, NOT `sudo service mongod start` (which will report error
# "service not found")!!!
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
RUN echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
RUN apt-get update

# avoid tzdata asking for geographic location interactively: https://bugs.launchpad.net/ubuntu/+source/tzdata/+bug/1554805
RUN ln -fs /usr/share/zoneinfo/US/Pacific-New /etc/localtime
RUN apt-get install -y tzdata
RUN dpkg-reconfigure -f noninteractive tzdata
RUN apt-get install -y mongodb-org

RUN echo "mongodb-org hold" | dpkg --set-selections
RUN echo "mongodb-org-server hold" | dpkg --set-selections
RUN echo "mongodb-org-shell hold" | dpkg --set-selections
RUN echo "mongodb-org-mongos hold" | dpkg --set-selections
RUN echo "mongodb-org-tools hold" | dpkg --set-selections

RUN mkdir -p /data/db /data/configdb \
    && chown -R mongodb:mongodb /data/db /data/configdb
VOLUME /data/db /data/configdb

RUN mkdir /dockerly
COPY entrypoint.py /dockerly/
RUN chmod +x /dockerly/entrypoint.py

# args from `docker build --build-arg key=value`
# https://vsupalov.com/docker-arg-vs-env/
ARG USER=docker
ARG UID=1001
RUN echo USER=$USER, UID=$UID

# Enable sudo _within_ the docker container
# https://stackoverflow.com/questions/25845538/how-to-use-sudo-inside-a-docker-container
RUN adduser -u $UID --disabled-password --gecos '' $USER
RUN adduser $USER sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER $USER

# EXPOSE 8888
ENTRYPOINT ["/dockerly/entrypoint.py"]

