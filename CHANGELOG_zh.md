# 更新日志

本项目的所有重要变更都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/spec/v2.0.0.html)。

## [0.0.1] - 2026-01-04

### 新增
- Agilebot Robotics USD 资产库首次发布
- 支持 GBT-C5A 协作机器人（5 kg 负载，850 mm 臂展）
- 支持 GBT-C7A 协作机器人（7 kg 负载）
- 支持 GBT-C12A 协作机器人（12 kg 负载）
- 支持 GBT-C16A 协作机器人（16 kg 负载）
- 所有机器人型号的完整物理配置
- 所有机器人型号的完整传感器配置
- USD VariantSet 集成，支持夹爪切换
- 所有机器人型号的 Robotiq 2F-140 夹爪变体
- 所有机器人型号的材质和纹理资源
- 双语文档（中文和英文）

### 文档
- 包含项目概述的全面 README
- 机器人型号规格和功能说明
- 夹爪配置和变体切换指南
- 物理参数说明和使用指南
- Isaac Sim 和 Isaac Lab 集成说明
- 贡献指南和许可信息
- 包含计划机器人型号的未来路线图

### 致谢
- NVIDIA Isaac Sim 团队提供的仿真平台
- Isaac Lab 团队提供的机器人框架
- Robotiq 提供的开源夹爪模型

---

## [0.0.2] - 2026-01-05

### 新增
- 添加 GBT-C5A 机器人+Robotiq 夹爪+奥比中光 Femto Mega 相机集成模型
- 添加集成模型的完整文档，包括使用指南和技术规格
- 添加第三方组件许可证文档（THIRD_PARTY_LICENSES.md）

### 优化
- 更新所有机器人型号的关节自然频率和阻尼参数为 Isaac Sim 官方推荐经验值（活动关节：300，联动关节：2500，阻尼：0.005）
- 更新所有机器人型号（GBT-C5A、GBT-C7A、GBT-C12A、GBT-C16A）的物理参数，包括质量、惯量和关节驱动参数
- 更新物理参数文档，明确质量和方向惯量的来源（所有机型：由捷勃特手动计算）

### 文档
- 增强 README 文档，添加集成模型的详细信息
- 添加集成模型 README，包含组件规格、使用指南和 Python API 示例
- 添加第三方组件许可证文档，包含所有第三方组件的完整许可证信息
- 更新物理参数说明，准确反映所有机器人型号的配置情况

### 修复
- 修复 CHANGELOG 中的格式问题（移除优化部分的换行符）

---

## [0.0.3] - 2026-02-03

### 修复
- 修复 gbt-c5a_camera_gripper 模型纹理丢失的问题

---

## [0.0.4] - 2026-03-09

### 移除
- **移除 Robotiq 2F-140 夹爪 USD 资产** - 由于版权不确定性，从所有机器人型号（GBT-C5A、GBT-C7A、GBT-C12A、GBT-C16A）中移除了所有 Robotiq 2F-140 夹爪相关的 USD 文件
- **移除 gbt-c5a_camera_gripper 集成模型** - 由于第三方版权问题，移除了包含机器人夹爪和奥比中光 Femto Mega 相机的集成模型目录

### 新增
- 新增夹爪抓取问题排查文档（`docs/gripper_troubleshooting_zh.md`），提供针对 Isaac Sim 5.1 的系统化排查步骤

### 变更
- 更新所有机器人型号主 USD 文件，移除夹爪变体引用
- 更新 README_zh.md，移除 Robotiq 夹爪相关内容及文档

---

## [0.0.5] - 2026-03-12

### 新增
- 新增 `gbt-c5a_wrist_camera_gripper` 组合模型目录，提供 GBT-C5A 机械臂、Robotiq 2F-140 夹爪和手腕相机安装位的 URDF 工作流
- 新增中文使用文档，说明用户需自行将夹爪相关 URDF 转换为 USD，并在转换后的机器人 USD 上挂载腕部相机

### 说明
- 夹爪部分仅提供 URDF 集成方案，不发布转换后的 Robotiq 夹爪 USD 资产
- 腕部相机支架模型为 AI 辅助生成，仅作为演示用途

---

## [0.0.6] - 2026-03-17

### 修复
- 修正 `gbt-c5a_wrist_camera_gripper/urdf/gbt-c5a_wrist_camera_gripper.urdf` 中错误的质量与惯量参数，提升导入质量和物理稳定性

### 文档
- 在 `gbt-c5a_wrist_camera_gripper/README.zh-CN.md` 中新增 Isaac Sim 版本兼容性提示，说明若导入后出现腕部夹爪组件分离或行为异常，建议优先使用 Isaac Sim 5.0

---

## [0.0.7] - 2026-03-26

### 变更
- 更新 gbt-c5a_wrist_camera_gripper 工作流：移除 `add_online_camera_usd.py`，新增 `convert_urdf_to_usd.py` 和 `remove_camera_rect_light.py`，改进 URDF 转 USD 流程

### 文档
- 更新 gbt-c5a_wrist_camera_gripper 的 README 和 README.zh-CN.md

---

## [0.0.8] - 2026-03-30

### 新增
- 新增碰撞体同步功能到 `convert_urdf_to_usd.py` - 自动为机器人 link 添加碰撞几何体
- README 新增 Miniforge 环境激活说明

### 变更
- 重构 `convert_urdf_to_usd.py` - 将 `remove_camera_rect_light.py` 功能合并到 postprocess 步骤中
- 移除独立的 `remove_camera_rect_light.py` 脚本
- postprocess 现在固定执行：相机挂载 + 删除 RectLight + 碰撞体补齐 + physics layer 更新（不再有 `--skip-camera` 或 `--skip-physics` 选项）
- 更新 `gbt-c5a_wrist_camera_gripper.urdf` 参数

### 文档
- 更新 gbt-c5a_wrist_camera_gripper 的 README.md 和 README.zh-CN.md，包含新工作流和碰撞体同步说明

---

## [未发布]

### 计划中
- 添加工业 SCARA 机器人（GBT-S3A、GBT-S6A、GBT-S10A、GBT-S20A）
- 添加工业 PUMA 机器人（GBT-P7A）
