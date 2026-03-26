# GBT C5A Wrist Camera Gripper

[中文说明 / Chinese](README.zh-CN.md)

This repository provides a combined URDF for the GBT C5A arm, a wrist camera mount, and a Robotiq 2F-140 gripper, plus a script-first workflow for generating USD assets for Isaac Sim.

The documented workflow in this repository is script-only. GUI import steps are intentionally omitted so the process stays reproducible for open-source users.

## Repository Layout

- `urdf/gbt-c5a_wrist_camera_gripper.urdf`: combined robot URDF
- `meshes/visual/`: visual meshes used by the URDF
- `meshes/collision/`: collision meshes used by the URDF
- `scripts/setup_robotiq_meshes.sh`: installs the required Robotiq STL files into this repository
- `scripts/convert_urdf_to_usd.py`: imports the URDF, attaches the camera USD, and updates the physics layer
- `scripts/remove_camera_rect_light.py`: deactivates the `RectLight` prim under the attached Orbbec Gemini2 camera
- `urdf/gbt-c5a_wrist_camera_gripper/`: generated USD outputs after import

## Prerequisites

- Isaac Sim or Isaac Lab Python environment
- Robotiq 2F-140 STL files from a lawful source

Important notes:

- This repository does not redistribute Robotiq STL assets.
- `scripts/convert_urdf_to_usd.py` is not a plain Python utility. It depends on Isaac runtime modules such as `isaacsim`, `isaaclab`, `omni.kit.commands`, and `pxr`.
- `scripts/remove_camera_rect_light.py` must also run inside an Isaac Sim, Isaac Lab, or other `pxr`-enabled Python environment.
- The camera postprocess step adds the Orbbec Gemini2 USD by remote asset URL. If that remote asset is unavailable in your environment, run the workflow with `--skip-camera`.

## Quick Start

1. Install the required Robotiq meshes:

```bash
bash scripts/setup_robotiq_meshes.sh /path/to/robotiq_stl_dir
```

Required STL files:

- `robotiq_arg2f_base_link.stl`
- `robotiq_arg2f_coupling.stl`
- `robotiq_arg2f_140_outer_knuckle.stl`
- `robotiq_arg2f_140_outer_finger.stl`
- `robotiq_arg2f_140_inner_knuckle.stl`
- `robotiq_arg2f_140_inner_finger.stl`

2. Run the scripted import inside an Isaac Sim or Isaac Lab Python environment:

Recommended one-shot command: this makes the current project-recommended parameters explicit so the result is easier to reproduce.

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

This recommended command:

- runs headless
- keeps `fix_base=true`
- keeps `merge_fixed_joints=false`
- automatically attaches the camera and updates the physics layer
- if you want to hide the camera light, run `python scripts/remove_camera_rect_light.py` after import

```bash
python scripts/convert_urdf_to_usd.py
```

By default, this command:

- reads `urdf/gbt-c5a_wrist_camera_gripper.urdf`
- writes `urdf/gbt-c5a_wrist_camera_gripper/gbt-c5a_wrist_camera_gripper.usd`
- runs headless
- keeps `fix_base=true`
- keeps `merge_fixed_joints=false`
- automatically runs postprocess to attach the camera and update the physics layer
- does not remove the camera `RectLight` unless you run `scripts/remove_camera_rect_light.py`

## Script Workflow

Generate USD with explicit input and output paths:

```bash
python scripts/convert_urdf_to_usd.py \
  urdf/gbt-c5a_wrist_camera_gripper.urdf \
  urdf/gbt-c5a_wrist_camera_gripper/gbt-c5a_wrist_camera_gripper.usd
```

Import only, without camera or physics postprocess:

```bash
python scripts/convert_urdf_to_usd.py --skip-camera --skip-physics
```

Postprocess an existing USD stage:

```bash
python scripts/convert_urdf_to_usd.py postprocess \
  urdf/gbt-c5a_wrist_camera_gripper/gbt-c5a_wrist_camera_gripper.usd
```

Remove the `RectLight` under the attached Orbbec camera:

```bash
python scripts/remove_camera_rect_light.py \
  urdf/gbt-c5a_wrist_camera_gripper/gbt-c5a_wrist_camera_gripper.usd
```

Useful help commands:

```bash
python scripts/convert_urdf_to_usd.py --help
python scripts/convert_urdf_to_usd.py postprocess --help
python scripts/remove_camera_rect_light.py --help
```

## Key Options

Common import options:

- `--no-headless`: show the Isaac app window during import
- `--no-fix-base`: import the robot with a floating base
- `--merge-fixed-joints`: not recommended for this robot
- `--drive-type force|acceleration`
- `--arm-natural-frequency`
- `--gripper-natural-frequency`
- `--mimic-natural-frequency`
- `--damping-ratio`
- `--finger-max-force`

Common postprocess options:

- `--skip-camera`: skip camera attachment
- `--skip-physics`: skip physics-layer updates
- `--physics-stage <path>`: use an explicit physics layer
- `--skip-finger-friction`: skip finger material creation and binding
- `--skip-articulation-config`: skip articulation solver tuning

Default script values:

- arm natural frequency: `300.0`
- gripper natural frequency: `300.0`
- mimic natural frequency: `2500.0`
- damping ratio: `0.02`
- finger max force: `5000.0`
- drive type: `force`
- static friction: `1.2`
- dynamic friction: `1.1`
- restitution: `0.0`
- solver position iterations: `96`
- solver velocity iterations: `8`

## Outputs

After a successful import, the generated files usually include:

- `urdf/gbt-c5a_wrist_camera_gripper/gbt-c5a_wrist_camera_gripper.usd`
- `urdf/gbt-c5a_wrist_camera_gripper/configuration/gbt-c5a_wrist_camera_gripper_base.usd`
- `urdf/gbt-c5a_wrist_camera_gripper/configuration/gbt-c5a_wrist_camera_gripper_physics.usd`
- `urdf/gbt-c5a_wrist_camera_gripper/configuration/gbt-c5a_wrist_camera_gripper_robot.usd`
- `urdf/gbt-c5a_wrist_camera_gripper/configuration/gbt-c5a_wrist_camera_gripper_sensor.usd`

## Validation

Minimum validation after changes:

- run `python3 -m py_compile scripts/convert_urdf_to_usd.py`
- run `python3 -m py_compile scripts/remove_camera_rect_light.py`
- confirm the top-level USD was generated
- confirm the physics layer exists
- open the USD in Isaac Sim and check that the camera view is available
- confirm the gripper is visible in `Stream_rgb`
- if `scripts/remove_camera_rect_light.py` was used, confirm the `RectLight` is inactive or no longer visible in the stage

## Troubleshooting

- If the mesh setup script fails, verify that all 6 required STL files exist with the exact expected filenames.
- If the conversion script fails immediately, make sure you are running it inside an Isaac Sim or Isaac Lab Python environment.
- If camera attachment fails, verify that your Isaac Sim environment can access the remote Orbbec Gemini2 asset. If not, rerun with `--skip-camera`.
- If the camera light is still visible after import, run `python scripts/remove_camera_rect_light.py`. If your stage uses a different prim hierarchy, rerun with `--prim-path <path>`.
- If the script cannot find the physics layer during postprocess, rerun with `--physics-stage <path>`.
- Do not enable fixed-joint merging for this robot. Keeping `merge_fixed_joints=false` preserves the expected camera and gripper hierarchy.

## Known Limitations

- The workflow depends on Isaac runtime modules and cannot be fully executed in a generic Python environment.
- The default camera asset reference depends on remote Isaac asset availability.
- Robotiq assets must be obtained separately by the user.
- The documented workflow is script-only; GUI steps are intentionally not covered here.
