from setuptools import find_packages, setup

package_name = 'intensity_estimator'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='lakshya',
    maintainer_email='lakshya@todo.todo',
    description='Intensity based position estimator',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'position_node = intensity_estimator.position_calculator:main',
            'sensor_node = intensity_estimator.drone_sensor:main',
            'drone_controller = intensity_estimator.drone_controller:main',
        ],
    },
)