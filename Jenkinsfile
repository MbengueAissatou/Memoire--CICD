// ====================================
// PIPELINE CORRIGÉ - Maven Configuré
// ====================================

pipeline {
    agent any
    
    // 🔧 AJOUT IMPORTANT: Déclarer Maven comme outil
    tools {
        maven 'Maven'  // Le nom doit correspondre à celui configuré dans Jenkins
    }
    
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
        
        stage('Build') {
            steps {
                echo '🔨 Building project with Maven...'
                sh 'mvn clean install -DskipTests'
            }
        }
        
        stage('Test') {
            steps {
                echo '🧪 Running tests...'
                sh 'mvn test'
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                echo '📊 Starting SonarQube analysis...'
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        mvn sonar:sonar \
                            -Dsonar.projectKey=memoire-cicd \
                            -Dsonar.projectName="Memoire CI-CD" \
                            -Dsonar.login=${SONAR_TOKEN}
                    '''
                }
            }
        }
        
        stage('Quality Gate') {
            steps {
                echo '⏳ Waiting for Quality Gate...'
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
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
            echo '❌ Build ou analyse échouée !'
        }
    }
}

// ====================================
// ÉTAPES DE CONFIGURATION MAVEN
// ====================================
/*

📋 ÉTAPE 1: Configurer Maven dans Jenkins

1. Aller dans Jenkins → Manage Jenkins → Global Tool Configuration

2. Chercher la section "Maven"

3. Cliquer sur "Add Maven"

4. Configurer:
   - Name: Maven (⚠️ Ce nom doit correspondre à tools { maven 'Maven' })
   - Install automatically: ✅ COCHÉ
   - Version: Choisir la dernière version (ex: 3.9.6)

5. Cliquer sur "Save"

6. Redémarrer Jenkins (optionnel mais recommandé):
   docker restart jenkins
   # ou
   systemctl restart jenkins

*/

// ====================================
// ALTERNATIVE: Maven via Docker
// ====================================
/*

Si vous utilisez Jenkins dans Docker, utilisez ce pipeline:

pipeline {
    agent {
        docker {
            image 'maven:3.9.6-eclipse-temurin-17'
            args '-v /root/.m2:/root/.m2'
        }
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
                sh 'mvn clean install -DskipTests'
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh 'mvn sonar:sonar -Dsonar.login=${SONAR_TOKEN}'
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
}

*/

// ====================================
// VÉRIFICATION MAVEN
// ====================================
/*

Pour vérifier que Maven est bien configuré, créez un pipeline de test:

pipeline {
    agent any
    
    tools {
        maven 'Maven'
    }
    
    stages {
        stage('Check Maven') {
            steps {
                sh '''
                    echo "=== Maven Version ==="
                    mvn --version
                    echo ""
                    echo "=== Java Version ==="
                    java -version
                '''
            }
        }
    }
}

Si cette commande fonctionne, Maven est bien configuré!

*/
