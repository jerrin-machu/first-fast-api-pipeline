pipeline {
    agent any

    environment {
        REGISTRY = 'docker.io'
        REGISTRY_NAMESPACE = 'jerrinmachu'
        APP_NAME = 'fastapi-app'
        PROD_SSH_HOST = '192.168.50.187'
        PROD_SSH_USER = 'jerrin'
        PROD_APP_DIR = '/srv/my-fastapi-app'
    }

    stages {
        stage('Build & Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'registry-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin $REGISTRY
                        docker build -t $REGISTRY/$REGISTRY_NAMESPACE/$APP_NAME:latest .
                        docker push $REGISTRY/$REGISTRY_NAMESPACE/$APP_NAME:latest
                    '''
                }
            }
        }

        stage('Generate .env file') {
            steps {
                withCredentials([
                    string(credentialsId: 'POSTGRES_USER_ID', variable: 'POSTGRES_USER'),
                    string(credentialsId: 'POSTGRES_PASSWORD_ID', variable: 'POSTGRES_PASSWORD'),
                    string(credentialsId: 'POSTGRES_DB_ID', variable: 'POSTGRES_DB'),
                    string(credentialsId: 'DB_HOST_ID', variable: 'DB_HOST'),
                    string(credentialsId: 'DB_PORT_ID', variable: 'DB_PORT')
                ]) {
                    sh '''
                        cat > .env <<EOF
POSTGRES_USER=$POSTGRES_USER
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
POSTGRES_DB=$POSTGRES_DB
DB_HOST=$DB_HOST
DB_PORT=$DB_PORT
EOF
                    '''
                }
            }
        }

        stage('Upload docker-compose and env') {
            steps {
                sshagent(['jerrin']) {
                    sh '''
                        scp -o StrictHostKeyChecking=no docker-compose.prod.yml $PROD_SSH_USER@$PROD_SSH_HOST:$PROD_APP_DIR/
                        scp -o StrictHostKeyChecking=no .env $PROD_SSH_USER@$PROD_SSH_HOST:$PROD_APP_DIR/
                    '''
                }
            }
        }

        stage('Deploy to Production') {
            steps {
                sshagent(['jerrin']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no $PROD_SSH_USER@$PROD_SSH_HOST "
                            cd $PROD_APP_DIR &&
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
            echo "✅ Successfully deployed to production"
        }
        failure {
            echo "❌ Deployment failed. Check logs."
        }
    }
}
