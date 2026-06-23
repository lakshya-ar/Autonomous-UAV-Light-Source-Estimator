---
title: 'Autonomous UAV Light Source Estimator '

---

# Autonomous UAV Light Source Estimator

![ROS 2](https://img.shields.io/badge/ROS_2-Humble-22314E?logo=ros)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)
![SymPy](https://img.shields.io/badge/Math-SymPy-green)

An autonomous localization framework designed for Unmanned Aerial Vehicles (UAVs). This ROS 2 package continuously processes intensity data from four distributed ground or structural sensors to estimate the exact 3D coordinates of a target light source using multilateration. It seamlessly translates raw sensor streams into real-time target waypoints for automated flight navigation.

**Developed for the AE Winter Project at the Indian Institute of Technology Kanpur.**

---

## Table of Contents
- [System Architecture](#-system-architecture)
- [Mathematical Formulation](#-mathematical-formulation)
- [File Structure](#-file-structure)
- [Prerequisites](#-prerequisites)
- [Installation & Build](#-installation--build)
- [Usage & Testing](#-usage--testing)
- [Future Scope](#-future-scope)

---

## System Architecture

The project is built on a decoupled ROS 2 Publisher-Subscriber architecture, ensuring the mathematical estimation logic is isolated and scalable for future physics engine integrations.

### Node Specifications
* **Package Name:** `intensity_estimator`
* **Executable Node:** `position_node`

### Topic Interactions
* **Subscribes to:** `/sensor_intensities` 
  * **Type:** `std_msgs/msg/Float32MultiArray`
  * **Function:** Ingests an array of 4 floating-point values representing the real-time light intensity captured at each known sensor location.
* **Publishes to:** `/target_position`
  * **Type:** `geometry_msgs/msg/Point`
  * **Function:** Outputs the computed spatial coordinate (x, y, z) of the target light source, serving as a directional waypoint for the UAV.

---

## Mathematical Formulation

The localization core relies on the **Inverse Square Law** of light propagation, which dictates that the intensity I is inversely proportional to the square of the distance d from the source:

$$I \propto \frac{1}{d^2}$$

Given four sensors positioned at predefined coordinates (x_i, y_i, z_i), the system establishes the following relationship for the distances to the unknown target (x, y, z):

$$I_1 \cdot d_1^2 = I_2 \cdot d_2^2$$
$$I_2 \cdot d_2^2 = I_3 \cdot d_3^2$$
$$I_3 \cdot d_3^2 = I_4 \cdot d_4^2$$

The node leverages Python's `SymPy` library to evaluate these non-linear difference equations in real-time, isolating the target coordinates and filtering for the valid physical solution.

---

## File Structure

    Drone Position/
    ├── Task_1.py                     # Independent task script
    ├── Task1_UI.py                   # Independent task UI interface
    └── ROS/                          # Main ROS 2 Workspace
        └── src/
            └── intensity_estimator/
                ├── package.xml
                ├── setup.py
                ├── setup.cfg
                └── intensity_estimator/
                    ├── __init__.py
                    └── position_calculator.py

---

## Prerequisites

Ensure your system meets the following requirements before building the workspace:
* **OS:** Ubuntu 22.04 / macOS (via Conda/RoboStack)
* **Framework:** ROS 2 (Humble Hawksbill or later)
* **Language:** Python 3.10+
* **Dependencies:** `SymPy`, `colcon-common-extensions`

---

## Installation & Build

**1. Clone the repository into your workspace:**

    mkdir -p ~/Drone\ Position/ROS/src
    cd ~/Drone\ Position/ROS/src
    git clone https://github.com/lakshya-ar/Autonomous-UAV-Light-Source-Estimator.git


**2. Install Python Dependencies:**
*(Note: If using a Conda environment, ensure it is activated before running this command).*

    pip install sympy


**3. Build the ROS 2 Workspace:**
Navigate back to the root of your ROS workspace and compile the package using `colcon`.

    cd ~/Drone\ Position/ROS
    colcon build --packages-select intensity_estimator


---

## Usage & Testing

**1. Source the Environment:**
You must source both your base ROS 2 installation and your local workspace overlay.

    # Example for standard Linux installs
    source /opt/ros/humble/setup.bash
    source ~/Drone\ Position/ROS/install/setup.bash


**2. Launch the Estimator Node:**

    ros2 run intensity_estimator position_node

*Expected Terminal Output:*
`[INFO] [light_estimator_node]: Light Estimator Node started. Waiting for data...`

**3. Simulate Sensor Data (Testing):**
To verify the math logic without a physical sensor array, open a second terminal, source your environment, and publish a mock intensity array:

    ros2 topic pub --once /sensor_intensities std_msgs/msg/Float32MultiArray "{data: [100.0, 80.5, 90.2, 75.0]}"

The estimator node will instantly compute and print the resolved (x, y, z) coordinates.

---

## Future Scope

* **Gazebo Integration:** Mapping the `/target_position` node into a 3D simulated physics environment to track dynamic target movement.
* **Flight Controller Pipeline:** Forwarding the spatial output directly to ArduPilot or PX4 firmware to automate physical drone pitching and yawing toward the target.
* **Dynamic Filtering:** Implementing an Extended Kalman Filter (EKF) or Exponential Moving Average (EMA) to smooth noisy intensity inputs from physical photodiode sensors.