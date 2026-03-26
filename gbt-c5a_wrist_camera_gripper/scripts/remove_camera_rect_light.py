#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_STAGE_PATH = Path("urdf/gbt-c5a_wrist_camera_gripper/gbt-c5a_wrist_camera_gripper.usd")
DEFAULT_STAGE_NAME = DEFAULT_STAGE_PATH.name
DEFAULT_ROBOT_ROOT_NAME = "GBT_C5A_wrist_camera_gripper"
DEFAULT_CAMERA_LINK_CANDIDATES = (
    "/camera_link",
    "/camera_mount_link/camera_link",
)
DEFAULT_LIGHT_RELATIVE_PATH = "/Orbbec_Gemini2/camera_ldm/camera_ldm/RectLight"


def import_usd_modules():
    from pxr import Usd

    return Usd


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


def normalize_prim_path(prim_path: str) -> str:
    return prim_path if prim_path.startswith("/") else f"/{prim_path}"


def resolve_robot_root_path(stage) -> str:
    preferred_candidates = (
        f"/{DEFAULT_ROBOT_ROOT_NAME}",
        f"/World/{DEFAULT_ROBOT_ROOT_NAME}",
    )
    for prim_path in preferred_candidates:
        if stage.GetPrimAtPath(prim_path).IsValid():
            return prim_path

    default_prim = stage.GetDefaultPrim()
    if default_prim and default_prim.IsValid():
        if default_prim.GetName() == DEFAULT_ROBOT_ROOT_NAME:
            return str(default_prim.GetPath())

        robot_child = default_prim.GetChild(DEFAULT_ROBOT_ROOT_NAME)
        if robot_child and robot_child.IsValid():
            return str(robot_child.GetPath())

    matches = [str(prim.GetPath()) for prim in stage.Traverse() if prim.GetName() == DEFAULT_ROBOT_ROOT_NAME]
    if matches:
        for prim_path in matches:
            if prim_path.startswith(f"/{DEFAULT_ROBOT_ROOT_NAME}"):
                return prim_path
        return matches[0]

    return f"/{DEFAULT_ROBOT_ROOT_NAME}"


def resolve_camera_link_path(stage, robot_root_path: str) -> str:
    for relative_path in DEFAULT_CAMERA_LINK_CANDIDATES:
        prim_path = f"{robot_root_path}{relative_path}"
        if stage.GetPrimAtPath(prim_path).IsValid():
            return prim_path

    matches = [str(prim.GetPath()) for prim in stage.Traverse() if prim.GetName() == "camera_link"]
    if matches:
        for prim_path in matches:
            if prim_path.startswith(f"{robot_root_path}/"):
                return prim_path
        return matches[0]

    return f"{robot_root_path}{DEFAULT_CAMERA_LINK_CANDIDATES[0]}"


def resolve_light_prim_path(stage, explicit_prim_path: str | None) -> str:
    if explicit_prim_path:
        return normalize_prim_path(explicit_prim_path)
    robot_root_path = resolve_robot_root_path(stage)
    camera_link_path = resolve_camera_link_path(stage, robot_root_path)
    return f"{camera_link_path}{DEFAULT_LIGHT_RELATIVE_PATH}"


def deactivate_prim(stage, prim_path: str) -> tuple[bool, str]:
    prim = stage.GetPrimAtPath(prim_path)
    existed_in_composed_stage = prim.IsValid()

    # Author an inactive over so the referenced light disappears from the composed stage.
    override = stage.OverridePrim(prim_path)
    if not override.IsValid():
        raise RuntimeError(f"Failed to create override prim for {prim_path}")
    override.SetActive(False)

    root_layer = stage.GetRootLayer()
    root_layer.Save()
    return existed_in_composed_stage, root_layer.realPath or root_layer.identifier


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Deactivate the Orbbec Gemini2 RectLight prim in the generated robot USD stage."
    )
    parser.add_argument("stage", nargs="?", default=None, help="Top-level robot USD stage path.")
    parser.add_argument(
        "--prim-path",
        default=None,
        help=(
            "Explicit light prim path to deactivate. "
            f"Default: auto-detect the robot root and use {DEFAULT_LIGHT_RELATIVE_PATH}."
        ),
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    try:
        stage_path = existing_stage_path(args.stage)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr, flush=True)
        return 1

    if not stage_path.exists():
        print(f"Stage file not found: {stage_path}", file=sys.stderr, flush=True)
        return 1

    try:
        Usd = import_usd_modules()
    except ModuleNotFoundError as exc:
        print(
            "Missing USD Python modules. Run this script inside an Isaac Sim / Isaac Lab / pxr-enabled Python environment: "
            f"{exc}",
            file=sys.stderr,
            flush=True,
        )
        return 1

    stage = Usd.Stage.Open(str(stage_path))
    if stage is None:
        print(f"Failed to open USD stage: {stage_path}", file=sys.stderr, flush=True)
        return 1

    prim_path = resolve_light_prim_path(stage, args.prim_path)
    existed_in_composed_stage, saved_layer = deactivate_prim(stage, prim_path)

    print(f"Stage: {stage_path}", flush=True)
    print(f"RectLight prim path: {prim_path}", flush=True)
    if existed_in_composed_stage:
        print("Result: deactivated existing RectLight prim in the composed stage.", flush=True)
    else:
        print(
            "Result: authored an inactive over for the RectLight prim path. "
            "This is expected if the light only exists through a referenced camera asset.",
            flush=True,
        )
    print(f"Saved layer: {saved_layer}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
