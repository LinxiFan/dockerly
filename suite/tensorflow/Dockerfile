FROM tensorflow/tensorflow:latest-gpu-py3

RUN apt-get update -qq -y \
 && apt-get install -y libsm6 libxrender1 libxext-dev python3-tk\
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /opt/
RUN pip3 install --upgrade pip
RUN pip3 install cmake
#RUN pip3 install dlib --install-option=--yes --install-option=USE_AVX_INSTRUCTIONS
RUN pip3 install dlib
RUN pip3 --no-cache-dir install -r /opt/requirements.txt && rm /opt/requirements.txt

# patch for tensorflow:latest-gpu-py3 image
RUN cd /usr/local/cuda/lib64 \
 && mv stubs/libcuda.so ./ \
 && ln -s libcuda.so libcuda.so.1 \
 && ldconfig

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

ENTRYPOINT ["/dockerly/entrypoint.py"]

