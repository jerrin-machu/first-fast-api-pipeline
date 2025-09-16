pipeline {
  agent any

  environment {
    REGISTRY = 'docker.io'
    REGISTRY_NAMESPACE = 'jerrinmachu'
    APP_NAME = 'fastapi-app'
    PROD_SSH_HOST = '192.168.50.187'
    PROD_SSH_USER = 'jerrin'
    PROD_APP_DIR = '/srv/my-fastapi-app'
    IMAGE_TAG = "latest"
    IMAGE = "${REGISTRY}/${REGISTRY_NAMESPACE}/${APP_NAME}:${IMAGE_TAG}"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build & Push Docker Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh '''
            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin $REGISTRY
            docker build -t $IMAGE .
            docker push $IMAGE
          '''
        }
      }
    }

    stage('Deploy to Production') {
      steps {
        // Jenkins SSH credentials with ID 'prod-ssh-key' should correspond to user 'jerrin' on 192.168.50.187
        sshagent(credentials: ['prod-ssh-key']) {
          sh '''
            ssh -o StrictHostKeyChecking=no ${PROD_SSH_USER}@${PROD_SSH_HOST} "
              mkdir -p ${PROD_APP_DIR} &&
              cd ${PROD_APP_DIR} &&
              git init . &&
              git remote add origin https://github.com/your/repo.git || true &&
              git fetch --all &&
              git reset --hard origin/main &&
              echo 'IMAGE=${IMAGE}' > .env &&
              docker compose -f docker-compose.prod.yml pull web &&
              docker compose -f docker-compose.prod.yml up -d --remove-orphans
            "
          '''
        }
      }
    }
  }

  post {
    success {
      echo "✅ Deployed successfully to ${PROD_SSH_HOST}"
    }
    failure {
      echo "❌ Deployment failed. Check logs."
    }
  }
}
