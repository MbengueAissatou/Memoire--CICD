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

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    venv/bin/pip install -r requirements.txt
                    venv/bin/pip install pytest pytest-django flake8
                '''
            }
        }

        stage('Linting') {
    steps {
        sh 'venv/bin/flake8 rsa_app/ --max-line-length=120 --exit-zero'
    }
}
        stage('Run Tests') {
            steps {
                sh 'venv/bin/python -m pytest rsa_app/tests -v'
            }
        }

        // ✅ Étape SonarQube
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {  // ← nom défini à l'étape 5
                    sh 'sonar-scanner'
                }
            }
        }

        // ✅ Attendre le Quality Gate
        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }
}