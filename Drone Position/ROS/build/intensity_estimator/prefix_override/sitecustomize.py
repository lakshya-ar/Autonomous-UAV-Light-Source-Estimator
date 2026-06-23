import sys
if sys.prefix == '/Users/lakshya/miniconda3/envs/ros2':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/Users/lakshya/Library/CloudStorage/OneDrive-IITKanpur/IITK/ROS/install/intensity_estimator'
