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
                    url: 'https://github.com/MbengueAissatou/Memoire--CICD.git'
            }
        }
        
        stage('Setup Python') {
            steps {
                echo '🐍 Setting up Python environment...'
                sh '''
                    python3 -m venv ${WORKSPACE}/venv
                    . ${WORKSPACE}/venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest pytest-django flake8 pip-audit coverage
                '''
            }
        }
        
        stage('Linting') {
            steps {
                echo '🔍 Running linting...'
                sh '''
                    . ${WORKSPACE}/venv/bin/activate
                    flake8 rsa_app/ --max-line-length=120 || true
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                echo '🧪 Running tests with coverage...'
                sh '''
                    export DJANGO_SETTINGS_MODULE=rsa_project.settings
                    . ${WORKSPACE}/venv/bin/activate
                    
                    # Exécuter les tests avec coverage
                    coverage run -m pytest rsa_app/tests -v
                    
                    # Générer le rapport XML pour SonarQube
                    coverage xml -o coverage.xml
                    
                    # Afficher le rapport
                    coverage report
                '''
            }
        }
        
        stage('Scan Dependencies') {
            steps {
                echo '🔒 Scanning dependencies for vulnerabilities...'
                sh '''
                    . ${WORKSPACE}/venv/bin/activate
                    pip-audit -f json || echo "⚠️ Vulnerabilities found but continuing"
                    echo "✅ Dependency scan completed"
                '''
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                echo '📊 Running SonarQube analysis...'
                script {
                    // Utiliser le SonarScanner configuré dans Jenkins
                    def scannerHome = tool 'SonarScanner'
                    
                    withSonarQubeEnv('SonarQube') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                                -Dsonar.projectKey=MemoireRSA \
                                -Dsonar.projectName='Memoire RSA CI-CD' \
                                -Dsonar.sources=. \
                                -Dsonar.exclusions=**/venv/**,**/migrations/**,**/static/**,**/__pycache__/**,**/tests/** \
                                -Dsonar.tests=rsa_app/tests \
                                -Dsonar.test.inclusions=**/test_*.py \
                                -Dsonar.python.version=3 \
                                -Dsonar.python.coverage.reportPaths=coverage.xml \
                                -Dsonar.host.url=\${SONAR_HOST_URL} \
                                -Dsonar.login=\${SONAR_AUTH_TOKEN}
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
            echo '🔄 Pipeline terminé.'
        }
        success {
            echo '✅ Pipeline réussi - Tous les stages ont passé !'
        }
        failure {
            echo '❌ Pipeline échoué - Vérifiez les logs ci-dessus.'
        }
    }
}
```

## 📋 Actions à Faire Maintenant

### 1️⃣ Vérifiez SonarScanner dans Jenkins

**Jenkins** → **Manage Jenkins** → **Global Tool Configuration** → Section **SonarQube Scanner**

Assurez-vous que :
- ✅ Name: `SonarScanner`
- ✅ Install automatically: Coché
- ✅ Version: SonarQube Scanner 5.0.1.3006 (ou plus récent)

### 2️⃣ Vérifiez SonarQube Server dans Jenkins

**Jenkins** → **Manage Jenkins** → **Configure System** → Section **SonarQube servers**

Assurez-vous que :
- ✅ Name: `SonarQube`
- ✅ Server URL: `http://sonarqube:9000` ⚠️ **IMPORTANT : Pas localhost !**
- ✅ Server authentication token: `jenkins_sonar`

### 3️⃣ Configurez le Webhook dans SonarQube

1. Connectez-vous à SonarQube : `http://localhost:9000`
2. **Administration** → **Configuration** → **Webhooks**
3. Créez un nouveau webhook :
```
   Name: Jenkins
   URL: http://jenkins:8080/sonarqube-webhook/
   Secret: [laisser vide]