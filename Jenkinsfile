pipeline{

    agent any

    stages{

        stage('Cloning repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning repo to Jenkins .....'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/pranav11111/Hotel-Reservation.git']])

                }

            }

        }
    }
}