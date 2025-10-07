pipeline {
    agent any

    environment {
        // 🔐 Ton token SonarQube stocké dans Jenkins Credentials (type : Secret Text)
        SONAR_TOKEN = credentials('jenkins_sonar')
    }

    stages {

        stage('Checkout') {
            steps {
                echo "📦 Clonage du dépôt GitHub..."
                git branch: 'master',
                    url: 'https://github.com/MbengueAissatou/Memoire--CICD.git',
                    credentialsId: 'github-jenkins'
            }
        }

        stage('Build') {
            steps {
                echo "⚙️ Construction du projet Maven..."
                bat 'mvn clean install'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                echo "🔍 Lancement de l’analyse SonarQube..."
                withSonarQubeEnv('SonarQube') { // ⚠️ Nom exact de ton serveur configuré dans Jenkins
                    bat """
                    mvn sonar:sonar ^
                        -Dsonar.projectKey=Memoire-CICD ^
                        -Dsonar.host.url=%SONARQUBE_URL% ^
                        -Dsonar.login=${env.SONAR_TOKEN}
                    """
                }
            }
        }

        stage('Quality Gate') {
            steps {
                echo "🚦 Vérification du Quality Gate SonarQube..."
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }

    post {
        always {
            echo "🔚 Fin du pipeline (état : ${currentBuild.currentResult})"
        }
        success {
            echo "✅ Build et analyse SonarQube réussis !"
        }
        failure {
            echo "❌ Build ou analyse échouée ! Vérifie la console Jenkins pour plus de détails."
        }
    }
}
