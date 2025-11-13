# CI/CD Deployment Pipeline - Complete Setup

## Project Structure
```
cicd-demo-pipeline/
├── Jenkinsfile
├── Dockerfile
├── docker-compose.yml
├── docker-compose-jenkins.yml
├── app/
│   ├── app.py
│   ├── test_app.py
│   └── requirements.txt
├── healthcheck.sh
└── README.md
```

## Quick Start Guide

### Option 1: Run Jenkins in Docker (Recommended)

1. **Start Jenkins with Docker-in-Docker**:
```bash
docker-compose -f docker-compose-jenkins.yml up -d
```

2. **Get Jenkins initial admin password**:
```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

3. **Access Jenkins**:
   - Open: http://localhost:8080
   - Install suggested plugins
   - Create admin user

4. **Configure Jenkins**:
   - Install "Docker Pipeline" plugin (Manage Jenkins → Plugins)
   - Create new Pipeline job
   - Point to your Jenkinsfile in SCM or paste it directly

5. **Run the Pipeline**:
   - Click "Build Now"
   - Watch the stages execute: Build → Test → Package → Deploy → Health Check

### Option 2: Use Existing Jenkins

1. **Prerequisites**:
   - Jenkins installed with Docker and Docker Pipeline plugins
   - Docker and Docker Compose installed on Jenkins host

2. **Create Pipeline Job**:
   - New Item → Pipeline
   - Configure SCM or paste Jenkinsfile
   - Save and Build

## Application Details

### Demo Application
- **Type**: Flask web application
- **Language**: Python 3.9
- **Endpoints**:
  - `GET /` - Returns "Hello World from CI/CD Pipeline!"
  - `GET /health` - Health check endpoint returning status

### Pipeline Stages

1. **Checkout**: Gets code from repository
2. **Build**: Installs dependencies
3. **Test**: Runs unit tests
4. **Package**: Builds Docker image
5. **Deploy**: Deploys using Docker Compose
6. **Health Check**: Verifies application is running

## Health Check

The pipeline verifies the application by:
- Checking container status
- Calling the `/health` endpoint
- Validating HTTP 200 response

## Cleanup

```bash
# Stop and remove containers
docker-compose down

# Stop Jenkins (if using Docker)
docker-compose -f docker-compose-jenkins.yml down

# Remove images
docker rmi cicd-demo-app:latest
```

## Troubleshooting

### Port Already in Use
If port 3000 is occupied:
```bash
# Find process using port
lsof -i :3000

# Or change port in docker-compose.yml
```

### Docker Permission Issues
```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

### Jenkins Cannot Access Docker
Ensure Jenkins container has Docker socket mounted:
```yaml
volumes:
  - /var/run/docker.sock:/var/run/docker.sock
```

## Screenshots Location

After successful pipeline run, capture:
1. Jenkins Blue Ocean view showing all stages green
2. Console output showing health check success
3. Browser showing app running at http://localhost:3000

## Next Steps

- Add integration tests
- Implement staging environment
- Add Slack/email notifications
- Implement rollback strategy
- Add security scanning stage


#!/bin/bash
# Quick Setup Commands for CI/CD Pipeline Demo
# Run these commands in order

echo "=================================="
echo "CI/CD Pipeline Setup Commands"
echo "=================================="

# 1. CREATE PROJECT STRUCTURE
echo -e "\n1️⃣  Creating project structure..."
mkdir -p cicd-demo-pipeline/app
cd cicd-demo-pipeline

# 2. CREATE ALL FILES (Copy the content from artifacts)
echo -e "\n2️⃣  Create these files with content from artifacts:"
echo "   - Jenkinsfile"
echo "   - Dockerfile"
echo "   - docker-compose.yml"
echo "   - docker-compose-jenkins.yml"
echo "   - healthcheck.sh"
echo "   - app/app.py"
echo "   - app/test_app.py"
echo "   - app/requirements.txt"
echo "   - README.md"

# 3. SET PERMISSIONS
echo -e "\n3️⃣  Setting permissions..."
chmod +x healthcheck.sh

# 4. START JENKINS (Option A - With Jenkins)
echo -e "\n4️⃣a Starting Jenkins with Docker-in-Docker..."
docker-compose -f docker-compose-jenkins.yml up -d

# Wait for Jenkins
echo "   Waiting for Jenkins to start (30 seconds)..."
sleep 30

# Get Jenkins password
echo -e "\n5️⃣  Jenkins Initial Password:"
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

echo -e "\n6️⃣  Next Steps:"
echo "   • Open: http://localhost:8080"
echo "   • Use the password above"
echo "   • Install suggested plugins"
echo "   • Create admin user"
echo "   • Install 'Docker Pipeline' plugin"
echo "   • Create new Pipeline job"
echo "   • Configure pipeline with Jenkinsfile"
echo "   • Click 'Build Now'"

# 4. MANUAL TEST (Option B - Without Jenkins)
echo -e "\n4️⃣b OR run manually without Jenkins:"
echo "   docker build -t cicd-demo-app:latest ."
echo "   docker-compose up -d"
echo "   ./healthcheck.sh"

echo -e "\n=================================="
echo "Setup commands prepared!"
echo "=================================="

# ADDITIONAL USEFUL COMMANDS
cat << 'EOF'

📋 USEFUL COMMANDS:

# View Jenkins logs
docker logs -f jenkins

# View app logs
docker logs -f cicd-demo-app

# Stop everything
docker-compose down
docker-compose -f docker-compose-jenkins.yml down

# Restart app only
docker-compose restart

# Rebuild app
docker-compose up -d --build

# Test endpoints
curl http://localhost:3000
curl http://localhost:3000/health
curl http://localhost:3000/info

# View running containers
docker ps

# View all containers
docker ps -a

# Remove everything
docker-compose down
docker-compose -f docker-compose-jenkins.yml down
docker rmi cicd-demo-app:latest jenkins/jenkins:lts
docker volume prune
docker network prune

# Check container health
docker inspect cicd-demo-app | grep -A 10 Health

# Execute health check
./healthcheck.sh

# Follow Jenkins logs in real-time
docker exec -it jenkins tail -f /var/jenkins_home/logs/jenkins.log

EOF# CI-CD-demo-pipeline
# CI-CD-demo-pipeline
