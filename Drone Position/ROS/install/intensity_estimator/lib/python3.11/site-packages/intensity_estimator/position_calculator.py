import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
from sympy import symbols, solve

class PositionCalculator(Node):
    def __init__(self):
        super().__init__('position_calculator_node')
        self.subscription = self.create_subscription(
            Float32MultiArray, 'sensor_intensities', self.intensity_callback, 10)

    def intensity_callback(self, msg):
        I1, I2, I3, I4 = msg.data
        x, y, z = symbols('x y z', real=True)

        # FIXED SENSOR LOCATIONS
        x1, y1, z1 = 0.0, 0.0, 0.0   # B
        x2, y2, z2 = 5.0, 0.0, 0.0   # C
        x3, y3, z3 = 0.0, 5.0, 0.0   # D
        x4, y4, z4 = 2.5, 2.5, 5.0   # E
        d1_sq = (x-x1)**2 + (y-y1)**2 + (z-z1)**2
        d2_sq = (x-x2)**2 + (y-y2)**2 + (z-z2)**2
        d3_sq = (x-x3)**2 + (y-y3)**2 + (z-z3)**2
        d4_sq = (x-x4)**2 + (y-y4)**2 + (z-z4)**2

        eq1 = I1 * d1_sq - I2 * d2_sq
        eq2 = I1 * d1_sq - I3 * d3_sq
        eq3 = I1 * d1_sq - I4 * d4_sq

        # Solve for x, y, z
        solutions = solve((eq1, eq2, eq3), (x, y, z))

        if solutions:
            best_sol = None
            for sol in solutions:
                if sol[2] >= 0: # Check Z coordinate
                    best_sol = sol
                    break
            
            if best_sol:
                ax, ay, az = [float(val) for val in best_sol]
                
                # NOW CALCULATE P EXACTLY
                # P = I * d^2
                dist_sq_to_B = (ax - x1)**2 + (ay - y1)**2 + (az - z1)**2
                calculated_P = I1 * dist_sq_to_B
                
                self.get_logger().info(f'--- TARGET FOUND ---')
                self.get_logger().info(f'Coord A: ({ax:.3f}, {ay:.3f}, {az:.3f})')
                self.get_logger().info(f'Calculated Power P: {calculated_P:.2f}')
                self.get_logger().info(f'--------------------')

def main(args=None):
    rclpy.init(args=args)
    node = PositionCalculator()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()