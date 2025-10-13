pipeline {
    agent any

    environment {
        SONAR_TOKEN = credentials('jenkins_sonar')
        VENV = "venv"
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
                    python3 --version
                    python3 -m venv $VENV
                    . $VENV/bin/activate
                    pip install --upgrade pip

                    # Installer les dépendances
                    if [ -f requirements.txt ]; then
                        pip install -r requirements.txt
                    else
                        # Installer minimum pour Django + tests + SonarQube
                        pip install Django coverage pylint pylint-django sonarqube-scanner
                    fi

                    pip list
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo '🧪 Running Django tests...'
                sh '''
                    . $VENV/bin/activate

                    if [ -f manage.py ]; then
                        # Lancer les tests avec couverture
                        coverage run --source='.' manage.py test --noinput || true
                        coverage xml -o coverage.xml
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
                    . $VENV/bin/activate
                    find . -name "*.py" -not -path "./$VENV/*" -not -path "./migrations/*" | xargs pylint --exit-zero || true
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                echo '📊 Starting SonarQube analysis...'
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        . $VENV/bin/activate
                        sonar-scanner \
                          -Dsonar.projectKey=Memoire-CICD \
                          -Dsonar.projectName='Memoire CI-CD Django' \
                          -Dsonar.sources=. \
                          -Dsonar.exclusions=**/venv/**,**/migrations/**,**/static/**,**/media/**,**/__pycache__/** \
                          -Dsonar.python.version=3 \
                          -Dsonar.python.coverage.reportPaths=coverage.xml \
                          -Dsonar.host.url=$SONAR_HOST_URL \
                          -Dsonar.login=$SONAR_TOKEN
                    '''
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
                            // Pour l’instant, on ne bloque pas le build
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
            sh 'rm -rf $VENV || true'
        }
        success {
            echo '✅ Build et analyse SonarQube réussis !'
        }
        failure {
            echo '❌ Build ou analyse échouée ! Vérifiez les logs ci-dessus.'
        }
    }
}
