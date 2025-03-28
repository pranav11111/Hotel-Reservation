pipeline{

    agent any

    environment{
        
        VENV_DIR = 'venv'

    }

    stages{

        stage('Cloning repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning repo to Jenkins .....'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/pranav11111/Hotel-Reservation.git']])

                }

            }

        }

        stage('setting up virtual enviorment and installing dependecies'){
            steps{
                script{
                    echo 'setting up virtual enviorment and installing dependecies'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }

            }

        }
    }
}