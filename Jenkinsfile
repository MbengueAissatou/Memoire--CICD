pipeline {
    agent any

    environment {
        DJANGO_SETTINGS_MODULE = 'rsa_project.settings'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Create Virtual Env') {
            steps {
                sh 'python3 -m venv venv'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    venv/bin/pip install -r requirements.txt
                    venv/bin/pip install pytest pytest-django
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh 'venv/bin/python -m pytest rsa_app/tests -v'
            }
        }
        
        
    }
}