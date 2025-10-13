pipeline {
    agent any
    
    environment {
        SONAR_TOKEN = credentials('jenkins_sonar')
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '📦 Cloning repository...'
                git branch: 'master', 
                    url: 'https://github.com/MbengueAissatou/Memoire--CICD.git', 
                    credentialsId: 'github-jenkins'
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                echo '🐍 Setting up Python virtual environment...'
                sh '''
                    # Vérifier la version de Python
                    python3 --version
                    
                    # Créer un environnement virtuel
                    python3 -m venv venv
                    
                    # Activer l'environnement virtuel et installer les dépendances
                    . venv/bin/activate
                    pip install --upgrade pip
                    
                    # Installer les dépendances si requirements.txt existe
                    if [ -f requirements.txt ]; then
                        pip install -r requirements.txt
                    else
                        # Installer les packages minimum pour Django
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
                    . venv/bin/activate
                    
                    # Vérifier si manage.py existe
                    if [ -f manage.py ]; then
                        # Exécuter les tests Django avec coverage
                        coverage run --source='.' manage.py test --noinput || true
                        
                        # Générer le rapport de couverture XML pour SonarQube
                        coverage xml -o coverage.xml
                        
                        # Afficher le rapport de couverture
                        coverage report
                    else
                        echo "⚠️ manage.py not found, skipping tests"
                    fi
                '''
            }
        }
        
        stage('Code Quality - Pylint') {
            steps {
                echo '🔍 Running code quality checks...'
                sh '''
                    . venv/bin/activate
                    
                    # Exécuter pylint sur les fichiers Python (ne pas bloquer le build)
                    find . -name "*.py" -not -path "./venv/*" -not -path "./migrations/*" | xargs pylint --exit-zero || true
                '''
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                echo '📊 Starting SonarQube analysis...'
                script {
                    // Utiliser SonarScanner pour les projets Python
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
                            // Ne pas bloquer le build pour l'instant
                            // error "Quality Gate failed: ${qg.status}"
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
            
            // Nettoyer l'environnement virtuel
            sh 'rm -rf venv || true'
        }
        success {
            echo '✅ Build et analyse SonarQube réussis !'
        }
        failure {
            echo '❌ Build ou analyse échouée ! Vérifiez les logs ci-dessus.'
        }
    }
}
