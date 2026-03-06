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
                    coverage run -m pytest rsa_app/tests -v
                    coverage xml -o coverage.xml
                    coverage report
                '''
            }
        }
        
        stage('Scan Dependencies') {
            steps {
                echo '🔒 Scanning dependencies...'
                sh '''
                    . ${WORKSPACE}/venv/bin/activate
                    pip-audit -f json || echo "⚠️ Vulnerabilities found"
                    echo "✅ Scan completed"
                '''
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                echo '📊 Running SonarQube analysis...'
                script {
                    def scannerHome = tool 'SonarScanner'
                    withSonarQubeEnv('SonarQube') {
                        sh """
                            ${