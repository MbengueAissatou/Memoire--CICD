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
                    venv/bin/pip install --upgrade pip
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

        stage('Scan Secrets') {
            steps {
                sh 'trufflehog filesystem . --only-verified --no-update || true'
            }
        }

        stage('Scan Dependencies') {
            steps {
                sh 'venv/bin/pip-audit -r requirements.txt || true'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    script {
                        def scannerHome = tool 'SonarScanner'
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                    docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest
                '''
            }
        }

        stage('Scan Trivy') {
            steps {
                sh '''
                    trivy image \
                        --exit-code 1 \
                        --severity CRITICAL \
                        --format table \
                        ${DOCKER_IMAGE}:${DOCKER_TAG} || true
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                        docker push ${DOCKER_IMAGE}:latest
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                    kubectl apply -f k8s/networkpolicy.yaml
                    kubectl rollout status deployment/rsa-app --timeout=300s
                '''
            }
        }

        stage('Deploy Monitoring') {
            steps {
                sh '''
                    # Prometheus
                    kubectl apply -f k8s/prometheus-deployment.yaml
                    kubectl apply -f k8s/service-prometheus.yaml

                    # Grafana
                    kubectl apply -f k8s/grafana-deployment.yaml
                    kubectl apply -f k8s/service-grafana.yaml
                '''
            }
        }

    }

    post {
        success {
            echo '✅ Pipeline DevSecOps + Monitoring terminé avec succès !'
        }
        failure {
            echo '❌ Pipeline échoué - vérifiez les logs et la sécurité.'
        }
        always {
            echo '🔄 Pipeline terminé.'
        }
    }
}