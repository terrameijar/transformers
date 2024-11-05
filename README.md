# PyCon Zim 2024 Code Examples

Welcome to the Docker Essentials for Python Developers code examples repository! This repo contains two distinct examples demonstrating how to Dockerize Flask applications. These examples are designed to help you understand the basics of containerization and how to apply it to both simple and complex applications.

## Complex Docker Example

The `complex_docker` directory contains an example of how to Dockerize a multi-container app using Docker Compose. This example includes a Flask application with a PostgreSQL database.

### Getting Started

1. **Navigate to the `complex_docker` directory:**

   ```sh
   cd complex_docker
   ```

2. **Build the Docker images and start the services:**

   ```sh
   docker-compose up --build
   ```

3. **Access the application:**

   Open your browser and navigate to `http://localhost:8001`.

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

The complex example includes custom Flask CLI commands:

- **Populate the database:**

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
