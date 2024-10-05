# Docker Demo (running an nginx image)

we will see a demo running an nginx image in this part 

before running to demo we need to have a basic understanding about **docker hub** 

[**Docker Hub](https://hub.docker.com/)** is a marketplace for docker images from where we can use images to create our image and container 

![image.png](image%205.png)

we can directly run an image from docker hub but the best practice is to use either a compose file or Dockerfile to use and run them we will talk more about compose in our next part in this demo we are going to use a Dockerfile 

```docker
**# Use the official Nginx image from the Docker Hub as the base image
FROM nginx:latest

# Copy custom configuration file to the Nginx configuration directory
# Uncomment and modify the following line if you have a custom nginx.conf
# COPY nginx.conf /etc/nginx/nginx.conf

# Copy static HTML files to the default Nginx content directory
# Uncomment and modify the following line if you have custom HTML files
# COPY html /usr/share/nginx/html

# Expose port 80 to allow traffic to the Nginx server
EXPOSE 80

# Define the default command to run when starting the container
CMD ["nginx", "-g", "daemon off;"]**

```

lets look at the commands ***ignore comments for now***   

The **FROM** keyword is used to define an base image which we are going to use in this case nginx after colon the latest is tag , we can see multiple tags available for the image in its official docker repository  

Another command **EXPOSE** is used to expose a port from the container in this case 80 which is the default port used by nginx , we can use any ports as per our requirements 

the last line **CMD** executes a command while running container 

```docker
**docker build -t my-nginx .**
```

```docker
**docker run -p 80:80 -d my-nginx 
# -p is to map ports from inside container to outside container 
# -d is used to run the container in detach mode i.e as a background process** 
```