import subprocess
import time
import os
import signal

# 1. Setup Environment
cwd = os.getcwd()
env = os.environ.copy()
# Ensuring your custom workspace is in the python path
env["PYTHONPATH"] = f"{cwd}/src/intensity_estimator:{env.get('PYTHONPATH', '')}"

nodes = []

def start_node(cmd):
    p = subprocess.Popen(cmd, env=env, shell=True, preexec_fn=os.setsid)
    nodes.append(p)
    return p

print("Launching...")

try:
    # 2. Start the Static Transform (Fixed Frame)
    start_node("ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 map base_link")
    
    # 3. Start the Logic Nodes
    start_node("python3 src/intensity_estimator/intensity_estimator/drone_sensor.py")
    start_node("python3 src/intensity_estimator/intensity_estimator/position_calculator.py")
    start_node("python3 src/intensity_estimator/intensity_estimator/drone_controller.py")
    
    # 4. Start RViz with the AUTO-CONFIG file
    config_path = "src/intensity_estimator/drone_sim.rviz"
    print(f"Loading RViz config from: {config_path}")
    start_node(f"rviz2 -d {config_path}")

    print("\n All systems GO. Press Ctrl+C to shut down everything.")
    
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\n Shutting down all nodes...")
    for node in nodes:
        try:
            os.killpg(os.getpgid(node.pid), signal.SIGTERM)
        except:
            pass
    print("Done.")