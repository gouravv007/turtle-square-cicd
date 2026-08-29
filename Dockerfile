# Dockerfile
FROM ros:humble-ros-base

# Install build tools, test deps, and xvfb for headless GUI (turtlesim needs a display)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-pytest \
    ros-humble-turtlesim \
    xvfb \
    git \
    && rm -rf /var/lib/apt/lists/*

# rosdep init only if not already done in base image
RUN rosdep update || true

WORKDIR /ros2_ws

COPY src ./src

RUN /bin/bash -c "source /opt/ros/humble/setup.bash && \
    rosdep install --from-paths src --ignore-src -r -y"

RUN /bin/bash -c "source /opt/ros/humble/setup.bash && \
    colcon build --symlink-install"

# Default entrypoint sources both ROS and the workspace
RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc && \
    echo "source /ros2_ws/install/setup.bash" >> /root/.bashrc

CMD ["/bin/bash"]
