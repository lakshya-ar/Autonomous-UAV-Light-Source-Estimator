import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray

class VirtualLabSensors(Node):
    def __init__(self):
        super().__init__('sensor_node')
        self.publisher_ = self.create_publisher(Float32MultiArray, 'sensor_intensities', 10)
        
        # GROUND TRUTH
        self.target_a = (2.0, 2.0, 2.0) 
        self.P_true = 1000.0  
        
        # Fixed Sensor Locations (B, C, D, E)
        self.sensors = [(0.0, 0.0, 0.0), (5.0, 0.0, 0.0), (0.0, 5.0, 0.0), (2.5, 2.5, 5.0)]
        
        self.timer = self.create_timer(2.0, self.timer_callback) # Slow pulse every 2s
        self.get_logger().info(f"Virtual Sensors Active. Target at {self.target_a}")

    def timer_callback(self):
        tx, ty, tz = self.target_a
        intensities = []
        for (sx, sy, sz) in self.sensors:
            dist_sq = (tx - sx)**2 + (ty - sy)**2 + (tz - sz)**2
            intensities.append(float(self.P_true / max(dist_sq, 0.01)))
            
        msg = Float32MultiArray(data=intensities)
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = VirtualLabSensors()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()