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
                    venv/bin/pip install pytest pytest-django flake8 safety
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

        // 🔐 SÉCURITÉ 1 : Détection de secrets
        stage('Scan Secrets') {
            steps {
                sh 'trufflehog filesystem . --only-verified'
            }
        }

        // 🔐 SÉCURITÉ 2 : Dépendances vulnérables
        stage('Scan Dependencies') {
            steps {
                sh 'venv/bin/safety scan -r requirements.txt'
            }
        }

        // 🔐 SÉCURITÉ 3 : Qualité et vulnérabilités du code
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

        // 🔐 SÉCURITÉ 4 : Scan image Docker
        stage('Scan Trivy') {
            steps {
                sh '''
                    trivy image \
                        --exit-code 1 \
                        --severity CRITICAL \
                        --format table \
                        ${DOCKER_IMAGE}:${DOCKER_TAG}
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
                        echo $DOCKER_PASS | docker login \
                            -u $DOCKER_USER --password-stdin
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
                    kubectl rollout status deployment/rsa-app --timeout=60s
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline DevSecOps terminé avec succès !'
        }
        failure {
            echo '❌ Pipeline échoué - vérifiez les logs de sécurité.'
        }
        always {
            echo '🔄 Pipeline terminé.'
        }
    }
}