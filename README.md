# Transformers Flask API

This project is a Flask application that manages a database of Transformers characters. It includes a PostgreSQL database for production and SQLite for development. The application can be deployed using Docker Compose for local testing and Kubernetes for production.

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- (Optional) Kubernetes (kubectl and a running cluster)

### Local Development

1. **Clone the repository:**

   ```sh
   git clone https://github.com/terrameijar/transformers.git
   cd transformers
   ```

2. **Set up the environment variables:**
   Create a `.env` file in the `transformers` directory with the following content:

```env
POSTGRES_USER=<your_postgres_username>
POSTGRES_PASSWORD=<your_postgres_password>
POSTGRES_DB=<your_transformers_db_name>

```

3. **Build the Docker images and start the services:**

```shell
docker compose up --build
```

4. **Access the application:**

Open your browser and navigate to `http://localhost:8001`.

### Kubernetes Deployment

1. **Apply the Kubernetes configurations:**

Navigate to the project root directory and run:

```shell
kubectl apply -f k8s/
```

2. **Access the application:**
   There are two ways to access this application depending on where it is run; via an internal IP or an external IP (if available).

### Public Cloud Setup

If running this on a public cloud like AWS, GKE or similar, set up the Transformers service as a load balancer by modifying `k8s/transformers-service.yaml` to use `LoadBalancer` type:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: transformers-service
spec:
  selector:
    app: transformers
  ports:
    - protocol: TCP
      port: 8000
      targetPort: 8000
  type: LoadBalancer
```

Apply the modified service configuration:

```shell
kubectl apply -f k8s/transformers-service.yaml
```

Wait for the external IP to be assigned. You can check the status using:

```shell
kubectl get services
```

Once the IP is assigned, open your browser and navigate to http://<external-ip>:8000.

### On Prem/Bare Metal Set up

- Install MetalLB in your Kubernetes cluster following the [MetalLB Installation guide](https://metallb.universe.tf/installation/).

- Configure MetalLB with a pool of IP addresses using the `k8s/metallb-config.yaml` file.

- Apply the MetalLB configuration:

```shell
kubectl apply -f k8s/metallb/metallb-config.yaml
```

Check the external IP:

```shell
kubectl get services
```

Once the external IP is assigned, open your browser and navigate to http://<your-server-ip>

### Code Overview

-

app.py

: The main Flask application file.

-

commands.py

: Custom Flask CLI commands for managing the database.

- [`config.py`]: Configuration settings for the Flask application.
- [`models.py`]: SQLAlchemy models for the application.
-

requirements.txt

: Python dependencies for the application.

-

Dockerfile

: The Dockerfile used to build the Docker image.

-

docker-compose.yml

: The Docker Compose file used to define and run multi-container Docker applications.

- `templates/`: HTML templates for the application.
- `static/`: Static files such as CSS and JavaScript.
- `migrations/`: Database migration files managed by Flask-Migrate.

### Custom Commands

The transformers app contains custom Flask CLI commands that can be run from within the transformers api container:

- **Populate the database:**

Exec into the API container and run this command to populate the database:

```sh
flask populate_db
```

- **Delete duplicate Transformers:**

  ```sh
  flask delete_duplicates
  ```

### Database Migrations

To manage database migrations, use the following commands:

1. **Initialize the migrations directory:**

   ```sh
   flask db init
   ```

2. **Create a migration script:**

   ```sh
   flask db migrate -m "Initial migration."
   ```

3. **Apply the migration:**

   ```sh
   flask db upgrade
   ```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

These examples are designed to help you get started with Docker and Flask, providing a foundation for building and deploying your own applications. Enjoy exploring and learning at PyCon Zim 2024!
