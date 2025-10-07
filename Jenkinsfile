pipeline {
    agent any

    environment {
        // ID du credential Jenkins contenant ton token SonarQube
        SONAR_TOKEN = credentials('jenkins_sonar') 
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', 
                    url: 'https://github.com/MbengueAissatou/Memoire--CICD.git', 
                    credentialsId: 'github-jenkins'
            }
        }

        stage('Build') {
            steps {
                // ✅ Utilisation de 'sh' pour Linux
                sh 'mvn clean install'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    // ✅ Utilisation de 'sh' aussi ici
                    sh 'mvn sonar:sonar -Dsonar.login=$SONAR_TOKEN'
                }
            }
        }

        stage('Quality Gate') {
            steps {
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
            echo '✅ Build et analyse SonarQube réussis !'
        }
        failure {
            echo '❌ Build ou analyse échouée ! Vérifie la console Jenkins pour plus de détails.'
        }
    }
}
