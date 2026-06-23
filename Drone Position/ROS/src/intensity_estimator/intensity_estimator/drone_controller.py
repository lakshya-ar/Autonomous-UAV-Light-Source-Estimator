import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point, Twist
from visualization_msgs.msg import Marker
import math

class DroneController(Node):
    def __init__(self):
        super().__init__('drone_controller')
        self.create_subscription(Point, 'target_position', self.target_callback, 10)
        self.marker_pub = self.create_publisher(Marker, 'visualization_marker', 10)
        self.vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        
        self.current_pos = [0.0, 0.0, 0.0] 
        self.target_pos = None
        self.mission_started = False
        
        self.timer = self.create_timer(0.1, self.control_loop)
        self.get_logger().info("Pilot ready. Waiting for first target...")

    def target_callback(self, msg):
        self.target_pos = [msg.x, msg.y, msg.z]
        self.mission_started = True 
        # Create the Red Sphere in RViz
        self.publish_marker(msg.x, msg.y, msg.z, 0, [1.0, 0.0, 0.0], Marker.SPHERE)

    # THIS IS THE MISSING FUNCTION THAT CAUSED YOUR ERROR
    def publish_marker(self, x, y, z, id, color, m_type):
        marker = Marker()
        marker.header.frame_id = "map"
        marker.header.stamp = rclpy.time.Time().to_msg()
        marker.id = id
        marker.type = m_type
        marker.action = Marker.ADD
        marker.pose.position.x = float(x)
        marker.pose.position.y = float(y)
        marker.pose.position.z = float(z)
        marker.scale.x = marker.scale.y = marker.scale.z = 0.5
        marker.color.r, marker.color.g, marker.color.b, marker.color.a = color[0], color[1], color[2], 1.0
        self.marker_pub.publish(marker)

    def control_loop(self):
        if not self.mission_started or self.target_pos is None:
            return

        dx = self.target_pos[0] - self.current_pos[0]
        dy = self.target_pos[1] - self.current_pos[1]
        dz = self.target_pos[2] - self.current_pos[2]
        dist = math.sqrt(dx**2 + dy**2 + dz**2)
        
        if dist < 0.05:
            self.get_logger().info("--- TARGET REACHED ---")
            self.timer.cancel() 
        else:
            # P-Control: Move 5% of the distance every 0.1s
            self.current_pos[0] += dx * 0.05
            self.current_pos[1] += dy * 0.05
            self.current_pos[2] += dz * 0.05
            
            # Update Green Drone Cube in RViz
            self.publish_marker(self.current_pos[0], self.current_pos[1], self.current_pos[2], 1, [0.0, 1.0, 0.0], Marker.CUBE)
            self.get_logger().info(f"Flying... Distance: {dist:.2f}m")

def main(args=None):
    rclpy.init(args=args)
    node = DroneController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()