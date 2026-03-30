# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.1] - 2026-01-04

### Added
- Initial release of Agilebot Robotics USD Assets
- Support for GBT-C5A collaborative robot (5 kg payload, 850 mm reach)
- Support for GBT-C7A collaborative robot (7 kg payload)
- Support for GBT-C12A collaborative robot (12 kg payload)
- Support for GBT-C16A collaborative robot (16 kg payload)
- Complete physics configurations for all robot models
- Complete sensor configurations for all robot models
- USD VariantSet integration for gripper switching
- Robotiq 2F-140 gripper variant for all robot models
- Material and texture resources for all robot models
- Bilingual documentation (English and Chinese)

### Documentation
- Comprehensive README with project overview
- Robot model specifications and features
- Gripper configuration and variant switching guide
- Physics parameters notice and usage guidelines
- Isaac Sim and Isaac Lab integration instructions
- Contribution guidelines and license information
- Future roadmap with planned robot models

### Acknowledgments
- NVIDIA Isaac Sim team for simulation platform
- Isaac Lab team for robotics framework
- Robotiq for open-source gripper model

---

## [0.0.2] - 2026-01-05

### Added
- Added GBT-C5A robot + Robotiq gripper + Orbbec Femto Mega camera integrated model
- Added comprehensive documentation for integrated model including usage guide and technical specifications
- Added third-party licenses documentation (THIRD_PARTY_LICENSES.md)

### Optimized
- Updated all robot models' joint natural frequency and damping parameters to Isaac Sim official recommended empirical values (active joints: 300, linked joints: 2500, damping: 0.005)
- Updated physics parameters for all robot models (GBT-C5A, GBT-C7A, GBT-C12A, GBT-C16A), including mass, inertia, and joint drive parameters
- Updated physics parameters documentation to clarify mass and directional inertia sources (all models: manually calculated by Agilebot)

### Documentation
- Enhanced README with detailed integrated model information
- Added integrated model README with component specifications, usage guide, and Python API examples
- Added third-party licenses documentation with complete license information for all third-party components
- Updated physics parameters notice to reflect accurate configuration across all robot models

### Fixed
- Fixed formatting issues in CHANGELOG (removed line breaks in Optimized section)

---

## [0.0.3] - 2026-02-03

### Fixed
- Fixed texture loss issue for gbt-c5a_camera_gripper model

---

## [0.0.4] - 2026-03-09

### Removed
- **Removed Robotiq 2F-140 gripper USD assets** - Due to copyright uncertainty, removed all Robotiq 2F-140 gripper related USD files from all robot models (GBT-C5A, GBT-C7A, GBT-C12A, GBT-C16A)
- **Removed gbt-c5a_camera_gripper integrated model** - Removed the integrated model directory containing Robot gripper and Orbbec Femto Mega camera due to third-party copyright concerns

### Added
- Added gripper grasping troubleshooting documentation (`docs/gripper_troubleshooting_zh.md`) with systematic diagnosis steps for Isaac Sim 5.1

### Changed
- Updated all robot model main USD files to remove gripper variant references
- Updated README_zh.md to remove Robotiq gripper references and related documentation

---

## [0.0.5] - 2026-03-12

### Added
- Added the `gbt-c5a_wrist_camera_gripper` composite model directory, providing a URDF workflow for the GBT-C5A arm, Robotiq 2F-140 gripper, and wrist camera mounting point
- Added changelog and Chinese usage documentation clarifying that users must convert the gripper-related URDF into USD themselves and attach the wrist camera onto the generated robot USD

### Notes
- The gripper is provided only as a URDF integration workflow; converted Robotiq gripper USD assets are not distributed
- The wrist camera mount model was AI-assisted and is provided for demonstration only

---

## [0.0.6] - 2026-03-17

### Fixed
- Corrected incorrect mass and inertia parameters in `gbt-c5a_wrist_camera_gripper/urdf/gbt-c5a_wrist_camera_gripper.urdf` to improve import quality and physical stability

### Documentation
- Added Isaac Sim version compatibility notes to `gbt-c5a_wrist_camera_gripper/README.md`, including a recommendation to use Isaac Sim 5.0 if the wrist gripper assembly separates or behaves abnormally after import

---

## [0.0.7] - 2026-03-26

### Changed
- Updated gbt-c5a_wrist_camera_gripper workflow: removed `add_online_camera_usd.py`, added `convert_urdf_to_usd.py` and `remove_camera_rect_light.py` for improved URDF-to-USD conversion pipeline

### Documentation
- Updated README and README.zh-CN.md for gbt-c5a_wrist_camera_gripper

---

## [0.0.8] - 2026-03-30

### Added
- Added collider sync functionality to `convert_urdf_to_usd.py` - automatically adds collision geometry to robot links
- Added Miniforge environment activation instructions to README

### Changed
- Refactored `convert_urdf_to_usd.py` - merged `remove_camera_rect_light.py` functionality directly into postprocess step
- Removed standalone `remove_camera_rect_light.py` script
- Postprocess now always runs: camera attachment + RectLight removal + collider sync + physics update (no more `--skip-camera` or `--skip-physics` options)
- Updated `gbt-c5a_wrist_camera_gripper.urdf` parameters

### Documentation
- Updated README.md and README.zh-CN.md for gbt-c5a_wrist_camera_gripper with new workflow and collider sync instructions

---

## [Unreleased]

### Planned
- Add industrial SCARA robots (GBT-S3A, GBT-S6A, GBT-S10A, GBT-S20A)
- Add industrial PUMA robot (GBT-P7A)
