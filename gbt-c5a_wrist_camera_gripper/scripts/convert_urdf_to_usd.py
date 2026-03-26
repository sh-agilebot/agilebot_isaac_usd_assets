#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Sequence


REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_URDF_PATH = Path("urdf/gbt-c5a_wrist_camera_gripper.urdf")
DEFAULT_STAGE_PATH = Path("urdf/gbt-c5a_wrist_camera_gripper/gbt-c5a_wrist_camera_gripper.usd")
DEFAULT_STAGE_NAME = DEFAULT_STAGE_PATH.name
DEFAULT_PHYSICS_STAGE_NAME = "gbt-c5a_wrist_camera_gripper_physics.usd"

ARM_JOINT_PATTERN = r"^joint[1-6]$"
FINGER_JOINT_PATTERN = r"^finger_joint$"
MIMIC_JOINT_PATTERN = (
    r"^(left_inner_knuckle_joint|left_inner_finger_joint|right_outer_knuckle_joint|"
    r"right_inner_knuckle_joint|right_inner_finger_joint)$"
)
POSITION_JOINT_PATTERNS = (ARM_JOINT_PATTERN, FINGER_JOINT_PATTERN)

DEFAULT_ARM_NATURAL_FREQUENCY = 300.0
DEFAULT_GRIPPER_NATURAL_FREQUENCY = 300.0
DEFAULT_MIMIC_NATURAL_FREQUENCY = 2500.0
DEFAULT_DAMPING_RATIO = 0.02
DEFAULT_FINGER_MAX_FORCE = 5000.0
DEFAULT_DRIVE_TYPE = "force"
DEFAULT_HEADLESS = True
DEFAULT_FIX_BASE = True
DEFAULT_MERGE_FIXED_JOINTS = False

DEFAULT_CAMERA_PRIM_CANDIDATES = (
    "/GBT_C5A_wrist_camera_gripper/camera_mount_link/camera_link",
    "/World/GBT_C5A_wrist_camera_gripper/camera_mount_link/camera_link",
)
DEFAULT_CAMERA_ASSET_URL = (
    "https://omniverse-content-production.s3-us-west-2.amazonaws.com/"
    "Assets/Isaac/5.1/Isaac/Sensors/Orbbec/Gemini2/orbbec_gemini2_v1.0.usd"
)
LEGACY_CAMERA_URLS = {
    "https://omniverse-content-production.s3-us-west-2.amazonaws.com/"
    "Assets/Isaac/5.1/Isaac/Sensors/Orbbec/Gemini%202/orbbec_gemini2_V1.0.usd",
    DEFAULT_CAMERA_ASSET_URL,
}

DEFAULT_STATIC_FRICTION = 1.2
DEFAULT_DYNAMIC_FRICTION = 1.1
DEFAULT_RESTITUTION = 0.0
DEFAULT_FINGER_MATERIAL_NAME = "finger_physics_material"
DEFAULT_SOLVER_POSITION_ITERATIONS = 96
DEFAULT_SOLVER_VELOCITY_ITERATIONS = 8
DEFAULT_SLEEP_THRESHOLD = 0.00005
DEFAULT_STABILIZATION_THRESHOLD = 0.00001

DEFAULT_FINGER_BIND_TARGET_CANDIDATES = {
    "left": (
        "/colliders/left_inner_finger/mesh_1/box",
        "/colliders/left_inner_finger/robotiq_arg2f_140_inner_finger/mesh",
        "/GBT_C5A_wrist_camera_gripper/left_inner_finger/collisions/mesh_1/box",
        "/GBT_C5A_wrist_camera_gripper/left_inner_finger/collisions/robotiq_arg2f_140_inner_finger/mesh",
    ),
    "right": (
        "/colliders/right_inner_finger/mesh_1/box",
        "/colliders/right_inner_finger/robotiq_arg2f_140_inner_finger/mesh",
        "/GBT_C5A_wrist_camera_gripper/right_inner_finger/collisions/mesh_1/box",
        "/GBT_C5A_wrist_camera_gripper/right_inner_finger/collisions/robotiq_arg2f_140_inner_finger/mesh",
    ),
}
GEOM_TYPE_NAMES = {"Mesh", "Cube", "Capsule", "Cylinder", "Sphere", "Box"}


def import_usd_modules():
    from pxr import Sdf, Usd, UsdGeom, UsdPhysics, UsdShade

    return Sdf, Usd, UsdGeom, UsdPhysics, UsdShade


def resolve_repo_path(value: str | Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (REPO_ROOT / path).resolve()


def existing_stage_path(value: str | None) -> Path:
    if value:
        return resolve_repo_path(value)

    preferred = resolve_repo_path(DEFAULT_STAGE_PATH)
    if preferred.exists():
        return preferred

    candidates = sorted(REPO_ROOT.rglob(DEFAULT_STAGE_NAME))
    if not candidates:
        raise FileNotFoundError(f"Could not find existing USD stage named {DEFAULT_STAGE_NAME}")
    return candidates[0].resolve()


def existing_physics_stage_path(stage_path: Path, explicit_path: str | None) -> Path:
    if explicit_path:
        return resolve_repo_path(explicit_path)

    preferred = (stage_path.parent / "configuration" / DEFAULT_PHYSICS_STAGE_NAME).resolve()
    if preferred.exists():
        return preferred

    derived_name = f"{stage_path.stem}_physics.usd"
    candidates = sorted(stage_path.parent.rglob(derived_name))
    if candidates:
        return candidates[0].resolve()

    candidates = sorted(stage_path.parent.rglob("*_physics.usd"))
    if not candidates:
        raise FileNotFoundError(f"Could not find a physics USD layer near {stage_path}")
    return candidates[0].resolve()


def iter_matching_joints(robot_model, pattern: str):
    for joint_name, joint in robot_model.joints.items():
        if re.search(pattern, joint_name):
            yield joint_name, joint


def natural_frequency_map(args: argparse.Namespace) -> dict[str, float]:
    return {
        ARM_JOINT_PATTERN: args.arm_natural_frequency,
        FINGER_JOINT_PATTERN: args.gripper_natural_frequency,
        MIMIC_JOINT_PATTERN: args.mimic_natural_frequency,
    }


def max_force_map(args: argparse.Namespace) -> dict[str, float]:
    return {FINGER_JOINT_PATTERN: args.finger_max_force}


def configure_joint_drives(robot_model, urdf_interface, args: argparse.Namespace) -> set[str]:
    from isaacsim.asset.importer.urdf._urdf import UrdfJointDriveType, UrdfJointTargetType

    drive_type = {
        "force": UrdfJointDriveType.JOINT_DRIVE_FORCE,
        "acceleration": UrdfJointDriveType.JOINT_DRIVE_ACCELERATION,
    }[args.drive_type]
    configured_joint_names = set()

    for pattern in POSITION_JOINT_PATTERNS:
        for joint_name, joint in iter_matching_joints(robot_model, pattern):
            joint.drive.set_target_type(UrdfJointTargetType.JOINT_DRIVE_POSITION)
            configured_joint_names.add(joint_name)

    for pattern, natural_frequency in natural_frequency_map(args).items():
        for joint_name, joint in iter_matching_joints(robot_model, pattern):
            joint.drive.natural_frequency = natural_frequency
            joint.drive.damping_ratio = args.damping_ratio
            joint.drive.set_drive_type(drive_type)
            joint.drive.strength = urdf_interface.compute_natural_stiffness(
                robot_model,
                joint.name,
                joint.drive.natural_frequency,
            )

            equivalent_inertia = 1.0
            if joint.drive.target_type == UrdfJointTargetType.JOINT_DRIVE_POSITION:
                if joint.drive.drive_type == UrdfJointDriveType.JOINT_DRIVE_FORCE:
                    equivalent_inertia = joint.inertia
                joint.drive.damping = (
                    2.0 * equivalent_inertia * joint.drive.natural_frequency * joint.drive.damping_ratio
                )

            configured_joint_names.add(joint_name)
            print(
                f"Configured {joint_name}: target=position, natural_frequency={joint.drive.natural_frequency}, "
                f"damping_ratio={joint.drive.damping_ratio}, strength={joint.drive.strength}, "
                f"damping={joint.drive.damping}, drive_type={args.drive_type}",
                flush=True,
            )

    untouched_joint_names = sorted(set(robot_model.joints) - configured_joint_names)
    if untouched_joint_names:
        print("Left unchanged:", ", ".join(untouched_joint_names), flush=True)
    return configured_joint_names


def matching_override(pattern_map: dict[str, float], joint_name: str) -> float | None:
    for pattern, value in pattern_map.items():
        if re.search(pattern, joint_name):
            return value
    return None


def apply_drive_overrides(usd_path: Path, joint_names: set[str], args: argparse.Namespace) -> None:
    _, Usd, _, UsdPhysics, _ = import_usd_modules()

    stage = Usd.Stage.Open(str(usd_path))
    if stage is None:
        raise RuntimeError(f"Failed to reopen generated USD for drive overrides: {usd_path}")

    default_prim = stage.GetDefaultPrim()
    if not default_prim.IsValid():
        raise RuntimeError(f"Generated USD has no default prim: {usd_path}")

    force_overrides = max_force_map(args)
    for joint_name in sorted(joint_names):
        joint_path = f"{default_prim.GetPath()}/joints/{joint_name}"
        joint_prim = stage.GetPrimAtPath(joint_path)
        if not joint_prim.IsValid():
            raise RuntimeError(f"Missing joint prim after import: {joint_path}")

        drive = UsdPhysics.DriveAPI.Get(joint_prim, "angular") or UsdPhysics.DriveAPI.Get(joint_prim, "linear")
        if not drive:
            raise RuntimeError(f"Missing drive API after import: {joint_path}")

        max_force = matching_override(force_overrides, joint_name)
        if max_force is not None:
            drive.GetMaxForceAttr().Set(max_force)
            print(f"Overrode {joint_name} maxForce={max_force}", flush=True)

        print(
            f"Verified {joint_name}: stiffness={drive.GetStiffnessAttr().Get()}, "
            f"damping={drive.GetDampingAttr().Get()}, maxForce={drive.GetMaxForceAttr().Get()}, "
            f"type={drive.GetTypeAttr().Get()}",
            flush=True,
        )

    stage.Save()


def ensure_prim(stage, prim_path: str):
    _, _, UsdGeom, _, _ = import_usd_modules()
    prim = stage.GetPrimAtPath(prim_path)
    if prim.IsValid():
        return prim
    return UsdGeom.Xform.Define(stage, prim_path).GetPrim()


def resolve_camera_prim_path(stage) -> str:
    for prim_path in DEFAULT_CAMERA_PRIM_CANDIDATES:
        if stage.GetPrimAtPath(prim_path).IsValid():
            return prim_path

    matches = [str(prim.GetPath()) for prim in stage.Traverse() if prim.GetName() == "camera_link"]
    if not matches:
        return DEFAULT_CAMERA_PRIM_CANDIDATES[0]
    if len(matches) == 1:
        return matches[0]

    for prim_path in matches:
        if prim_path.startswith("/GBT_C5A_wrist_camera_gripper/"):
            return prim_path
    return matches[0]


def camera_asset_path() -> str:
    return DEFAULT_CAMERA_ASSET_URL


def list_reference_assets(prim) -> list[str]:
    refs = prim.GetMetadata("references")
    if refs is None:
        return []
    return [ref.assetPath for ref in refs.prependedItems]


def add_camera_reference(stage_path: Path) -> None:
    Sdf, Usd, _, _, _ = import_usd_modules()

    stage = Usd.Stage.Open(str(stage_path))
    if stage is None:
        raise RuntimeError(f"Failed to open stage: {stage_path}")

    prim = ensure_prim(stage, resolve_camera_prim_path(stage))
    for asset_path in list_reference_assets(prim):
        if asset_path in LEGACY_CAMERA_URLS:
            prim.GetReferences().RemoveReference(Sdf.Reference(asset_path))
            print(f"Removed legacy reference: {asset_path}", flush=True)

    target_asset_path = camera_asset_path()
    if target_asset_path in list_reference_assets(prim):
        print(f"Reference already exists on {prim.GetPath()}", flush=True)
        print(f"Asset path: {target_asset_path}", flush=True)
        return

    prim.GetReferences().AddReference(target_asset_path)
    stage.Save()
    print(f"Added reference to {target_asset_path}", flush=True)
    print(f"Target prim: {prim.GetPath()}", flush=True)
    print(f"Saved stage: {stage_path}", flush=True)


def find_default_prim(stage):
    default_prim = stage.GetDefaultPrim()
    if default_prim and default_prim.IsValid():
        return default_prim

    root_children = [child for child in stage.GetPseudoRoot().GetChildren() if child.IsActive()]
    if not root_children:
        raise RuntimeError("Could not determine a default prim for the USD stage.")
    return root_children[0]


def find_articulation_root_prim(stage):
    root_prim = find_default_prim(stage)
    articulation_prims = []

    for prim in stage.Traverse():
        schemas = prim.GetAppliedSchemas()
        if "PhysxArticulationAPI" in schemas or "PhysicsArticulationRootAPI" in schemas:
            articulation_prims.append(prim)

    if not articulation_prims:
        return root_prim

    root_path = str(root_prim.GetPath())
    for prim in articulation_prims:
        prim_path = str(prim.GetPath())
        if prim_path == root_path or prim_path.startswith(root_path):
            return prim
    return articulation_prims[0]


def is_bindable_geom(prim) -> bool:
    _, _, UsdGeom, _, _ = import_usd_modules()
    return prim.GetTypeName() in GEOM_TYPE_NAMES or prim.IsA(UsdGeom.Gprim)


def collect_finger_bind_targets(stage) -> list[object]:
    bind_targets = []
    for side in ("left", "right"):
        for prim_path in DEFAULT_FINGER_BIND_TARGET_CANDIDATES[side]:
            prim = stage.GetPrimAtPath(prim_path)
            if prim.IsValid() and is_bindable_geom(prim):
                bind_targets.append(prim)
                break
    return bind_targets


def ensure_finger_physics_material(stage, args: argparse.Namespace):
    _, _, _, UsdPhysics, UsdShade = import_usd_modules()

    material_path = f"{find_default_prim(stage).GetPath()}/Looks/{DEFAULT_FINGER_MATERIAL_NAME}"
    material = UsdShade.Material.Define(stage, material_path)
    physics_material = UsdPhysics.MaterialAPI.Apply(material.GetPrim())
    physics_material.CreateStaticFrictionAttr().Set(args.static_friction)
    physics_material.CreateDynamicFrictionAttr().Set(args.dynamic_friction)
    physics_material.CreateRestitutionAttr().Set(args.restitution)
    return material


def configure_articulation(stage, args: argparse.Namespace) -> None:
    from pxr import PhysxSchema, UsdPhysics

    articulation_prim = find_articulation_root_prim(stage)
    UsdPhysics.ArticulationRootAPI.Apply(articulation_prim)
    articulation_api = PhysxSchema.PhysxArticulationAPI.Apply(articulation_prim)
    articulation_api.CreateSolverPositionIterationCountAttr().Set(args.solver_position_iterations)
    articulation_api.CreateSolverVelocityIterationCountAttr().Set(args.solver_velocity_iterations)
    articulation_api.CreateSleepThresholdAttr().Set(args.sleep_threshold)
    articulation_api.CreateStabilizationThresholdAttr().Set(args.stabilization_threshold)
    print(
        "Configured articulation settings on "
        f"{articulation_prim.GetPath()}: "
        f"solver_position_iterations={args.solver_position_iterations}, "
        f"solver_velocity_iterations={args.solver_velocity_iterations}, "
        f"sleep_threshold={args.sleep_threshold}, "
        f"stabilization_threshold={args.stabilization_threshold}",
        flush=True,
    )


def configure_physics_stage(physics_stage_path: Path, args: argparse.Namespace) -> None:
    _, Usd, _, _, UsdShade = import_usd_modules()

    stage = Usd.Stage.Open(str(physics_stage_path))
    if stage is None:
        raise RuntimeError(f"Failed to open physics stage: {physics_stage_path}")

    if not args.skip_articulation_config:
        configure_articulation(stage, args)

    if not args.skip_finger_friction:
        material = ensure_finger_physics_material(stage, args)
        bind_targets = collect_finger_bind_targets(stage)
        if not bind_targets:
            raise RuntimeError("Could not find gripper finger collider prims to bind.")

        for prim in bind_targets:
            UsdShade.MaterialBindingAPI.Apply(prim).Bind(material, UsdShade.Tokens.weakerThanDescendants, "physics")
            print(f"Bound finger physics material to: {prim.GetPath()}", flush=True)

        print(
            "Configured finger friction material: "
            f"static={args.static_friction}, dynamic={args.dynamic_friction}, restitution={args.restitution}",
            flush=True,
        )

    stage.Save()
    print(f"Saved physics stage: {physics_stage_path}", flush=True)


def run_in_simulation_app(headless: bool, callback) -> None:
    try:
        import omni.kit.commands  # noqa: F401
        from isaacsim.asset.importer.urdf._urdf import acquire_urdf_interface  # noqa: F401
    except ModuleNotFoundError:
        app = launch_simulation_app(headless)
        try:
            warm_up_simulation_app(app)
            print("Simulation app ready", flush=True)
            callback()
        finally:
            app.close()
        return

    callback()


def launch_simulation_app(headless: bool):
    try:
        from isaacsim import SimulationApp

        print("Launching Isaac Sim SimulationApp", flush=True)
        return SimulationApp({"headless": headless})
    except ModuleNotFoundError:
        from isaaclab.app import AppLauncher

        print("Launching Isaac Lab AppLauncher", flush=True)
        launcher = AppLauncher(headless=headless)
        app = launcher.app
        setattr(app, "_app_launcher_owner", launcher)
        return app


def warm_up_simulation_app(app) -> None:
    for _ in range(5):
        app.update()


def pump_kit_updates(count: int = 5) -> None:
    import omni.kit.app

    app = omni.kit.app.get_app()
    for _ in range(count):
        app.update()


def build_postprocess_command(args: argparse.Namespace, usd_path: Path) -> list[str]:
    command = [sys.executable, str(Path(__file__).resolve()), "postprocess", str(usd_path)]
    if args.physics_stage:
        command.extend(["--physics-stage", str(resolve_repo_path(args.physics_stage))])
    if args.skip_camera:
        command.append("--skip-camera")
    if args.skip_physics:
        command.append("--skip-physics")
    if args.skip_finger_friction:
        command.append("--skip-finger-friction")
    if args.skip_articulation_config:
        command.append("--skip-articulation-config")

    command.extend(["--static-friction", str(args.static_friction)])
    command.extend(["--dynamic-friction", str(args.dynamic_friction)])
    command.extend(["--restitution", str(args.restitution)])
    command.extend(["--solver-position-iterations", str(args.solver_position_iterations)])
    command.extend(["--solver-velocity-iterations", str(args.solver_velocity_iterations)])
    command.extend(["--sleep-threshold", str(args.sleep_threshold)])
    command.extend(["--stabilization-threshold", str(args.stabilization_threshold)])
    return command


def build_import_command(args: argparse.Namespace, urdf_path: Path, usd_path: Path) -> list[str]:
    command = [sys.executable, str(Path(__file__).resolve()), str(urdf_path), str(usd_path), "--import-only-internal"]
    command.extend(["--arm-natural-frequency", str(args.arm_natural_frequency)])
    command.extend(["--gripper-natural-frequency", str(args.gripper_natural_frequency)])
    command.extend(["--mimic-natural-frequency", str(args.mimic_natural_frequency)])
    command.extend(["--damping-ratio", str(args.damping_ratio)])
    command.extend(["--finger-max-force", str(args.finger_max_force)])
    command.extend(["--drive-type", args.drive_type])
    command.append("--headless" if args.headless else "--no-headless")
    command.append("--fix-base" if args.fix_base else "--no-fix-base")
    command.append("--merge-fixed-joints" if args.merge_fixed_joints else "--no-merge-fixed-joints")
    return command


def run_import(args: argparse.Namespace) -> int:
    urdf_path = resolve_repo_path(args.urdf)
    usd_path = resolve_repo_path(args.output)
    if not urdf_path.exists():
        print(f"URDF file not found: {urdf_path}", file=sys.stderr)
        return 1

    print(f"Input URDF: {urdf_path}", flush=True)
    print(f"Output USD: {usd_path}", flush=True)

    if not args.import_only_internal:
        import_command = build_import_command(args, urdf_path, usd_path)
        print(f"Running import subprocess: {' '.join(import_command)}", flush=True)
        import_result = subprocess.run(import_command)
        if import_result.returncode != 0:
            return import_result.returncode

        if not args.skip_camera or not args.skip_physics:
            postprocess_command = build_postprocess_command(args, usd_path)
            print(f"Running postprocess subprocess: {' '.join(postprocess_command)}", flush=True)
            postprocess_result = subprocess.run(postprocess_command)
            return postprocess_result.returncode
        return 0

    def callback() -> None:
        print("Starting URDF import", flush=True)
        import omni.kit.commands
        from isaacsim.asset.importer.urdf._urdf import acquire_urdf_interface

        urdf_interface = acquire_urdf_interface()
        print("Acquired URDF interface", flush=True)
        _, import_config = omni.kit.commands.execute("URDFCreateImportConfig")
        print("Created import config", flush=True)
        import_config.set_distance_scale(1.0)
        import_config.set_make_default_prim(True)
        import_config.set_create_physics_scene(True)
        import_config.set_density(0.0)
        import_config.set_convex_decomp(False)
        import_config.set_collision_from_visuals(False)
        import_config.set_fix_base(args.fix_base)
        import_config.set_import_inertia_tensor(True)
        import_config.set_self_collision(False)
        import_config.set_parse_mimic(True)
        import_config.set_replace_cylinders_with_capsules(False)
        import_config.set_merge_fixed_joints(args.merge_fixed_joints)
        import_config.set_default_drive_type(1 if args.drive_type == "force" else 0)
        import_config.set_default_drive_strength(1e3)
        import_config.set_default_position_drive_damping(1e2)

        status, robot_model = omni.kit.commands.execute(
            "URDFParseFile",
            urdf_path=str(urdf_path),
            import_config=import_config,
        )
        print(f"URDFParseFile status={status}", flush=True)
        if not status:
            raise RuntimeError(f"Failed to parse URDF: {urdf_path}")

        configured_joint_names = configure_joint_drives(robot_model, urdf_interface, args)
        usd_path.parent.mkdir(parents=True, exist_ok=True)

        status, _ = omni.kit.commands.execute(
            "URDFImportRobot",
            urdf_path=str(urdf_path),
            urdf_robot=robot_model,
            import_config=import_config,
            dest_path=str(usd_path),
        )
        print(f"URDFImportRobot status={status}", flush=True)
        if not status:
            raise RuntimeError(f"Failed to import URDF into USD: {usd_path}")

        print(f"Generated USD: {usd_path}", flush=True)
        pump_kit_updates()
        apply_drive_overrides(usd_path, configured_joint_names, args)
        pump_kit_updates()
    try:
        run_in_simulation_app(args.headless, callback)
    except Exception as exc:
        print(f"Conversion failed: {exc}", file=sys.stderr, flush=True)
        return 1

    if not usd_path.exists():
        print(f"Conversion finished but USD was not created: {usd_path}", file=sys.stderr, flush=True)
        return 1
    return 0


def run_postprocess_actions(stage_path: Path, physics_stage_path: Path | None, args: argparse.Namespace) -> None:
    if not args.skip_camera:
        print("Adding camera reference", flush=True)
        add_camera_reference(stage_path)

    if not args.skip_physics:
        if physics_stage_path is None:
            physics_stage_path = existing_physics_stage_path(stage_path, args.physics_stage)
        print(f"Updating physics stage: {physics_stage_path}", flush=True)
        configure_physics_stage(physics_stage_path, args)


def run_postprocess(args: argparse.Namespace) -> int:
    try:
        stage_path = existing_stage_path(args.stage)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if not stage_path.exists():
        print(f"Stage file not found: {stage_path}", file=sys.stderr)
        return 1

    physics_stage_path = None
    if not args.skip_physics:
        try:
            physics_stage_path = existing_physics_stage_path(stage_path, args.physics_stage)
        except FileNotFoundError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        if not physics_stage_path.exists():
            print(f"Physics stage file not found: {physics_stage_path}", file=sys.stderr)
            return 1

    try:
        run_in_simulation_app(True, lambda: run_postprocess_actions(stage_path, physics_stage_path, args))
    except Exception as exc:
        print(f"Failed to update USD assets: {exc}", file=sys.stderr, flush=True)
        return 1
    return 0


def add_import_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("urdf", nargs="?", default=str(DEFAULT_URDF_PATH), help="Input URDF path.")
    parser.add_argument("output", nargs="?", default=str(DEFAULT_STAGE_PATH), help="Output USD path.")
    parser.add_argument(
        "--arm-natural-frequency",
        type=float,
        default=DEFAULT_ARM_NATURAL_FREQUENCY,
        help="Natural frequency for arm joints joint1-joint6.",
    )
    parser.add_argument(
        "--gripper-natural-frequency",
        type=float,
        default=DEFAULT_GRIPPER_NATURAL_FREQUENCY,
        help="Natural frequency for finger_joint.",
    )
    parser.add_argument(
        "--mimic-natural-frequency",
        type=float,
        default=DEFAULT_MIMIC_NATURAL_FREQUENCY,
        help="Natural frequency for gripper mimic joints.",
    )
    parser.add_argument(
        "--damping-ratio",
        type=float,
        default=DEFAULT_DAMPING_RATIO,
        help="Damping ratio applied to configured drives.",
    )
    parser.add_argument(
        "--finger-max-force",
        type=float,
        default=DEFAULT_FINGER_MAX_FORCE,
        help="Max force override for finger_joint after import.",
    )
    parser.add_argument(
        "--drive-type",
        choices=("force", "acceleration"),
        default=DEFAULT_DRIVE_TYPE,
        help="Drive type used for configured joints.",
    )
    parser.add_argument(
        "--headless",
        action=argparse.BooleanOptionalAction,
        default=DEFAULT_HEADLESS,
        help="Run Isaac Sim headless. Use --no-headless to show the app window.",
    )
    parser.add_argument(
        "--fix-base",
        action=argparse.BooleanOptionalAction,
        default=DEFAULT_FIX_BASE,
        help="Fix the robot base during import.",
    )
    parser.add_argument(
        "--merge-fixed-joints",
        action=argparse.BooleanOptionalAction,
        default=DEFAULT_MERGE_FIXED_JOINTS,
        help="Merge fixed joints during import.",
    )
    parser.add_argument(
        "--physics-stage",
        default=None,
        help="Optional explicit physics-layer USD path for postprocess.",
    )
    parser.add_argument(
        "--import-only-internal",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    add_postprocess_option_arguments(parser)


def add_postprocess_option_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--skip-camera", action="store_true", help="Do not attach the online camera USD.")
    parser.add_argument("--skip-physics", action="store_true", help="Do not update the physics layer.")
    parser.add_argument(
        "--static-friction",
        type=float,
        default=DEFAULT_STATIC_FRICTION,
        help=f"Static friction for the finger physics material. Default: {DEFAULT_STATIC_FRICTION}.",
    )
    parser.add_argument(
        "--dynamic-friction",
        type=float,
        default=DEFAULT_DYNAMIC_FRICTION,
        help=f"Dynamic friction for the finger physics material. Default: {DEFAULT_DYNAMIC_FRICTION}.",
    )
    parser.add_argument(
        "--restitution",
        type=float,
        default=DEFAULT_RESTITUTION,
        help=f"Restitution for the finger physics material. Default: {DEFAULT_RESTITUTION}.",
    )
    parser.add_argument(
        "--solver-position-iterations",
        type=int,
        default=DEFAULT_SOLVER_POSITION_ITERATIONS,
        help=f"Articulation solver position iteration count. Default: {DEFAULT_SOLVER_POSITION_ITERATIONS}.",
    )
    parser.add_argument(
        "--solver-velocity-iterations",
        type=int,
        default=DEFAULT_SOLVER_VELOCITY_ITERATIONS,
        help=f"Articulation solver velocity iteration count. Default: {DEFAULT_SOLVER_VELOCITY_ITERATIONS}.",
    )
    parser.add_argument(
        "--sleep-threshold",
        type=float,
        default=DEFAULT_SLEEP_THRESHOLD,
        help=f"Articulation sleep threshold. Default: {DEFAULT_SLEEP_THRESHOLD}.",
    )
    parser.add_argument(
        "--stabilization-threshold",
        type=float,
        default=DEFAULT_STABILIZATION_THRESHOLD,
        help=f"Articulation stabilization threshold. Default: {DEFAULT_STABILIZATION_THRESHOLD}.",
    )
    parser.add_argument(
        "--skip-finger-friction",
        action="store_true",
        help="Do not create or bind the gripper finger physics material.",
    )
    parser.add_argument(
        "--skip-articulation-config",
        action="store_true",
        help="Do not update articulation stability settings on the physics layer.",
    )


def add_postprocess_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("stage", nargs="?", default=None, help="Top-level robot USD stage path.")
    parser.add_argument(
        "--physics-stage",
        default=None,
        help="Optional explicit physics-layer USD path.",
    )
    add_postprocess_option_arguments(parser)


def build_postprocess_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Attach the online camera USD and update the generated physics layer."
    )
    add_postprocess_arguments(parser)
    return parser


def build_root_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert the combined URDF into USD and optionally postprocess the generated assets."
    )
    subparsers = parser.add_subparsers(dest="command")

    import_parser = subparsers.add_parser("import", help="Import URDF and generate the robot USD.")
    add_import_arguments(import_parser)

    postprocess_parser = subparsers.add_parser("postprocess", help="Attach camera and update physics settings.")
    add_postprocess_arguments(postprocess_parser)
    return parser


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    argv = list(argv if argv is not None else sys.argv[1:])
    if argv and argv[0] == "postprocess":
        parser = build_root_parser()
        return parser.parse_args(argv)

    parser = argparse.ArgumentParser(
        description="Convert the combined URDF into USD and optionally postprocess the generated assets."
    )
    add_import_arguments(parser)
    args = parser.parse_args(argv)
    args.command = "import"
    return args


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.command == "postprocess":
        return run_postprocess(args)
    return run_import(args)


if __name__ == "__main__":
    raise SystemExit(main())
