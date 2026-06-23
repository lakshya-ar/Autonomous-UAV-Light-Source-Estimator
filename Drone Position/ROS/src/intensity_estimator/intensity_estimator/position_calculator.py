import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Point
from sympy import symbols, solve
import math

class PositionCalculator(Node):
    def __init__(self):
        super().__init__('position_calculator_node')
        self.subscription = self.create_subscription(Float32MultiArray, 'sensor_intensities', self.intensity_callback, 10)
        self.target_pub = self.create_publisher(Point, 'target_position', 10)
        self.last_reported_pos = None

    def intensity_callback(self, msg):
        I1, I2, I3, I4 = msg.data
        x, y, z = symbols('x y z', real=True)
        sensors = [(0.0, 0.0, 0.0), (5.0, 0.0, 0.0), (0.0, 5.0, 0.0), (2.5, 2.5, 5.0)]
        d_sqs = [(x-s[0])**2 + (y-s[1])**2 + (z-s[2])**2 for s in sensors]
        eqs = [I1 * d_sqs[0] - I2 * d_sqs[1], I1 * d_sqs[0] - I3 * d_sqs[2], I1 * d_sqs[0] - I4 * d_sqs[3]]
        solutions = solve(eqs, (x, y, z))
        best_sol = next((sol for sol in solutions if sol[2] >= 0), None)
        
        if best_sol:
            ax, ay, az = [float(val) for val in best_sol]
            self.target_pub.publish(Point(x=ax, y=ay, z=az))
            if self.last_reported_pos is None or math.dist((ax, ay, az), self.last_reported_pos) > 0.05:
                self.get_logger().info(f'Target Found: ({ax:.2f}, {ay:.2f}, {az:.2f})')
                self.last_reported_pos = (ax, ay, az)

def main(args=None):
    rclpy.init(args=args)
    node = PositionCalculator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()