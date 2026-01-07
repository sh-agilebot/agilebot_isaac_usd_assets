# Agilebot Robotics USD Assets

[![License: BSD 3-Clause](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](LICENSE)
[![Isaac Sim](https://img.shields.io/badge/Isaac%20Sim-Compatible-green.svg)](https://developer.nvidia.com/isaac-sim)
[![USD](https://img.shields.io/badge/USD-Universal%20Scene%20Description-orange.svg)](https://openusd.org/)

**语言 / Language:** [English](README.md) | [中文](README_zh.md)

![Agilebot Robots in Isaac Sim](docs/images/agilebot_robots_simulation.png)

---

## 📖 仓库简介

本仓库是 Agilebot Robotics 官方 Isaac 生态的核心资产仓库，包含全系列协作机器人的 **USD（Universal Scene Description）** 数字资产，主要面向 **NVIDIA Isaac Sim 与 Isaac Lab** 生态，用于机器人建模、物理仿真、算法验证与应用开发。

### 核心价值

- **标准化资产**：所有机器人模型均采用 USD 格式，支持跨平台、跨工具的无缝集成
- **物理优化**：预配置的关节自然频率和阻尼参数，确保仿真稳定性和准确性
- **变体支持**：内置夹爪变体，可动态切换末端执行器配置
- **即开即用**：无需额外配置，直接在 Isaac Sim 和 Isaac Lab 中加载使用

USD 是一种面向复杂三维场景的开放标准，支持高效的层级组织、组合（Composition）、变体（Variant）、物理与语义扩展。通过标准化的 USD 格式，您可以快速将这些机器人模型集成到 Isaac Sim、Isaac Lab 及 Omniverse 相关工具链中，并支持灵活的组件配置与扩展。

---

## 🔗 生态系统与相关仓库

本仓库与以下仓库共同组成完整的 Agilebot Isaac 仿真与学习工作流：

| 仓库名称 | 功能定位 | 主要内容 |
|----------|----------|----------|
| **[agilebot_isaac_sim](https://github.com/sh-agilebot/agilebot_isaac_sim)** | 仿真集成 | Agilebot 机器人在 NVIDIA Isaac Sim 中的集成仓库，包含仿真配置、环境设置及示例 Demo。*不包含任何机器人数字资产。* |
| **[agilebot_isaac_lab](https://github.com/sh-agilebot/agilebot_isaac_lab)** | 训练学习 | 基于 NVIDIA Isaac Lab 的训练与学习仓库，包含任务定义、环境配置及训练示例。*不包含任何机器人数字资产。* |
| **[agilebot_isaac_usd_assets](https://github.com/sh-agilebot/agilebot_isaac_usd_assets)** | 资产管理 | 本仓库，统一维护 Agilebot 机器人的 USD 模型、网格文件及贴图资源。 |

---

## 📁 目录结构

```
agilebot_usd_assets/
├── gbt-c5a/                    # GBT-C5A 协作机器人模型
│   ├── Gripper/
│   │   └── robotiq_2f_140.usd  # Robotiq 2F-140 夹爪模型
│   ├── configuration/
│   │   ├── materials/          # 材质与纹理资源
│   │   ├── gbt-c5a_base.usd    # 机器人基础结构
│   │   ├── gbt-c5a_physics.usd # 物理与关节属性
│   │   ├── gbt-c5a_robot.usd   # 机器人主体定义
│   │   └── gbt-c5a_sensor.usd  # 传感器配置
│   └── gbt-c5a.usd             # 主入口 USD 文件
├── gbt-c5a_camera_gripper/     # GBT-C5A 机器人+相机+夹爪集成模型
│   └── gbt-c5a_camera_gripper.usd # 主入口 USD 文件
├── gbt-c7a/                    # GBT-C7A 协作机器人模型
│   └── (结构与 gbt-c5a 相同)
├── gbt-c12a/                   # GBT-C12A 协作机器人模型
│   └── (结构与 gbt-c5a 相同)
├── gbt-c16a/                   # GBT-C16A 协作机器人模型
│   └── (结构与 gbt-c5a 相同)
├── LICENSE                     # BSD 3-Clause License
├── README.md                   # 英文版 README
└── README_zh.md                # 中文版 README
```

---

## 🤖 机器人型号

### GBT-C5A 协作机器人

- **额定负载**：5 kg  
- **工作半径**：850 mm  
- **特点**：高配置、高性能、高性价比的首款协作机器人  
- **适用场景**：装配、涂胶、检测等协作应用  

### GBT-C5A 机器人+相机+夹爪集成模型

- **组成**：GBT-C5A 机器人 + Robotiq 2F-140 夹爪 + 奥比中光 Femto Mega 相机  
- **相机支架**：适配自 [MetaIsaacGrasp](https://github.com/YitianShi/MetaIsaacGrasp)（MIT 许可证）  
- **特点**：预配置的集成解决方案，适用于视觉引导机器人应用  
- **适用场景**：抓取、装配、检测等视觉辅助任务  

### GBT-C7A 协作机器人

- **额定负载**：7 kg  
- **特点**：中等负载协作机器人，适用于多种工业应用  

### GBT-C12A 协作机器人

- **额定负载**：12 kg  
- **特点**：高负载协作机器人，适用于多种工业应用 
- **适用场景**：重载装配、搬运等应用  

### GBT-C16A 协作机器人

- **额定负载**：16 kg  
- **特点**：大负载协作机器人，适用于重载作业场景  

---

## 🔧 夹爪配置与 Variant 切换

每个机器人型号均提供 **Robotiq 2F-140 夹爪变体**，夹爪以 **USD VariantSet** 的形式集成在机器人模型中，可在不修改 USD 结构的情况下动态切换。

### 夹爪变体列表

| 机器人型号 | 夹爪变体 | 文件路径 |
|------------|----------|----------|
| GBT-C5A | robotiq_2f_140 | `gbt-c5a/Gripper/robotiq_2f_140.usd` |
| GBT-C7A | robotiq_2f_140 | `gbt-c7a/Gripper/robotiq_2f_140.usd` |
| GBT-C12A | robotiq_2f_140 | `gbt-c12a/Gripper/robotiq_2f_140.usd` |
| GBT-C16A | robotiq_2f_140 | `gbt-c16a/Gripper/robotiq_2f_140.usd` |

### 通过 Python API 切换夹爪 Variant

在 Isaac Sim / Isaac Lab 中，可通过 USD Python API 动态切换夹爪配置：

```python
# 启用 Robotiq 2F-140 夹爪
robot.GetVariantSet("Gripper").SetVariantSelection("robotiq_2f_140")

# 不使用夹爪（裸法兰）
robot.GetVariantSet("Gripper").SetVariantSelection("None")
```

该方式适用于：

* 不同任务下的末端执行器切换
* 夹爪 / 工具的快速对比测试
* 强化学习或批量仿真中的自动配置

---

## 💡 小贴士

### 夹爪抓取问题

如果在抓取操作时遇到**夹爪穿模、掉落**的问题，可以尝试以下调整：

1. **降低夹爪最大力**：将最大力降低到个位数（例如 1-5 N），以减少抓取力度
2. **大幅降低降低物理仿真帧率**：将物理仿真帧率降低到默认的60FPS，以减少计算负担
    ```
    world = World(stage_units_in_meters=1.0, physics_dt=1/60.0)
    ```

这些调整有助于防止夹爪施加过大的力导致物体穿透，但都可能带来其他的抓取问题，请根据你的使用场景动态调整

---

## 📦 夹爪模型来源说明

夹爪模型来源于开源项目：
[robotiq_2f_gripper](https://github.com/gen-robot/robotiq_2f_gripper/tree/main/robotiq_2f_140_gripper_visualization)

该模型仅用于仿真与示例用途，其版权归原作者所有。

夹爪导入与组装流程参考 NVIDIA 官方文档：
[Isaac Sim 机器人导入与组装教程](https://docs.isaacsim.omniverse.nvidia.com/latest/robot_setup_tutorials/tutorial_import_assemble_manipulator.html)

---

## 🖥️ 实验环境

**测试环境：**

- **系统**：Ubuntu 22.04
- **GPU**：NVIDIA RTX 5090
- **Isaac Sim 版本**：5.1.0-rc.19+release.26219.9c81211b.gl
- **Isaac Lab 版本**：2.3.0

---

## 🚀 使用方法

### 在 Isaac Sim 中使用

当前版本提供标准化 USD 资产文件，可直接通过 Isaac Sim 的 USD Loader 或 Reference 方式加载。
Isaac Sim 的完整示例工程将在后续版本中提供。

### 在 Isaac Lab 中使用

当前版本可作为 Isaac Lab 中 `Articulation` 或自定义资产的输入。
相关任务配置与示例将另行发布。

---

## ⚠️ 物理参数说明

**重要提示：**

所有机器人型号的关节自然频率和阻尼参数均已配置为 Isaac Sim 推荐的经验值：

- **活动关节**：自然频率 = 300，阻尼 = 0.005
- **联动关节**：自然频率 = 2500，阻尼 = 0.005

这些值基于 Isaac Sim 官方推荐，并已通过测试可减少机器人仿真时出现的乱飞、晃动等问题。

关于质量和方向惯量：
- **GBT-C5A**：由捷勃特公司手动计算
- **其他机型（GBT-C7A、GBT-C12A、GBT-C16A）**：由 SolidWorks 或 Isaac Sim 自动生成

请根据具体的仿真任务需求手动调整上述参数，以确保仿真行为的准确性。

---

## 🤝 贡献指南

欢迎通过 Issue 与 Pull Request 参与本仓库的维护与改进。

### 贡献流程

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/AmazingFeature`
3. 提交修改：`git commit -m "Add some AmazingFeature"`
4. 推送到远程分支：`git push origin feature/AmazingFeature`
5. 创建 Pull Request

---

## 📄 许可证

本项目采用 **BSD 3-Clause License**，详见 [LICENSE](LICENSE)。

---

## 📞 联系方式

* **商务咨询**：[info@agilebot.com.cn](mailto:info@agilebot.com.cn)
* **技术支持**：400-996-7588
* **官方网站**：[https://www.sh-agilebot.com/](https://www.sh-agilebot.com/)

---

## 🙏 致谢

感谢 [NVIDIA Isaac Sim](https://developer.nvidia.com/isaac-sim) 和 [Isaac Lab](https://isaac-sim.github.io/IsaacLab/) 团队提供的优秀机器人仿真平台。

特别感谢 [Robotiq](https://robotiq.com/) 提供的开源夹爪模型，为我们的机器人资产增添了更多灵活性和实用性。

感谢 [奥比中光](https://www.orbbec3d.com/) 提供的 Femto Mega 相机，为视觉引导机器人应用提供了支持。

感谢 [MetaIsaacGrasp](https://github.com/YitianShi/MetaIsaacGrasp) 提供的相机支架设计，该设计基于 MIT 许可证使用。

有关第三方许可证的详细信息，请参考 [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md)。

---

## 📋 更新日志

详细的版本历史和变更记录，请参考 [CHANGELOG_zh.md](CHANGELOG_zh.md)。

---

## 🗺️ 后续计划

未来的开发计划包括：

### 工业机器人机型
- [ ] GBT-S3A - 3kg 负载工业 SCARA 机器人
- [ ] GBT-S6A - 6kg 负载工业 SCARA 机器人
- [ ] GBT-S10A - 10kg 负载工业 SCARA 机器人
- [ ] GBT-S20A - 20kg 负载工业 SCARA 机器人
- [ ] GBT-P7A - 7kg 负载工业 PUMA 机器人


### 物理参数
- [ ] 为 GBT-C7A 提供默认物理参数
- [ ] 为 GBT-C12A 提供默认物理参数
- [ ] 为 GBT-C16A 提供默认物理参数

---

## 🏢 关于 Agilebot Robotics

上海捷勃特机器人有限公司是一家专业的工业机器人和智能磁驱输送系统提供商。公司以"驱动未来工厂"为愿景，依托先进的驱控一体控制技术，为客户提供高性能、高品质、高性价比、高易用性的机器人产品。

产品线涵盖协作机器人、工业六轴机器人与 SCARA 机器人，广泛应用于装配、搬运、检测等工业场景。

* **官方网站**：[https://www.sh-agilebot.com/](https://www.sh-agilebot.com/)
* **商务邮箱**：[info@agilebot.com.cn](mailto:info@agilebot.com.cn)
* **联系电话**：400-996-7588

---

© 2026 Agilebot Robotics. All rights reserved.
