# Deployment

This guide explains how to deploy Nevron using Docker and various cloud platforms.

## Docker Deployment

Nevron comes with a pre-configured Dockerfile that allows you to run the agent in a containerized environment. This provides consistency across different deployment environments and makes it easy to deploy the agent anywhere that supports Docker.

### Prerequisites

- Docker installed on your system
- `.env` file with proper configuration
- Sufficient disk space for logs

### Building the Docker Image

To build the Docker image, run the following command from the root directory of the project:

```bash
docker build -t nevron:latest .
```

### Running the Container

To run the Nevron container, you need to:
1. Mount the logs directory
2. Provide environment variables

Here's the basic command:

```bash
docker run -d \
  --name nevron \
  -v $(pwd)/logs:/nevron/logs \
  --env-file .env \
  nevron:latest
```

#### Important Notes:

##### Logs Volume

- The container creates a `/nevron/logs` directory
- You should mount this directory to persist logs
- Example: `-v $(pwd)/logs:/nevron/logs`

##### Environment Variables

- The container requires a properly configured `.env` file
- You can copy `.env.dev` as a template: `cp .env.dev .env`
- Make sure to set all required API keys and configurations
- Pass the env file using `--env-file .env`

##### Container Management

```bash
# Stop the container
docker stop nevron

# Start the container
docker start nevron

# View logs
docker logs -f nevron
```

## Cloud Deployment Options

You can deploy the Nevron Docker container to various cloud platforms:

### AWS

1. Push the image to Amazon ECR
2. Deploy using:
   - ECS (Elastic Container Service)
   - EKS (Elastic Kubernetes Service)
   - EC2 with Docker installed

### Google Cloud

1. Push the image to Google Container Registry
2. Deploy using:
   - Google Kubernetes Engine (GKE)
   - Cloud Run
   - Compute Engine with Docker installed

### Azure

1. Push the image to Azure Container Registry
2. Deploy using:
   - Azure Kubernetes Service (AKS)
   - Azure Container Instances
   - VM with Docker installed

### Digital Ocean

1. Push the image to Digital Ocean Container Registry
2. Deploy using:
   - Digital Ocean Kubernetes
   - Droplet with Docker installed

## Best Practices

##### Security

- Never include sensitive data in the Docker image
- Use environment variables for all sensitive information
- Follow the [Security Policy](../SECURITY.md) guidelines

##### Monitoring

- Mount the logs directory to persist logs
- Consider implementing container monitoring
- Set up alerts for container health

##### Updates

- Use specific version tags for production deployments
- Implement a strategy for updating the container
- Keep base images updated for security patches

##### Resource Management

- Monitor container resource usage
- Set appropriate resource limits
- Scale based on your needs 