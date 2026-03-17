# GBT C5A Wrist Camera Gripper

[中文说明 / Chinese](README.zh-CN.md)

This repository packages a combined URDF for the GBT C5A arm, wrist camera mount, and Robotiq 2F-140 gripper, plus helper scripts for Isaac Sim import and camera attachment.

Recommended first-time workflow:

1. Install the Robotiq STL files required by the URDF.
2. Import `urdf/gbt-c5a_wrist_camera_gripper.urdf` in Isaac Sim.
3. Generate the robot USD with the Isaac Sim GUI importer and configure joint drives.
4. Attach the online camera USD to `camera_link` manually or with the helper script.

## Repository Layout

- `urdf/gbt-c5a_wrist_camera_gripper.urdf`: Combined robot URDF.
- `urdf/gbt-c5a_wrist_camera_gripper/`: Generated USD and configuration layers after import.
- `meshes/visual/`: Visual meshes for the arm, camera mount, and copied Robotiq STL files.
- `meshes/collision/`: Collision meshes and copied Robotiq STL files.
- `scripts/setup_robotiq_meshes.sh`: Copies the required Robotiq STL files into this repository.
- `scripts/convert_urdf_to_usd.py`: Experimental scripted import path. Useful for reference, not the recommended workflow.
- `scripts/add_online_camera_usd.py`: Adds the online camera USD under `camera_link`.

## 1. Install the Required Robotiq STL Files

### Copyright Notice

- This repository does not redistribute Robotiq STL assets.
- Download the Robotiq 2F-140 STL files yourself from a legitimate source.

Reference source:

- `https://github.com/ros-industrial-attic/robotiq`

### Required STL Files

Prepare these 6 files:

- `robotiq_arg2f_base_link.stl`
- `robotiq_arg2f_coupling.stl`
- `robotiq_arg2f_140_outer_knuckle.stl`
- `robotiq_arg2f_140_outer_finger.stl`
- `robotiq_arg2f_140_inner_knuckle.stl`
- `robotiq_arg2f_140_inner_finger.stl`

### One-Command Setup

After downloading the STL files into a local directory, run:

```bash
bash scripts/setup_robotiq_meshes.sh /path/to/robotiq_stl_dir
```

The script copies the files into:

- `meshes/visual/`
- `meshes/collision/`

After that, `urdf/gbt-c5a_wrist_camera_gripper.urdf` is ready for import.

## 2. URDF Structure Overview

The URDF already includes the wrist camera mount and gripper assembly. Before import, you only need to make sure all required meshes are present.

Key links and joints:

- Arm joints: `joint1` to `joint6`
- Camera mount fixed joint: `camera_mount_joint`
- Camera attach point: `camera_link`
- Gripper fixed joint: `gripper_joint`
- Gripper active joint: `finger_joint`
- Gripper mimic joints: `left_inner_knuckle_joint`, `left_inner_finger_joint`, `right_outer_knuckle_joint`, `right_inner_knuckle_joint`, `right_inner_finger_joint`

The online camera USD is attached to `camera_link` in the final step.

## 3. Import the URDF into Isaac Sim

The recommended workflow is the Isaac Sim GUI importer. `scripts/convert_urdf_to_usd.py` is kept as an experimental alternative and should not be the default path.

### Compatibility Note

- If the imported USD shows the wrist gripper assembly separating from the arm or behaving abnormally, try importing with Isaac Sim 5.0.
- In local testing, the same URDF/USD workflow worked normally in Isaac Sim 5.0 and did not reproduce this issue.

### Import Entry

Open the URDF Importer in Isaac Sim and use:

- Input file: `urdf/gbt-c5a_wrist_camera_gripper.urdf`
- Output file: `urdf/gbt-c5a_wrist_camera_gripper/gbt-c5a_wrist_camera_gripper.usd`

### Recommended Joint Drive Settings

Focus on `Joints & Drives` during import.

- Arm joints `joint1` to `joint6`: `Target = Position`, `Natural Frequency = 300`
- Gripper active joint `finger_joint`: `Target = Position`, `Natural Frequency = 300`
- Gripper mimic joints: `Natural Frequency = 2500`

Also verify:

- `Joint Configuration = Natural Frequency`
- `Drive Type = Force`

Keep Isaac Sim default damping unless the gripper later feels too soft.

Reference images:

- `docs/images/isaacsim_urdf_import_joint_settings.png`
- `docs/images/isaacsim_manual_drag_camera.png`

![Isaac Sim URDF import joint settings](docs/images/isaacsim_urdf_import_joint_settings.png)

### Expected Generated Files

After import, the following files should exist:

- `urdf/gbt-c5a_wrist_camera_gripper/gbt-c5a_wrist_camera_gripper.usd`
- `urdf/gbt-c5a_wrist_camera_gripper/configuration/gbt-c5a_wrist_camera_gripper_base.usd`
- `urdf/gbt-c5a_wrist_camera_gripper/configuration/gbt-c5a_wrist_camera_gripper_physics.usd`
- `urdf/gbt-c5a_wrist_camera_gripper/configuration/gbt-c5a_wrist_camera_gripper_robot.usd`
- `urdf/gbt-c5a_wrist_camera_gripper/configuration/gbt-c5a_wrist_camera_gripper_sensor.usd`

## 4. Attach the Online Camera USD

Recommended camera asset:

- `Isaac/Sensors/Orbbec/Gemini2/orbbec_gemini2_v1.0.usd`

### Manual Method

In Isaac Sim:

1. Open `Isaac/5.1/Isaac/Sensors/Orbbec/Gemini2/` in `Content` or `Asset Browser`.
2. Find `orbbec_gemini2_v1.0.usd`.
3. Find `camera_link` in `Stage`.
4. Drag the camera USD under `camera_link`.

Common `camera_link` prim paths:

- `/GBT_C5A_wrist_camera_gripper/camera_mount_link/camera_link`
- `/World/GBT_C5A_wrist_camera_gripper/camera_mount_link/camera_link`

![Isaac Sim manual drag camera USD](docs/images/isaacsim_manual_drag_camera.png)

### Script Method

Run inside an Isaac Sim or Isaac Lab Python environment:

```bash
python scripts/add_online_camera_usd.py
```

To specify the target stage explicitly:

```bash
python scripts/add_online_camera_usd.py urdf/gbt-c5a_wrist_camera_gripper/gbt-c5a_wrist_camera_gripper.usd
```

The script:

- Finds the target USD stage
- Resolves `camera_link`
- Adds `orbbec_gemini2_v1.0.usd` as a reference under that prim
- Removes older legacy camera references if they exist

## 5. Verify the Camera Attachment

After attaching the camera USD to `camera_link`, verify it visually in Isaac Sim.

1. Load `gbt-c5a_wrist_camera_gripper.usd`.
2. Open the camera menu in the viewport.
3. Expand `Cameras` and switch to `Stream_rgb`.
4. Confirm that the gripper is visible.

Success criteria:

- `Stream_rgb` can be selected normally
- The image is not black or empty
- The gripper is visible in the RGB view

If the gripper is not visible, check:

- The camera USD is actually attached under `camera_link`
- The pose of `camera_link` was not modified accidentally
- You selected the RGB stream rather than depth or infrared

![Isaac Sim verify RGB camera view](docs/images/isaacsim_verify_rgb_camera_view.png)

## 6. Checklist

At minimum, the full workflow should leave you with:

- The 6 required Robotiq STL files copied into `meshes/visual/` and `meshes/collision/`
- A successful Isaac Sim import of `urdf/gbt-c5a_wrist_camera_gripper.urdf`
- Recommended `Natural Frequency` settings applied during import
- `urdf/gbt-c5a_wrist_camera_gripper/gbt-c5a_wrist_camera_gripper.usd` generated
- The online camera USD attached to `camera_link`
- A visible gripper in `Stream_rgb`

## 7. References

- URDF Importer Extension:
  `https://docs.isaacsim.omniverse.nvidia.com/5.1.0/importer_exporter/ext_isaacsim_asset_importer_urdf.html`
- Setup a Manipulator:
  `https://docs.isaacsim.omniverse.nvidia.com/5.1.0/robot_setup_tutorials/tutorial_import_assemble_manipulator.html`
