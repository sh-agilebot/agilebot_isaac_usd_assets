# GBT-C5A Robot with Camera and Gripper Integrated Model

## Overview

This USD model provides a pre-configured integrated solution combining the GBT-C5A collaborative robot with a Robotiq 2F-140 gripper and an Orbbec Femto Mega camera. This model is designed for vision-guided robotics applications such as grasping, assembly, inspection, and other vision-aided tasks.

## Components

### Robot
- **Model**: GBT-C5A Collaborative Robot
- **Rated Payload**: 5 kg
- **Reach**: 850 mm
- **Features**: High-performance, cost-effective collaborative robot

### Gripper
- **Model**: Robotiq 2F-140
- **Type**: 2-finger adaptive gripper
- **Max Gripping Force**: 140 N
- **Stroke**: 140 mm
- **Features**: Adaptive underactuated fingers for versatile grasping

### Camera
- **Model**: Orbbec Femto Mega
- **Type**: RGB-D depth camera
- **Resolution**: 1280x1024 (RGB), 640x576 (Depth)
- **Frame Rate**: 30 FPS
- **Field of View**: 120° (H) × 90° (V) × 120° (D)
- **Features**: High-precision depth sensing, real-time data acquisition

### Camera Mount
- **Source**: Adapted from [MetaIsaacGrasp](https://github.com/YitianShi/MetaIsaacGrasp)
- **License**: MIT License
- **Description**: Custom-designed camera mount optimized for GBT-C5A robot

## Usage

### In Isaac Sim

1. **Open the Model**
   - Launch Isaac Sim
   - Go to `File > Open`
   - Navigate to `gbt-c5a_camera_gripper/` directory
   - Open `gbt-c5a_camera_gripper.usd`

2. **Add to Scene**
   - The model will appear in the viewport
   - The robot, gripper, and camera are pre-assembled and configured

3. **Physics Configuration**
   - The physics parameters are pre-configured with Isaac Sim recommended values
   - Active joints: Natural frequency = 300, Damping = 0.005
   - Linked joints: Natural frequency = 2500, Damping = 0.005

4. **Camera Setup**
   - The camera is mounted on the robot wrist
   - Camera data can be accessed through Isaac Sim's sensor API
   - RGB and depth data are available for vision processing

5. **Gripper Control**
   - The gripper is connected to the robot's end-effector
   - Gripper joints can be controlled through Isaac Sim's articulation API
   - Pre-configured for grasping applications

### Python API Example

```python
from omni.isaac.core import World
from omni.isaac.core.robots import Robot
from omni.isaac.sensor import Camera

# Create world
world = World(stage_units_in_meters=1.0)

# Load the integrated model
robot = world.scene.add(
    Robot(
        prim_path="/World/gbt_c5a_camera_gripper",
        name="gbt_c5a_camera_gripper",
        usd_path="gbt-c5a_camera_gripper/gbt-c5a_camera_gripper.usd"
    )
)

# Access camera
camera = Camera(
    prim_path="/World/gbt_c5a_camera_gripper/femto_mega",
    position=[0, 0, 0],
    frequency=30,
    resolution=(1280, 1024)
)

# Reset and simulate
world.reset()
while world.is_playing():
    world.step(render=True)
    # Access camera data
    rgb_data = camera.get_rgb()
    depth_data = camera.get_depth()
```

## Applications

- **Grasping**: Pick and place operations with visual feedback
- **Assembly**: Precision assembly with vision guidance
- **Inspection**: Quality control and defect detection
- **Bin Picking**: Random bin picking with depth sensing
- **Object Recognition**: Visual object identification and localization

## Technical Specifications

### Coordinate System
- **Robot Base**: Located at origin (0, 0, 0)
- **Camera Mount**: Attached to robot wrist (joint 6)
- **Gripper**: Attached to camera mount

### Joint Configuration
- **Robot Joints**: 6 DOF (j1 to j6)
- **Gripper Joints**: 2 DOF (left and right fingers)
- **Total DOF**: 8 DOF

### Physics Parameters
- **Active Joints**: Natural frequency = 300, Damping = 0.005
- **Linked Joints**: Natural frequency = 2500, Damping = 0.005
- **Optimization**: Based on Isaac Sim official recommendations

## Third-Party Components

### Robotiq Gripper
- **Source**: [Robotiq](https://robotiq.com/)
- **License**: Open-source model
- **Acknowledgment**: Thanks to Robotiq for providing the open-source gripper model

### Orbbec Camera
- **Source**: [Orbbec](https://www.orbbec3d.com/)
- **Product**: Femto Mega RGB-D Camera
- **Acknowledgment**: Thanks to Orbbec for providing the Femto Mega camera

### Camera Mount Design
- **Source**: [MetaIsaacGrasp](https://github.com/YitianShi/MetaIsaacGrasp)
- **License**: MIT License
- **Description**: Camera mount design adapted and optimized for GBT-C5A robot

## Notes

- The integrated model is pre-configured and ready to use
- Physics parameters have been optimized for stability
- Camera data is available in real-time during simulation
- Gripper control is fully integrated with robot articulation

## License

This integrated model follows the same license as the main project. Third-party components are used under their respective licenses as specified above.

## Support

For issues or questions related to:
- **GBT-C5A Robot**: Contact Agilebot
- **Robotiq Gripper**: Visit [Robotiq Support](https://robotiq.com/support)
- **Orbbec Camera**: Visit [Orbbec Support](https://www.orbbec3d.com/support)
- **Camera Mount**: Visit [MetaIsaacGrasp Repository](https://github.com/YitianShi/MetaIsaacGrasp)
