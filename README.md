# dockerly


TODO:

* Enable changing image by ENV variable
* Write dbuild and default image

## Troubleshoot

If you cannot copy a file into docker image (i.e. COPY command in Dockerfile), always check `.dockerignore`. Some repos have `'*'` in `.dockerignore` file to avoid sending huge amounts of context to Docker daemon.