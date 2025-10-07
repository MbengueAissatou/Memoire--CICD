pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo '📦 Clonage du dépôt...'
                git branch: 'master', url: 'https://github.com/MbengueAissatou/Memoire--CICD.git'
            }
        }

        stage('Build') {
            steps {
                echo '🔧 Build du projet...'
                // Ajoute ici les commandes pour construire ton projet, ex : sh 'php artisan migrate' pour Laravel
            }
        }

        stage('Test') {
            steps {
                echo '🧪 Exécution des tests...'
                // Ajoute ici les commandes pour tes tests, ex : sh 'php artisan test'
            }
        }

        stage('Deploy') {
            steps {
                echo '🚀 Déploiement (simulation)...'
            }
        }
    }

    post {
        success {
            echo '✅ Build réussi !'
        }
        failure {
            echo '❌ Build échoué.'
        }
    }
}
