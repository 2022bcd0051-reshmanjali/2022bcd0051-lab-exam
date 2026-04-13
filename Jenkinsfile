pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'reshma1204/2022bcd0051-model'
        CONTAINER_NAME = 'wine-quality-container'
        API_URL = 'http://localhost:8000'

    stages {
        stage('Pull Image') {
            steps {
                script {
                    sh "docker pull ${DOCKER_IMAGE}"
                }
            }
        }

        stage('Run Container') {
            steps {
                script {
                    sh "docker run -d -p 8000:8000 --name ${CONTAINER_NAME} ${DOCKER_IMAGE}"
                }
            }
        }

        stage('Wait for Readiness') {
            steps {
                script {
                    timeout(time: 30, unit: 'SECONDS') {
                        waitUntil {
                            def response = sh(script: "curl -s -o /dev/null -w '%{http_code}' ${API_URL}/health", returnStdout: true).trim()
                            return response == '200'
                        }
                    }
                }
            }
        }

        stage('Valid Inference') {
            steps {
                script {
                    def response = sh(script: """
                        curl -s -X POST ${API_URL}/predict \
                        -H "Content-Type: application/json" \
                        -d '{"feature1": 5.1, "feature2": 3.5, "feature3": 1.4, "feature4": 0.2}'
                    """, returnStdout: true).trim()
                    echo "Response: ${response}"
                    if (!response.contains('wine_quality')) {
                        error("Valid inference test failed: wine_quality not found in response")
                    }
                    echo "name: ReshmanjaliMaddula, roll no: 2022bcd0051, ${response}"
                }
            }
        }

        stage('Invalid Input Test') {
            steps {
                script {
                    def responseCode = sh(script: """
                        curl -s -o /dev/null -w '%{http_code}' -X POST ${API_URL}/predict \
                        -H "Content-Type: application/json" \
                        -d '{"feature1": 5.1}'
                    """, returnStdout: true).trim()
                    if (!responseCode.startsWith('4') && !responseCode.startsWith('5')) {
                        error("Invalid input test failed: Expected 4xx/5xx, got ${responseCode}")
                    }
                }
            }
        }

        stage('Stop Container') {
            steps {
                script {
                    sh "docker stop ${CONTAINER_NAME}"
                    sh "docker rm ${CONTAINER_NAME}"
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}