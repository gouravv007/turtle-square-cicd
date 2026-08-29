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
                // --shm-size: Xvfb + turtlesim require >64 MB shared memory; default Docker shm
                // causes SIGKILL (exit 137). Manual Xvfb avoids xvfb-run swallowing the
                // background turtlesim_node before it exits.
                sh '''
                    docker run --rm --shm-size=256m $IMAGE_NAME:$BUILD_NUMBER /bin/bash -c '
                        source /opt/ros/humble/setup.bash &&
                        source /ros2_ws/install/setup.bash &&
                        export RCUTILS_LOGGING_SEVERITY=WARN &&
                        Xvfb :99 -screen 0 1024x768x24 &
                        sleep 2 &&
                        export DISPLAY=:99 &&
                        ros2 run turtlesim turtlesim_node &
                        sleep 4 &&
                        timeout 10 ros2 run turtle_square square_node
                    '
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
                    docker run -d --name turtle_square_running --shm-size=256m $IMAGE_NAME:latest \
                        /bin/bash -c 'Xvfb :99 -screen 0 1024x768x24 & sleep 2 && export DISPLAY=:99 && source /opt/ros/humble/setup.bash && source /ros2_ws/install/setup.bash && ros2 launch turtle_square square.launch.py'
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
