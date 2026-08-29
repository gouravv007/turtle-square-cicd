pipeline {
    agent any

    environment {
        IMAGE_NAME = "turtle_square"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$BUILD_NUMBER .'
            }
        }

        stage('Unit Test') {
            steps {
                sh '''
                    docker run --rm $IMAGE_NAME:$BUILD_NUMBER /bin/bash -c "\
                    source /opt/ros/humble/setup.bash && \
                    source /ros2_ws/install/setup.bash && \
                    colcon test --packages-select turtle_square && \
                    colcon test-result --verbose"
                '''
            }
        }

        stage('Smoke Test (headless turtlesim)') {
            steps {
                sh '''
                    docker run --rm $IMAGE_NAME:$BUILD_NUMBER /bin/bash -c "\
                    source /opt/ros/humble/setup.bash && \
                    source /ros2_ws/install/setup.bash && \
                    xvfb-run -a bash -c 'ros2 run turtlesim turtlesim_node & sleep 3 && timeout 8 ros2 run turtle_square square_node'"
                '''
            }
        }

        stage('Deploy (self-update)') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                    docker tag $IMAGE_NAME:$BUILD_NUMBER $IMAGE_NAME:latest
                    docker rm -f turtle_square_running || true
                    docker run -d --name turtle_square_running $IMAGE_NAME:latest \
                        /bin/bash -c "source /opt/ros/humble/setup.bash && source /ros2_ws/install/setup.bash && xvfb-run -a ros2 launch turtle_square square.launch.py"
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded - new version deployed automatically.'
        }
        failure {
            echo 'Build/test failed - deployment skipped, old version keeps running.'
        }
    }
}
