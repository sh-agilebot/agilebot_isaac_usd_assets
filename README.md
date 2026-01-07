# Agilebot Robotics USD Assets

[![License: BSD 3-Clause](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](LICENSE)
[![Isaac Sim](https://img.shields.io/badge/Isaac%20Sim-Compatible-green.svg)](https://developer.nvidia.com/isaac-sim)
[![USD](https://img.shields.io/badge/USD-Universal%20Scene%20Description-orange.svg)](https://openusd.org/)

**Language:** [English](README.md) | [中文](README_zh.md)

---

## 📖 Project Overview

This repository contains **USD (Universal Scene Description)** digital assets for Agilebot Robotics' robot products, primarily targeting the **NVIDIA Isaac Sim and Isaac Lab** ecosystems for robot modeling, physics simulation, algorithm validation, and application development.

USD is an open standard for complex 3D scenes, supporting efficient hierarchical organization, composition, variants, physics, and semantic extensions. Through USD format, these robot models can be directly used in Isaac Sim, Isaac Lab, and Omniverse-related toolchains, with flexible component configuration and extension capabilities.

---

## 📁 Directory Structure

```
agilebot_usd_assets/
├── gbt-c5a/                    # GBT-C5A collaborative robot model
│   ├── Gripper/
│   │   └── robotiq_2f_140.usd  # Robotiq 2F-140 gripper model
│   ├── configuration/
│   │   ├── materials/          # Material and texture resources
│   │   ├── gbt-c5a_base.usd    # Robot base structure
│   │   ├── gbt-c5a_physics.usd # Physics and joint properties
│   │   ├── gbt-c5a_robot.usd   # Main robot definition
│   │   └── gbt-c5a_sensor.usd  # Sensor configuration
│   └── gbt-c5a.usd             # Main entry USD file
├── gbt-c5a_camera_gripper/     # GBT-C5A with camera and gripper integrated model
│   └── gbt-c5a_camera_gripper.usd # Main entry USD file
├── gbt-c7a/                    # GBT-C7A collaborative robot model
│   └── (Same structure as gbt-c5a)
├── gbt-c12a/                   # GBT-C12A collaborative robot model
│   └── (Same structure as gbt-c5a)
├── gbt-c16a/                   # GBT-C16A collaborative robot model
│   └── (Same structure as gbt-c5a)
├── LICENSE                     # BSD 3-Clause License
├── README.md                   # This file (English version)
└── README_zh.md                # Chinese version
```

---

## 🤖 Robot Models

### GBT-C5A Collaborative Robot

- **Rated Payload**: 5 kg  
- **Working Radius**: 850 mm  
- **Features**: High-performance, cost-effective collaborative robot  
- **Applications**: Assembly, gluing, inspection, and other collaborative tasks  

### GBT-C5A with Camera and Gripper Integrated Model

- **Composition**: GBT-C5A robot + Robotiq 2F-140 gripper + Orbbec Femto Mega camera  
- **Camera Mount**: Adapted from [MetaIsaacGrasp](https://github.com/YitianShi/MetaIsaacGrasp) (MIT License)  
- **Features**: Pre-configured integrated solution for vision-guided robotics applications  
- **Applications**: Grasping, assembly, inspection, and other vision-aided tasks  

### GBT-C7A Collaborative Robot

- **Rated Payload**: 7 kg  
- **Features**: Medium-load collaborative robot suitable for various industrial applications  

### GBT-C12A Collaborative Robot

- **Rated Payload**: 12 kg  
- **Features**: High-load collaborative robot suitable for various industrial applications  
- **Applications**: Heavy-duty assembly, material handling, etc.  

### GBT-C16A Collaborative Robot

- **Rated Payload**: 16 kg  
- **Features**: Large-load collaborative robot suitable for heavy-duty operations  

---

## 🔧 Gripper Configuration and Variant Switching

Each robot model provides **Robotiq 2F-140 gripper variant**, integrated as a USD VariantSet, allowing dynamic switching without modifying the USD structure.

### Gripper Variant List

| Robot Model | Gripper Variant | File Path |
|------------|----------|----------|
| GBT-C5A | robotiq_2f_140 | `gbt-c5a/Gripper/robotiq_2f_140.usd` |
| GBT-C7A | robotiq_2f_140 | `gbt-c7a/Gripper/robotiq_2f_140.usd` |
| GBT-C12A | robotiq_2f_140 | `gbt-c12a/Gripper/robotiq_2f_140.usd` |
| GBT-C16A | robotiq_2f_140 | `gbt-c16a/Gripper/robotiq_2f_140.usd` |

### Switch Gripper Variant via Python API

In Isaac Sim / Isaac Lab, you can dynamically switch gripper configurations using the USD Python API:

```python
# Enable Robotiq 2F-140 gripper
robot.GetVariantSet("Gripper").SetVariantSelection("robotiq_2f_140")

# No gripper (bare flange)
robot.GetVariantSet("Gripper").SetVariantSelection("None")
```

This method is suitable for:

* End-effector switching for different tasks
* Quick comparison testing of grippers/tools
* Automated configuration in reinforcement learning or batch simulations

---

## 💡 Tips

### Gripper Grasping Issues

If you experience **gripper clipping through objects or dropping** during grasping operations, try the following adjustments:

1. **Reduce gripper max force**: Lower the maximum force to single-digit values (e.g., 1-5 N) to reduce the gripping strength
2. **Significantly reduce physics simulation frame rate**: Lower the physics simulation frame rate to the default 60 FPS to reduce computational burden
    ```
    world = World(stage_units_in_meters=1.0, physics_dt=1/60.0)
    ```

These adjustments help prevent the gripper from applying excessive force that causes object penetration, but they may introduce other grasping issues. Please adjust dynamically based on your usage scenario.

---

## 📦 Gripper Model Source

The gripper model is sourced from the open-source project:
[robotiq_2f_gripper](https://github.com/gen-robot/robotiq_2f_gripper/tree/main/robotiq_2f_140_gripper_visualization)

This model is for simulation and demonstration purposes only, and its copyright belongs to the original author.

Gripper import and assembly process refers to NVIDIA official documentation:
[Isaac Sim Robot Import and Assembly Tutorial](https://docs.isaacsim.omniverse.nvidia.com/latest/robot_setup_tutorials/tutorial_import_assemble_manipulator.html)

---

## 🖥️ Experimental Environment

**Test Environment:**

- **System**: Ubuntu 22.04
- **GPU**: NVIDIA RTX 5090
- **Isaac Sim Version**: 5.1.0-rc.19+release.26219.9c81211b.gl
- **Isaac Lab Version**: 2.3.0

---

## 🚀 Usage

### Using in Isaac Sim

The current version provides standardized USD asset files, which can be directly loaded via Isaac Sim's USD Loader or Reference method. Complete sample projects for Isaac Sim will be provided in future releases.

### Using in Isaac Lab

The current version can be used as input for `Articulation` or custom assets in Isaac Lab. Task configurations and examples will be released separately.

---

## ⚠️ Physics Parameters Notice

**Important Note on Physics Parameters:**

For all robot models, the joint natural frequency and damping parameters have been configured with Isaac Sim recommended empirical values:

- **Active Joints**: Natural frequency = 300, Damping = 0.005
- **Linked Joints**: Natural frequency = 2500, Damping = 0.005

These values are based on Isaac Sim official recommendations and have been tested to reduce issues like robot flying or shaking during simulation.

Regarding mass and directional inertia:
- **GBT-C5A**: Manually calculated by Agilebot
- **Other Models (GBT-C7A, GBT-C12A, GBT-C16A)**: Automatically generated by SolidWorks or Isaac Sim

Please manually adjust these parameters according to your specific simulation requirements to ensure accurate behavior.

---

## 🤝 Contribution Guidelines

Contributions are welcome via Issues and Pull Requests.

### Contribution Process

1. Fork this repository
2. Create a feature branch: `git checkout -b feature/AmazingFeature`
3. Commit changes: `git commit -m "Add some AmazingFeature"`
4. Push to remote branch: `git push origin feature/AmazingFeature`
5. Create a Pull Request

---

## 📄 License

This project is licensed under the **BSD 3-Clause License**, see [LICENSE](LICENSE) for details.

---

## 📞 Contact

* **Business Inquiry**: [info@agilebot.com.cn](mailto:info@agilebot.com.cn)
* **Technical Support**: 400-996-7588
* **Official Website**: [https://www.sh-agilebot.com/](https://www.sh-agilebot.com/)

---

## 🙏 Acknowledgments

Thanks to the [NVIDIA Isaac Sim](https://developer.nvidia.com/isaac-sim) and [Isaac Lab](https://isaac-sim.github.io/IsaacLab/) teams for providing excellent robot simulation platforms.

Special thanks to [Robotiq](https://robotiq.com/) for their open-source gripper model, which enhances the versatility of our robot assets.

Thanks to [Orbbec](https://www.orbbec3d.com/) for their Femto Mega camera, which enables vision-guided robotics applications.

Thanks to [MetaIsaacGrasp](https://github.com/YitianShi/MetaIsaacGrasp) for their camera mount design, which is used under the MIT License.

For detailed information about third-party licenses, please refer to [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).

---

## 📋 Changelog

For detailed version history and changes, please refer to [CHANGELOG.md](CHANGELOG.md).

---

## 🗺️ Roadmap

Future development plans include:

### Industrial Robot Models
- [ ] GBT-S3A - 3 kg payload industrial SCARA robot
- [ ] GBT-S6A - 6 kg payload industrial SCARA robot
- [ ] GBT-S10A - 10 kg payload industrial SCARA robot
- [ ] GBT-S20A - 20 kg payload industrial SCARA robot
- [ ] GBT-P7A - 7 kg payload industrial PUMA robot

### Physics Parameters
- [ ] Provide default physics parameters for GBT-C7A
- [ ] Provide default physics parameters for GBT-C12A
- [ ] Provide default physics parameters for GBT-C16A

---

## 🏢 About Agilebot Robotics

Shanghai Agilebot Robotics Co., Ltd. is a professional provider of industrial robots and intelligent magnetic drive conveyor systems. With the vision of "Driving Future Factories", the company provides high-performance, high-quality, cost-effective, and easy-to-use robot products based on advanced integrated drive and control technology.

The product line covers collaborative robots, industrial six-axis robots, and SCARA robots, widely used in assembly, material handling, inspection, and other industrial scenarios.

* **Official Website**: [https://www.sh-agilebot.com/](https://www.sh-agilebot.com/)
* **Business Email**: [info@agilebot.com.cn](mailto:info@agilebot.com.cn)
* **Contact Phone**: 400-996-7588

---

© 2026 Agilebot Robotics. All rights reserved.
