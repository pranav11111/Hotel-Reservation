pipeline{

    agent any

    environment{
        
        VENV_DIR = 'venv'
        GCP_PROJECT = 'turing-alcove-454906-a1'
        GCLOUD_PATH = 'var/jenkins_home/google-cloud-sdk/bin'

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

        stage('Building and pushing docker image to GCR'){
            steps{
                withCredentials([file(credentialsId: 'GCP-Key', variable: 'GOOGLE_APP_CRED')]){
                    script{
                        echo 'Building and pushing docker image to GCR'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}

                        gcloud auth activate-service-account --key-file=${GOOGLE_APP_CRED}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud auth configure-docker --quiet

                        docker build -t gcr.io/{GCP_PROJECT}/Hotel-Reservation:latest .

                        docker push gcr.io/{GCP_PROJECT}/Hotel-Reservation:latest 

                        '''
                    }

                }

            }

        }
    }
}