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

# Enable sudo _within_ the docker container
# https://stackoverflow.com/questions/25845538/how-to-use-sudo-inside-a-docker-container
RUN adduser -u 15560 --disabled-password --gecos '' jimfan
RUN adduser jimfan sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER jimfan

WORKDIR /home/jimfan

COPY entrypoint.py /mylibs/entrypoint.py
ENTRYPOINT ["/mylibs/entrypoint.py"]
