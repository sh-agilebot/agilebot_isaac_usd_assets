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
- Updated physics parameters documentation to clarify mass and directional inertia sources (GBT-C5A: manually calculated by Agilebot, other models: automatically generated)

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

## [Unreleased]

### Planned
- Add industrial SCARA robots (GBT-S3A, GBT-S6A, GBT-S10A, GBT-S20A)
- Add industrial PUMA robot (GBT-P7A)
- Provide default physics parameters for GBT-C7A
- Provide default physics parameters for GBT-C12A
- Provide default physics parameters for GBT-C16A
- Isaac Sim example projects
- Isaac Lab task configurations and examples