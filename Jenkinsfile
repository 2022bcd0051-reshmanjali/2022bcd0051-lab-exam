pipeline {
    agent any

    stages {

        stage('Build Image') {
            steps {
                sh 'docker build -t 2022bcd0051-model .'
            }
        }

        stage('Run Training Container') {
            steps {
                sh '''
                docker run --name ml-container 2022bcd0051-model
                '''
            }
        }

        stage('Check Output Files') {
            steps {
                script {
                    def files = sh(
                        script: 'docker cp ml-container:/app/output ./output || true && ls output',
                        returnStdout: true
                    ).trim()

                    echo "Output Files: ${files}"

                    if (!files.contains("model.pkl") || !files.contains("results.json")) {
                        error("Output files missing ")
                    }
                }
            }
        }

        stage('Stop & Remove Container') {
            steps {
                sh '''
                docker stop ml-container || true
                docker rm ml-container || true
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline Passed "
        }
        failure {
            echo "Pipeline Failed "
        }
    }
}