pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                git branch: 'main', url: 'https://github.com/islam-kamel/ArabClubDeploy.git'
                bat 'python -m venv env'
                bat 'env/Scripts/activate'
                bat 'pip install -r requirements.txt'
                bat 'python manage.py makemigrations'
                bat 'python manage.py migrate'

            }
        }
        stage('Testing') {
            steps {
                bat 'git fetch https://github.com/islam-kamel/ArabClub.git'
                bat 'coverage  run --omit="*/env/*" manage.py test'
                bat 'coverage html'
                bat 'coverage xml -o reports/coverage.xml'
            }
            post{
                always{
                    step([$class: 'CoberturaPublisher',
                                   autoUpdateHealth: false,
                                   autoUpdateStability: false,
                                   coberturaReportFile: 'reports/coverage.xml',
                                   failNoReports: false,
                                   failUnhealthy: false,
                                   failUnstable: false,
                                   maxNumberOfBuilds: 10,
                                   onlyStable: false,
                                   sourceEncoding: 'ASCII',
                                   zoomCoverageChart: false])
                }
            }
        }
        stage('Deploy') {
            steps {
//                 bat 'git remote remove origin'
//                 bat 'git remote add origin https://github.com/islam-kamel/ArabClubDeploy.git'
//                 bat 'git remote set-url origin https://github.com/islam-kamel/ArabClubDeploy.git'
//                 bat 'git fetch origin main'
//                 bat 'git commit -m "Jenkins Automate build-id: %BUILD_NUMBER% :rocket:"'
                bat 'git push origin main'
            }

        }

    }
    post {
        always {
            publishHTML([allowMissing: false, alwaysLinkToLastBuild: true, keepAll: true, reportDir: 'htmlcov', reportFiles: 'index.html', reportName: 'HTML Report', reportTitles: 'Coverage Report'])
        }
    }
}
