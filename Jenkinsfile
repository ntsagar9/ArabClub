pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/islam-kamel/ArabClub.git'
            }
        }
        stage('Create Environment') {
            steps {
                bat 'python -m venv env'
                bat 'env/Scripts/activate'
                bat 'pip install -r requirements.txt'

            }
        }
        stage('Build') {
            steps {
                bat 'python manage.py makemigrations'
                bat 'python manage.py migrate'
                bat 'coverage  run --omit="*/env/*" manage.py test'
                bat 'coverage html'
            }
        }
        stage('Deploy') {
            steps {
                bat 'git remote remove origin'
                bat 'git remote add origin https://github.com/islam-kamel/ArabClubDeploy.git'
                bat 'git remote set-url origin https://github.com/islam-kamel/ArabClubDeploy.git'
                bat 'git add . --force'
                bat 'git commit -m "Jenkins Automate build"'
                bat 'git push origin main --force'
            }

        }

    }
    post {
        always {
            publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'htmlcov', reportFiles: 'index.html', reportName: 'HTML Report', reportTitles: ''])
        }
    }
}
