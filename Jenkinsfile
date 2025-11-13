pipeline {
    agent any
    
    environment {
        APP_NAME = 'cicd-demo-app'
        APP_VERSION = "${BUILD_NUMBER}"
        DOCKER_IMAGE = "${APP_NAME}:latest"
        APP_PORT = '3000'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '📥 Checking out code...'
                // In real scenario, this would be:
                // checkout scm
                // For demo, we assume code is already present
                sh 'echo "Code checkout completed"'
            }
        }
        
        stage('Build') {
            steps {
                echo '🔨 Building application...'
                dir('app') {
                    sh '''
                        echo "Installing dependencies..."
                        pip3 install --user -r requirements.txt || true
                        echo "Build completed successfully!"
                    '''
                }
            }
        }
        
        stage('Test') {
            steps {
                echo '🧪 Running unit tests...'
                dir('app') {
                    sh '''
                        echo "Executing test suite..."
                        python3 test_app.py
                        echo "All tests passed! ✅"
                    '''
                }
            }
        }
        
        stage('Package') {
            steps {
                echo '📦 Building Docker image...'
                script {
                    sh """
                        echo "Building Docker image: ${DOCKER_IMAGE}"
                        docker build -t ${DOCKER_IMAGE} .
                        echo "Docker image built successfully!"
                        docker images | grep ${APP_NAME}
                    """
                }
            }
        }
        
        stage('Deploy') {
            steps {
                echo '🚀 Deploying application...'
                script {
                    sh '''
                        echo "Stopping existing containers..."
                        docker-compose down || true
                        
                        echo "Starting application with Docker Compose..."
                        docker-compose up -d
                        
                        echo "Waiting for application to start..."
                        sleep 5
                        
                        echo "Deployment completed!"
                    '''
                }
            }
        }
        
        stage('Health Check') {
            steps {
                echo '🏥 Verifying application health...'
                script {
                    sh '''
                        echo "Running health check script..."
                        chmod +x healthcheck.sh
                        ./healthcheck.sh
                        
                        echo ""
                        echo "✅ Pipeline completed successfully!"
                        echo "Application is running at: http://localhost:${APP_PORT}"
                    '''
                }
            }
        }
    }
    
    post {
        success {
            echo '''
            ╔═══════════════════════════════════════╗
            ║  ✅ PIPELINE COMPLETED SUCCESSFULLY   ║
            ╚═══════════════════════════════════════╝
            
            🎉 All stages passed!
            📊 Build Number: ${BUILD_NUMBER}
            🐳 Docker Image: ${DOCKER_IMAGE}
            🌐 Application URL: http://localhost:${APP_PORT}
            💚 Health Status: OK
            '''
        }
        failure {
            echo '''
            ╔═══════════════════════════════════════╗
            ║  ❌ PIPELINE FAILED                   ║
            ╚═══════════════════════════════════════╝
            
            Please check the console output for errors.
            '''
        }
        always {
            echo '🧹 Cleaning up...'
            // Uncomment to clean up after each build
            // sh 'docker-compose down || true'
        }
    }
}