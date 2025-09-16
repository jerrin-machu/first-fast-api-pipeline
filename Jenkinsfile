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
        withCredentials([usernamePassword(credentialsId: 'registry-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
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
        withCredentials([usernamePassword(credentialsId: 'prod-ssh', usernameVariable: 'SSH_USER', passwordVariable: 'SSH_PASS')]) {
          sh '''
            # install sshpass if not already available
            if ! command -v sshpass >/dev/null 2>&1; then
              echo "sshpass not found, installing..."
              sudo apt-get update && sudo apt-get install -y sshpass
            fi

            sshpass -p "$SSH_PASS" ssh -o StrictHostKeyChecking=no $SSH_USER@$PROD_SSH_HOST "
              mkdir -p $PROD_APP_DIR &&
              cd $PROD_APP_DIR &&
              echo 'IMAGE=$IMAGE' > .env &&
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
