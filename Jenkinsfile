pipeline {
    agent any

    environment {
        DJANGO_SETTINGS_MODULE = 'rsa_project.settings'
        DOCKER_IMAGE = 'astou233/rsa-app'
        DOCKER_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                venv/bin/pip install -r requirements.txt
                venv/bin/pip install pytest pytest-django flake8 pip-audit
                '''
            }
        }

        stage('Linting') {
            steps {
                sh 'venv/bin/flake8 rsa_app/ --max-line-length=120'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'venv/bin/python -m pytest rsa_app/tests -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t $DOCKER_IMAGE:$DOCKER_TAG .
                docker tag $DOCKER_IMAGE:$DOCKER_TAG $DOCKER_IMAGE:latest
                '''
            }
        }

    }

    post {
        success {
            echo 'Pipeline réussi'
        }
        failure {
            echo 'Pipeline échoué'
        }
    }
}