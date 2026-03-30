# GBT C5A Wrist Camera Gripper

[中文说明 / Chinese](README.zh-CN.md)

This repository provides a combined URDF for the GBT C5A arm, a wrist camera mount, and a Robotiq 2F-140 gripper, plus a script-first workflow for generating USD assets for Isaac Sim.

The documented workflow in this repository is script-only. GUI import steps are intentionally omitted so the process stays reproducible for open-source users.

## Repository Layout

- `urdf/gbt-c5a_wrist_camera_gripper.urdf`: combined robot URDF
- `meshes/visual/`: visual meshes used by the URDF
- `meshes/collision/`: collision meshes used by the URDF
- `scripts/setup_robotiq_meshes.sh`: installs the required Robotiq STL files into this repository
- `scripts/convert_urdf_to_usd.py`: imports the URDF, attaches the camera USD, removes the camera `RectLight`, adds collider APIs, and updates the physics layer
- `urdf/gbt-c5a_wrist_camera_gripper/`: generated USD outputs after import

## Prerequisites

- Isaac Sim or Isaac Lab Python environment
- Robotiq 2F-140 STL files from a lawful source

Important notes:

- This repository does not redistribute Robotiq STL assets.
- `scripts/convert_urdf_to_usd.py` is not a plain Python utility. It depends on Isaac runtime modules such as `isaacsim`, `isaaclab`, `omni.kit.commands`, and `pxr`.
- The camera postprocess step adds the Orbbec Gemini2 USD by remote asset URL. Your environment must be able to access that asset for the default workflow to succeed.

If you manage Isaac Lab with Miniforge, activate that environment before running any commands below:

```bash
source ~/miniforge3/bin/activate isaaclab
```

If your Miniforge installation lives somewhere else, replace `~/miniforge3` with the actual path.

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
- automatically attaches the camera, adds colliders, and updates the physics layer
- removes the camera light automatically during postprocess

```bash
python scripts/convert_urdf_to_usd.py
```

By default, this command:

- reads `urdf/gbt-c5a_wrist_camera_gripper.urdf`
- writes `urdf/gbt-c5a_wrist_camera_gripper/gbt-c5a_wrist_camera_gripper.usd`
- runs headless
- keeps `fix_base=true`
- keeps `merge_fixed_joints=false`
- automatically runs postprocess to attach the camera, add colliders, and update the physics layer
- removes the camera `RectLight` automatically during postprocess

## Script Workflow

Generate USD with explicit input and output paths:

```bash
python scripts/convert_urdf_to_usd.py \
  urdf/gbt-c5a_wrist_camera_gripper.urdf \
  urdf/gbt-c5a_wrist_camera_gripper/gbt-c5a_wrist_camera_gripper.usd
```

Postprocess an existing USD stage:

```bash
python scripts/convert_urdf_to_usd.py postprocess \
  urdf/gbt-c5a_wrist_camera_gripper/gbt-c5a_wrist_camera_gripper.usd
```

Postprocess always attaches the camera, removes the camera `RectLight`, adds colliders, and updates the nearby physics layer.

Add colliders to an existing USD stage without re-running URDF import:

```bash
python scripts/convert_urdf_to_usd.py postprocess \
  urdf/gbt-c5a_wrist_camera_gripper/gbt-c5a_wrist_camera_gripper.usd
```

Collider edits always redirect to the nearby `*_physics.usd` layer when one exists and prefer `/colliders` as the search root. Collider sync is always enabled and uses the built-in defaults.

Useful help commands:

```bash
python scripts/convert_urdf_to_usd.py --help
python scripts/convert_urdf_to_usd.py postprocess --help
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

- `--urdf <path>`: use an explicit URDF file when syncing colliders
- `--physics-stage <path>`: use an explicit physics layer
- `--no-remove-camera-rect-light`: keep the camera `RectLight` instead of deactivating it
- `--skip-finger-friction`: skip finger material creation and binding
- `--skip-articulation-config`: skip articulation solver tuning

Camera attachment, `RectLight` removal, collider sync, and physics-layer updates always run with the built-in workflow defaults.

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
- run `python3 scripts/convert_urdf_to_usd.py --help`
- run `python3 scripts/convert_urdf_to_usd.py postprocess --help`
- confirm the top-level USD was generated
- confirm the physics layer exists
- open the USD in Isaac Sim and check that the camera view is available
- confirm the gripper is visible in `Stream_rgb`
- if the camera `RectLight` still appears unexpectedly, rerun `scripts/convert_urdf_to_usd.py postprocess` with `--no-remove-camera-rect-light` omitted and confirm the light prim is inactive

## Troubleshooting

- If the mesh setup script fails, verify that all 6 required STL files exist with the exact expected filenames.
- If the conversion script fails immediately, make sure you are running it inside an Isaac Sim or Isaac Lab Python environment.
- If camera attachment fails, verify that your Isaac Sim environment can access the remote Orbbec Gemini2 asset.
- If the camera light is still visible after import, rerun `python scripts/convert_urdf_to_usd.py postprocess` and make sure `--no-remove-camera-rect-light` is not set.
- If the script cannot find the physics layer during postprocess, rerun with `--physics-stage <path>`.
- If collider sync cannot find your robot links, rerun `scripts/convert_urdf_to_usd.py postprocess` and inspect the generated stage hierarchy. The built-in sync always prefers the nearby physics layer and `/colliders` when present.
- Do not enable fixed-joint merging for this robot. Keeping `merge_fixed_joints=false` preserves the expected camera and gripper hierarchy.

## Known Limitations

- The workflow depends on Isaac runtime modules and cannot be fully executed in a generic Python environment.
- The default camera asset reference depends on remote Isaac asset availability.
- Robotiq assets must be obtained separately by the user.
- The documented workflow is script-only; GUI steps are intentionally not covered here.
