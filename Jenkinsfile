pipeline {
    agent any

    environment {
        DOCKERHUB_USER  = "akila280197"
        IMAGE_NAME      = "hello-world-devops"
        IMAGE_TAG       = "${env.BUILD_NUMBER}"
        FULL_IMAGE      = "${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
        CONTAINER_NAME  = "hello-world-app"
        APP_PORT        = "8081"
        SONAR_URL       = "http://your-ec2-public-ip:9000"
    }

    stages {

        stage('Checkout') {
            steps {
                echo "========== STAGE 1: Checkout =========="
                checkout scm
                echo "Code checked out successfully ✅"
                sh 'ls -la'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo "========== STAGE 2: Install Dependencies =========="
                sh '''
                    pip3 install -r requirements.txt
                '''
                echo "Dependencies installed ✅"
            }
        }

        stage('Run Tests') {
            steps {
                echo "========== STAGE 3: Run Tests =========="
                sh '''
                    pip3 install pytest
                    python3 -m pytest test_app.py -v
                '''
                echo "All tests passed ✅"
            }
        }

     stage('SonarQube Analysis') {
    steps {
        echo "========== STAGE 4: SonarQube Analysis =========="
        withCredentials([string(
            credentialsId: 'sonar-token',
            variable: 'SONAR_TOKEN'
        )]) {
            sh """
                /opt/sonar-scanner/bin/sonar-scanner \
                  -Dsonar.projectKey=hello-world-devops \
                  -Dsonar.sources=. \
                  -Dsonar.host.url=${SONAR_URL} \
                  -Dsonar.token=${SONAR_TOKEN}
            """
        }
        echo "SonarQube analysis completed ✅"
    }
}

        stage('Build Docker Image') {
            steps {
                echo "========== STAGE 5: Build Docker Image =========="
                sh "docker build -t ${FULL_IMAGE} ."
                echo "Docker image built ✅"
                sh "docker images | grep ${IMAGE_NAME}"
            }
        }

        stage('Push to DockerHub') {
            steps {
                echo "========== STAGE 6: Push to DockerHub =========="
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo $DOCKER_PASS | \
                          docker login -u $DOCKER_USER --password-stdin
                        docker push ${FULL_IMAGE}
                        docker logout
                    '''
                }
                echo "Image pushed to DockerHub ✅"
            }
        }

        stage('Deploy') {
            steps {
                echo "========== STAGE 7: Deploy =========="
                sh """
                    docker stop ${CONTAINER_NAME} || true
                    docker rm   ${CONTAINER_NAME} || true

                    docker run -d \
                      --name ${CONTAINER_NAME} \
                      -p ${APP_PORT}:8081 \
                      --restart always \
                      ${FULL_IMAGE}

                    docker ps | grep ${CONTAINER_NAME}
                """
                echo "Application deployed ✅"
            }
        }
    }

    post {
        success {
            echo """
            ============================================
            ✅ PIPELINE SUCCEEDED!
            Image: ${FULL_IMAGE}
            App URL: http://your-ec2-ip:${APP_PORT}
            Build: #${env.BUILD_NUMBER}
            ============================================
            """
        }
        failure {
            echo """
            ============================================
            ❌ PIPELINE FAILED!
            Build: #${env.BUILD_NUMBER}
            Check console output for details
            ============================================
            """
        }
        always {
            echo "Pipeline completed — Build #${env.BUILD_NUMBER}"
            sh "docker image prune -f || true"
        }
    }
}
