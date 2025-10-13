pipeline {
    agent any
    
    // 🔧 AJOUTEZ CETTE SECTION
    tools {
        maven 'Maven'  // ⚠️ Le nom doit être exactement 'Maven'
    }
    
    environment {
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
                sh 'mvn clean install'
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh 'mvn sonar:sonar -Dsonar.login=$SONAR_TOKEN'
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
    }
    
    post {
        always {
            echo 'Pipeline terminé !'
        }
        success {
            echo '✅ Build et analyse SonarQube réussis !'
        }
        failure {
            echo '❌ Build ou analyse échouée !'
        }
    }
}
