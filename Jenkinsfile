pipeline {
    agent any

    triggers {
        pollSCM('H/5 * * * *')
    }

    environment {
        JAVA_HOME = tool name: 'Java 17', type: 'jdk'
        PATH = "${JAVA_HOME}/bin:${env.PATH}:${env.WORKSPACE}/env/bin" // inclut l'env virtuel Python
        DEP_CHECK_HOME = "${env.WORKSPACE}/dependency-check"
        SONAR_HOST_URL = 'http://localhost:9000' // URL de ton serveur SonarQube
        SONAR_LOGIN = credentials('jenkins_sonar') // Token Sonar stocké dans Jenkins
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python Env') {
            steps {
                bat '''
                python -m venv env
                source env/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh """
                    sonar-scanner \
                        -Dsonar.projectKey=scanfield-django \
                        -Dsonar.sources=. \
                        -Dsonar.language=py \
                        -Dsonar.host.url=$SONAR_HOST_URL \
                        -Dsonar.login=$SONAR_LOGIN
                    """
                }
            }
        }

        stage('Setup Dependency-Check') {
            steps {
                sh '''
                wget https://github.com/jeremylong/DependencyCheck/releases/download/v10.0.3/dependency-check-10.0.3-release.zip
                unzip dependency-check-10.0.3-release.zip -d $DEP_CHECK_HOME
                chmod +x $DEP_CHECK_HOME/dependency-check/bin/dependency-check.sh
                '''
            }
        }

        stage('Run Dependency-Check') {
            steps {
                sh '''
                $DEP_CHECK_HOME/dependency-check/bin/dependency-check.sh \
                    --project "scanfield-django" \
                    --scan ./ \
                    --format ALL \
                    --out ./ \
                    --prettyPrint
                mv dependency-check-report.xml dependency-check-report-django.xml || true
                '''
            }
        }

        stage('Install wkhtmltopdf') {
            steps {
                sh 'sudo apt-get update && sudo apt-get install -y wkhtmltopdf'
            }
        }

        stage('Convert Report to PDF') {
            steps {
                sh '''
                if command -v wkhtmltopdf > /dev/null; then
                    echo "➡ Génération du rapport PDF..."
                    wkhtmltopdf dependency-check-report.html rapport-owasp-report-django.pdf
                else
                    echo "⚠ wkhtmltopdf non installé, PDF non généré"
                fi
                '''
            }
        }

        stage('Archive Reports') {
            steps {
                archiveArtifacts artifacts: 'dependency-check-report-django.xml, dependency-check-report.html, rapport-owasp-report-django.pdf', fingerprint: true
            }
        }
    }

    post {
        always {
            echo "✅ Pipeline OWASP Dependency-Check + SonarQube pour Django terminé"
        }
    }
}
