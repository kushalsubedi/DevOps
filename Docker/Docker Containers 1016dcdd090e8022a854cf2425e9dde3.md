# Docker Containers

A container is a lightweight, standalone, and executable software package that includes everything needed to run a piece of software

![image.png](image%204.png)

Once we grasp the concept of Docker images, we can see that Docker containers are closely related. Running an image initiates a runtime environment for it, known as a container.

In the section on Docker images [What are images in Docker](What%20are%20images%20in%20Docker%201016dcdd090e806399a8c8453ffc01fe.md), we discussed building an image from a Dockerfile. When you execute the image using the following command, it creates a container from that image.

```docker
docker run <image name> # in our case docker run my-image 
#this action will create a container where our application will be running 
```

to view the the created image you can run 

```docker
docker ps # lists all running container 
docker ps -a # list all containers wether they are running or dangling
```

remember the word dangling , dangling images and containers refers to un-used containers or images which can be remove to free up the space in our computer.