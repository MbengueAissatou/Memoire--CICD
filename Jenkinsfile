pipeline {
    agent any

    environment {
        // ID du credential Jenkins contenant ton token SonarQube
        SONAR_TOKEN = credentials('sonar-token') 
    }

    stages {
        stage('Checkout') {
            steps {
                // Récupération du code depuis GitHub avec credential
                git branch: 'master', 
                    url: 'https://github.com/MbengueAissatou/Memoire--CICD.git', 
                    credentialsId: 'github-jenkins'
            }
        }

        stage('Build') {
            steps {
                // Compilation du projet Maven
                sh 'mvn clean install'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                // Exécute l'analyse SonarQube
                withSonarQubeEnv('SonarQube') { // Nom de ton SonarQube server dans Jenkins
                    sh 'mvn sonar:sonar -Dsonar.login=$SONAR_TOKEN'
                }
            }
        }

        stage('Quality Gate') {
            steps {
                // Vérifie que l'analyse respecte le Quality Gate SonarQube
                timeout(time: 1, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline terminé !'
        }
        success {
            echo 'Build et analyse SonarQube réussis ✅'
        }
        failure {
            echo 'Build ou analyse échouée ❌'
        }
    }
}
