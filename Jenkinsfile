pipeline {
    agent any

    environment {
        DJANGO_SETTINGS_MODULE = 'rsa_project.settings'
        VENV_DIR = "${WORKSPACE}/venv"
        DOCKER_IMAGE = 'astou233/rsa-app'
        DOCKER_TAG = "${BUILD_NUMBER}"
        SONARQUBE = 'SonarQube'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: 'https://github.com/MbengueAissatou/Memoire--CICD.git'
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                    python3 -m venv $VENV_DIR
                    . $VENV_DIR/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest pytest-django flake8 pip-audit
                '''
            }
        }

        stage('Linting') {
            steps {
                sh '''
                    . $VENV_DIR/bin/activate
                    flake8 rsa_app/ --max-line-length=120
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
                    . $VENV_DIR/bin/activate
                    pytest rsa_app/tests -v
                '''
            }
        }

        stage('Scan Dependencies') {
            steps {
                sh '''
                    . $VENV_DIR/bin/activate
                    pip-audit --json > pip_audit_report.json
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv(SONARQUBE) {
                    sh '''
                        . $VENV_DIR/bin/activate
                        sonar-scanner \
                            -Dsonar.projectKey=MemoireRSA \
                            -Dsonar.sources=. \
                            -Dsonar.python.coverage.reportPaths=coverage.xml
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE:$DOCKER_TAG .'
            }
        }

        stage('Scan Docker Image') {
            steps {
                sh 'trivy image --severity HIGH,CRITICAL $DOCKER_IMAGE:$DOCKER_TAG'
            }
        }

        stage('Push Docker Image') {
            steps {
                sh '''
                    docker login -u $DOCKER_USER -p $DOCKER_PASSWORD
                    docker push $DOCKER_IMAGE:$DOCKER_TAG
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f k8s/'
            }
        }
    }

    post {
        always {
            echo '🔄 Pipeline terminé.'
        }
        success {
            echo '✅ Pipeline réussi !'
        }
        failure {
            echo '❌ Pipeline échoué - vérifie les logs.'
        }
    }
}