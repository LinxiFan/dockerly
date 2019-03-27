# dockerly


TODO:

* Enable changing image by ENV variable
* Write dbuild and default image

Add the following lines to the end of your Dockerfile:

```Dockerfile
RUN mkdir /dockerly
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

COPY entrypoint.py /dockerly/
RUN chmod +x /dockerly/entrypoint.py
ENTRYPOINT ["/dockerly/entrypoint.py"]
```

## ~/.dockerly.yml

We recommend that you specify both `container_root` and `host_root` to be your home directory with the same absolute path (e.g. `/home/jimfan`). In this way, bash `~/` expansion will always work correctly. Otherwise only relative paths (e.g. `../neighbor/test.txt`) will work.

## Troubleshoot

If you cannot copy a file into docker image (i.e. COPY command in Dockerfile), always check `.dockerignore`. Some repos have `'*'` in `.dockerignore` file to avoid sending huge amounts of context to Docker daemon.