import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


def next_command(step: int) -> Twist:
    """Pure logic, no ROS - easy to unit test without a simulator."""
    cmd = Twist()
    if step % 2 == 0:
        cmd.linear.x = 2.0
    else:
        cmd.angular.z = 1.5708  # 90 degrees
    return cmd


class SquareNode(Node):
    def __init__(self):
        super().__init__('turtle_square')
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.step = 0
        self.timer = self.create_timer(2.0, self.tick)

    def tick(self):
        cmd = next_command(self.step)
        self.publisher.publish(cmd)
        self.get_logger().info(f'Step {self.step}: lin={cmd.linear.x} ang={cmd.angular.z}')
        self.step = (self.step + 1) % 8


def main(args=None):
    rclpy.init(args=args)
    node = SquareNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
