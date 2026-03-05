pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "rsa_project:latest"
        SONARQUBE_SERVER = "SonarQube"
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/MbengueAissatou/Memoire--CICD.git', branch: 'master'
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest pytest-django flake8 pip-audit
                '''
            }
        }

        stage('Linting') {
            steps {
                sh '. venv/bin/activate && flake8 rsa_app/ --max-line-length=120'
            }
        }

        stage('Run Tests') {
            steps {
                sh '. venv/bin/activate && pytest rsa_app/tests -v'
            }
        }

        stage('Scan Secrets') {
            steps {
                sh 'trufflehog filesystem . --only-verified --no-update'
            }
        }

        stage('Scan Dependencies') {
            steps {
                sh '. venv/bin/activate && pip-audit -r requirements.txt --progress bar'
            }
        }

        stage('SonarQube Analysis') {
            environment {
                scannerHome = tool name: 'SonarScanner', type: 'hudson.plugins.sonar.SonarRunnerInstallation'
            }
            steps {
                withSonarQubeEnv("${SONARQUBE_SERVER}") {
                    sh "${scannerHome}/bin/sonar-scanner"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE} ."
            }
        }

        stage('Scan Docker Image') {
            steps {
                sh "trivy image ${DOCKER_IMAGE}"
            }
        }

        stage('Push Docker Image') {
            steps {
                sh "docker tag ${DOCKER_IMAGE} myregistry/${DOCKER_IMAGE}"
                sh "docker push myregistry/${DOCKER_IMAGE}"
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh "kubectl apply -f k8s/"
            }
        }
    }

    post {
        always {
            echo "🔄 Pipeline terminé."
        }
        success {
            echo "✅ Pipeline réussi !"
        }
        failure {
            echo "❌ Pipeline échoué - vérifie les logs de sécurité."
        }
    }
}