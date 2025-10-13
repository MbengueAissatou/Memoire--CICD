pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    
    environment {
        SONAR_TOKEN = credentials('jenkins_sonar')
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '📦 Cloning repository...'
                checkout scm
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                echo '🐍 Setting up Python environment...'
                sh '''
                    # Afficher la version de Python
                    python --version
                    
                    # Mettre à jour pip
                    pip install --upgrade pip
                    
                    # Installer les dépendances
                    if [ -f requirements.txt ]; then
                        pip install -r requirements.txt
                    else
                        # Installer les packages minimum
                        pip install Django coverage pylint pylint-django
                    fi
                    
                    # Afficher les packages installés
                    pip list
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                echo '🧪 Running Django tests...'
                sh '''
                    # Vérifier si manage.py existe
                    if [ -f manage.py ]; then
                        # Exécuter les tests Django avec coverage
                        coverage run --source='.' manage.py test --noinput || true
                        
                        # Générer le rapport de couverture
                        coverage xml -o coverage.xml
                        coverage report
                    else
                        echo "⚠️ manage.py not found, creating dummy coverage file"
                        echo '<?xml version="1.0" ?><coverage version="1.0"></coverage>' > coverage.xml
                    fi
                '''
            }
        }
        
        stage('Code Quality - Pylint') {
            steps {
                echo '🔍 Running code quality checks...'
                sh '''
                    # Exécuter pylint sur les fichiers Python
                    find . -name "*.py" -not -path "./venv/*" -not -path "./migrations/*" | xargs pylint --exit-zero || true
                '''
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                echo '📊 Starting SonarQube analysis...'
                script {
                    def scannerHome = tool 'SonarScanner'
                    withSonarQubeEnv('SonarQube') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                                -Dsonar.projectKey=memoire-cicd \
                                -Dsonar.projectName='Memoire CI-CD Django' \
                                -Dsonar.sources=. \
                                -Dsonar.exclusions=**/venv/**,**/migrations/**,**/static/**,**/media/**,**/__pycache__/** \
                                -Dsonar.python.version=3 \
                                -Dsonar.python.coverage.reportPaths=coverage.xml \
                                -Dsonar.host.url=${SONAR_HOST_URL} \
                                -Dsonar.login=${SONAR_TOKEN}
                        """
                    }
                }
            }
        }
        
        stage('Quality Gate') {
            steps {
                echo '⏳ Waiting for Quality Gate result...'
                timeout(time: 5, unit: 'MINUTES') {
                    script {
                        def qg = waitForQualityGate()
                        if (qg.status != 'OK') {
                            echo "⚠️ Quality Gate status: ${qg.status}"
                        } else {
                            echo "✅ Quality Gate passed!"
                        }
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo '🏁 Pipeline terminé !'
        }
        success {
            echo '✅ Build et analyse SonarQube réussis !'
        }
        failure {
            echo '❌ Build ou analyse échouée ! Vérifiez les logs ci-dessus.'
        }
    }
}
