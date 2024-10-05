# What are images in Docker

A [Docker](https://www.techtarget.com/searchitoperations/definition/Docker) image is a file used to execute code in a Docker [container](https://www.techtarget.com/searchitoperations/definition/container-containerization-or-container-based-virtualization). Docker images act as a set of instructions to build a Docker cotainer, such as a template. Docker images also act as the starting point when using Docker. An image is comparable to a snapshot in virtual machine ([VM](https://www.techtarget.com/searchitoperations/definition/virtual-machine-VM)) environments.

![image.png](image%203.png)

```docker
FROM python:3.12-slim
WORKDIR /app
copy . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python","app.py"]
```

An example of Docker-file , the dockerfile is compile into an image like an C file is compile down to an .exe or .out file and Java files are compile down to jar files 

we can use following command to build an Docker image 

```docker
docker buld -t my-image . 
# docker build command build docker file into an image 
# -t flag is used to give a tag to image tags are basically a name to image 
# which is my-image in this case
# the last "." specifies where is our docker file "." means current directory 
# if we have to use file from another directory we can use following command 
docker build -t my-image -f </path/to/Dockerfile> # replace <> with actual path
```