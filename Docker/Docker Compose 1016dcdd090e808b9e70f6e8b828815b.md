# Docker Compose

**Docker Compose** is a tool used for defining and running multi-container Docker applications. It allows you to configure multiple services, networks, and volumes using a simple YAML file (`docker-compose.yml`). With Docker Compose, you can manage complex applications composed of several containers, making it ideal for managing microservices, testing environments, or complex multi-tier applications.

```yaml
services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"        # Maps port 8080 on the host to port 80 on the container
    volumes:
      - ./html:/usr/share/nginx/html  # Mounts a local directory for static HTML content
    depends_on:
      - db               # Ensures the 'db' service starts before the 'web' service

  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: example     # Set MySQL root password
      MYSQL_DATABASE: mydatabase       # Create a database named 'mydatabase'
      MYSQL_USER: user                 # Create a MySQL user
      MYSQL_PASSWORD: password         # Set the user's password
    volumes:
      - db_data:/var/lib/mysql         # Mount a volume for persistent database storage

volumes:
  db_data:
```

- **`services`**:
    - **`web`**:
        - Uses the **Nginx** image (`nginx:latest`).
        - Maps port `8080` on the host to port `80` inside the container.
        - Mounts the local directory `./html` to `/usr/share/nginx/html` inside the container to serve static HTML files.
        - **`depends_on`** ensures that the database service (`db`) starts before the Nginx service (`web`).
    - **`db`**:
        - Uses the **MySQL 5.7** image.
        - Sets environment variables to configure the MySQL database:
            - `MYSQL_ROOT_PASSWORD`: Root password for MySQL.
            - `MYSQL_DATABASE`: Creates a database named `mydatabase`.
            - `MYSQL_USER` and `MYSQL_PASSWORD`: Creates a new MySQL user with credentials.
        - Mounts a named volume (`db_data`) to persist MySQL data between container restarts.
- **`volumes`**:
    - **`db_data`**: A named volume to store the MySQL database files, ensuring data is persisted outside the container lifecycle.
1. **Create the file**:
    - Save the above YAML content into a file named `docker-compose.yml`.
2. **Run the services**:
    - In the same directory where the `docker-compose.yml` file is located, run:
        
        ```bash
        docker-compose up
        ```
        
    - This command will pull the required Docker images, create containers for the web and database services, and start them.
3. **Access the web service**:
    - Open your web browser and go to `http://localhost:8080`. The web service (Nginx) will serve any static files you place in the `./html` directory.
4. **Stopping the services**:
    - When you're done, stop and remove the containers, networks, and volumes using:
        
        ```bash
        docker-compose down
        ```
        

###