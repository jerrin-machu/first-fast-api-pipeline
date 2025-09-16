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
        sshagent(['deploy-key']) { // <-- use the credentials ID
            sh '''
                ssh -o StrictHostKeyChecking=no jerrin@192.168.50.187 '
                    mkdir -p /srv/my-fastapi-app &&
                    cd /srv/my-fastapi-app &&
                    echo "IMAGE=docker.io/jerrinmachu/fastapi-app:latest" > .env &&
                    docker compose -f docker-compose.prod.yml pull web &&
                    docker compose -f docker-compose.prod.yml up -d --remove-orphans
                '
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
