# GBT C5A Wrist Camera Gripper

[English README](README.md)

本仓库提供一个组合 URDF，包含 GBT C5A 机械臂、腕部相机安装支架和 Robotiq 2F-140 夹爪，并提供一套面向 Isaac Sim 的脚本化 USD 生成流程。

本文档只保留脚本方式，不再介绍 GUI 导入或手工挂载步骤，目的是让开源用户能够复现同一套流程。

## 仓库结构

- `urdf/gbt-c5a_wrist_camera_gripper.urdf`：组合机器人 URDF
- `meshes/visual/`：URDF 使用的可视化网格
- `meshes/collision/`：URDF 使用的碰撞网格
- `scripts/setup_robotiq_meshes.sh`：把所需 Robotiq STL 安装到本仓库
- `scripts/convert_urdf_to_usd.py`：负责 URDF 导入、相机挂载、删除相机 `RectLight`、碰撞体补齐和 physics layer 更新
- `urdf/gbt-c5a_wrist_camera_gripper/`：导入后生成的 USD 输出目录

## 前置条件

- Isaac Sim 或 Isaac Lab 的 Python 环境
- 你已经从合法来源准备好 Robotiq 2F-140 STL 文件

请注意：

- 本仓库不分发 Robotiq STL 资源。
- `scripts/convert_urdf_to_usd.py` 不是普通 Python 脚本，它依赖 `isaacsim`、`isaaclab`、`omni.kit.commands`、`pxr` 等 Isaac 运行时模块。
- 相机后处理默认通过远程资产 URL 挂载 Orbbec Gemini2 相机。默认流程要求当前环境能够访问该远程资源。

如果你是通过 Miniforge 管理 Isaac Lab 环境，建议先激活环境再执行下面所有命令：

```bash
source ~/miniforge3/bin/activate isaaclab
```

如果你的 Miniforge 安装路径不是 `~/miniforge3`，请改成你自己的实际路径。

## 快速开始

1. 安装所需 Robotiq 网格：
>https://github.com/ros-industrial-attic/robotiq/tree/kinetic-devel/robotiq_2f_140_gripper_visualization
```bash
bash scripts/setup_robotiq_meshes.sh /path/to/robotiq_stl_dir
```

需要准备的 STL 文件：

- `robotiq_arg2f_base_link.stl`
- `robotiq_arg2f_coupling.stl`
- `robotiq_arg2f_140_outer_knuckle.stl`
- `robotiq_arg2f_140_outer_finger.stl`
- `robotiq_arg2f_140_inner_knuckle.stl`
- `robotiq_arg2f_140_inner_finger.stl`

2. 在 Isaac Sim 或 Isaac Lab 的 Python 环境中运行导入脚本：

推荐直接使用这条一键命令，它把当前项目默认建议保留的参数都显式写出来，便于复现：

```bash
python scripts/convert_urdf_to_usd.py \
  urdf/gbt-c5a_wrist_camera_gripper.urdf \
  urdf/gbt-c5a_wrist_camera_gripper/gbt-c5a_wrist_camera_gripper.usd \
  --drive-type force \
  --arm-natural-frequency 300.0 \
  --gripper-natural-frequency 300.0 \
  --mimic-natural-frequency 2500.0 \
  --damping-ratio 0.005 \
  --finger-max-force 200.0 \
  --solver-position-iterations 64 \
  --solver-velocity-iterations 16
```

这套推荐参数会：

- 以 headless 模式运行
- 保持 `fix_base=true`
- 保持 `merge_fixed_joints=false`
- 导入完成后自动挂载相机、补齐碰撞体，并更新 physics layer
- 会在后处理阶段自动去掉相机自带灯光

```bash
python scripts/convert_urdf_to_usd.py
```

默认情况下，这条命令会：

- 读取 `urdf/gbt-c5a_wrist_camera_gripper.urdf`
- 生成 `urdf/gbt-c5a_wrist_camera_gripper/gbt-c5a_wrist_camera_gripper.usd`
- 以 headless 模式运行
- 保持 `fix_base=true`
- 保持 `merge_fixed_joints=false`
- 在导入完成后自动执行后处理，包括挂载相机、补齐碰撞体，以及更新 physics layer
- 会在后处理阶段自动去掉相机 `RectLight`

## 脚本工作流

显式指定输入 URDF 和输出 USD：

```bash
python scripts/convert_urdf_to_usd.py \
  urdf/gbt-c5a_wrist_camera_gripper.urdf \
  urdf/gbt-c5a_wrist_camera_gripper/gbt-c5a_wrist_camera_gripper.usd
```

对已有 USD 单独执行后处理：

```bash
python scripts/convert_urdf_to_usd.py postprocess \
  urdf/gbt-c5a_wrist_camera_gripper/gbt-c5a_wrist_camera_gripper.usd
```

后处理会固定执行相机挂载、删除相机 `RectLight`、碰撞体补齐，以及附近 physics layer 更新。

不给 URDF 重新导入，单独给已有 USD 补碰撞体：

```bash
python scripts/convert_urdf_to_usd.py postprocess \
  urdf/gbt-c5a_wrist_camera_gripper/gbt-c5a_wrist_camera_gripper.usd
```

碰撞体编辑会自动切到附近的 `*_physics.usd` layer，并优先在 `/colliders` 下查找碰撞几何体。碰撞体补齐始终开启，并固定使用脚本内建默认值。

帮助命令：

```bash
python scripts/convert_urdf_to_usd.py --help
python scripts/convert_urdf_to_usd.py postprocess --help
```

## 关键参数

常用导入参数：

- `--no-headless`：导入时显示 Isaac 窗口
- `--no-fix-base`：以浮动底座方式导入
- `--merge-fixed-joints`：不建议对该机器人启用
- `--drive-type force|acceleration`
- `--arm-natural-frequency`
- `--gripper-natural-frequency`
- `--mimic-natural-frequency`
- `--damping-ratio`
- `--finger-max-force`

常用后处理参数：

- `--urdf <path>`：在补 collider 时显式指定 URDF 文件
- `--physics-stage <path>`：显式指定 physics layer
- `--no-remove-camera-rect-light`：保留相机 `RectLight`，不在后处理阶段自动禁用
- `--skip-finger-friction`：跳过手指摩擦材质创建与绑定
- `--skip-articulation-config`：跳过 articulation 求解器参数更新

相机挂载、`RectLight` 删除、碰撞体补齐和 physics layer 更新都固定使用脚本内建工作流默认值。

脚本默认值：

- 机械臂 natural frequency：`300.0`
- 夹爪主动关节 natural frequency：`300.0`
- mimic joints natural frequency：`2500.0`
- damping ratio：`0.02`
- finger max force：`5000.0`
- drive type：`force`
- static friction：`1.2`
- dynamic friction：`1.1`
- restitution：`0.0`
- solver position iterations：`96`
- solver velocity iterations：`8`

## 输出文件

导入成功后，通常会生成这些文件：

- `urdf/gbt-c5a_wrist_camera_gripper/gbt-c5a_wrist_camera_gripper.usd`
- `urdf/gbt-c5a_wrist_camera_gripper/configuration/gbt-c5a_wrist_camera_gripper_base.usd`
- `urdf/gbt-c5a_wrist_camera_gripper/configuration/gbt-c5a_wrist_camera_gripper_physics.usd`
- `urdf/gbt-c5a_wrist_camera_gripper/configuration/gbt-c5a_wrist_camera_gripper_robot.usd`
- `urdf/gbt-c5a_wrist_camera_gripper/configuration/gbt-c5a_wrist_camera_gripper_sensor.usd`

## 验证建议

最少建议完成以下检查：

- 运行 `python3 -m py_compile scripts/convert_urdf_to_usd.py`
- 运行 `python3 scripts/convert_urdf_to_usd.py --help`
- 运行 `python3 scripts/convert_urdf_to_usd.py postprocess --help`
- 确认顶层 USD 已生成
- 确认 physics layer 文件存在
- 在 Isaac Sim 中打开生成的 USD，确认相机视图可用
- 确认 `Stream_rgb` 中能看到夹爪
- 如果 `RectLight` 仍然意外可见，可以重新执行 `scripts/convert_urdf_to_usd.py postprocess`，并确认没有启用 `--no-remove-camera-rect-light`

## 排障说明

- 如果网格安装脚本报错，先检查 6 个 STL 文件名是否完全匹配。
- 如果转换脚本一开始就失败，通常是因为没有在 Isaac Sim 或 Isaac Lab 的 Python 环境中运行。
- 如果相机挂载失败，先检查当前 Isaac Sim 环境是否能访问远程 Orbbec Gemini2 资产。
- 如果导入后仍然能看到相机灯光，请重新运行 `python scripts/convert_urdf_to_usd.py postprocess`，并确认没有启用 `--no-remove-camera-rect-light`。
- 如果后处理阶段找不到 physics layer，请通过 `--physics-stage <path>` 显式传入。
- 如果补碰撞体找不到机器人 link，可以优先重跑 `scripts/convert_urdf_to_usd.py postprocess`，再检查生成出来的 stage 层级。内建补齐逻辑会优先使用附近的 physics layer 和 `/colliders` 路径。
- 不要为该机器人启用 fixed joint merge。保持 `merge_fixed_joints=false` 才能保留预期的相机和夹爪层级。

## 已知限制

- 这套流程依赖 Isaac 运行时模块，不能在通用 Python 环境中完整执行。
- 默认相机引用依赖远程 Isaac 资产可访问。
- Robotiq 资源需要用户自行获取。
- 本文档只覆盖脚本工作流，不包含 GUI 操作说明。
