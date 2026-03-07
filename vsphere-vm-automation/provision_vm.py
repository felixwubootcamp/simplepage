#!/usr/bin/env python3
"""vSphere VM provisioning starter CLI.

This script reads a VM spec from YAML, validates required fields,
and prints an execution plan. Hook the final plan to pyVmomi tasks.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


REQUIRED_FIELDS = [
    "vm.name",
    "vm.datacenter",
    "vm.cluster",
    "vm.datastore",
    "vm.template",
    "hardware.cpu",
    "hardware.memory_mb",
    "network.nics",
    "os.type",
    "os.hostname",
]


class SpecValidationError(ValueError):
    """Raised when a VM specification file is invalid."""


def _get_nested(spec: dict[str, Any], key_path: str) -> Any:
    current: Any = spec
    for part in key_path.split('.'):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def load_spec(spec_path: Path) -> dict[str, Any]:
    with spec_path.open('r', encoding='utf-8') as file:
        data = yaml.safe_load(file)

    if not isinstance(data, dict):
        raise SpecValidationError('Spec must be a YAML object at root level.')

    return data


def validate_spec(spec: dict[str, Any]) -> None:
    missing = [field for field in REQUIRED_FIELDS if _get_nested(spec, field) in (None, "")]
    if missing:
        raise SpecValidationError(f"Missing required fields: {', '.join(missing)}")

    nics = _get_nested(spec, "network.nics")
    if not isinstance(nics, list) or len(nics) == 0:
        raise SpecValidationError("network.nics must contain at least one NIC definition")

    disks = _get_nested(spec, "hardware.disks")
    if disks is not None and not isinstance(disks, list):
        raise SpecValidationError("hardware.disks must be a list if provided")


def build_execution_plan(spec: dict[str, Any]) -> list[dict[str, Any]]:
    vm = spec["vm"]
    hardware = spec["hardware"]
    network = spec["network"]
    os_cfg = spec["os"]

    plan = [
        {
            "step": "clone_vm",
            "from_template": vm["template"],
            "target_name": vm["name"],
            "datacenter": vm["datacenter"],
            "cluster": vm["cluster"],
            "datastore": vm["datastore"],
            "folder": vm.get("folder", "/"),
        },
        {
            "step": "configure_compute",
            "cpu": hardware["cpu"],
            "memory_mb": hardware["memory_mb"],
        },
        {
            "step": "configure_disks",
            "disks": hardware.get("disks", []),
        },
        {
            "step": "configure_network",
            "nics": network["nics"],
        },
        {
            "step": "customize_guest_os",
            "os_type": os_cfg["type"],
            "hostname": os_cfg["hostname"],
            "domain": os_cfg.get("domain"),
            "timezone": os_cfg.get("timezone", "UTC"),
            "customization_spec": os_cfg.get("customization_spec"),
        },
        {
            "step": "power_on",
            "enabled": True,
        },
    ]
    return plan


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="vSphere VM provisioning starter")
    parser.add_argument("--spec", required=True, help="Path to VM YAML spec")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print plan only (recommended for initial use)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    spec_path = Path(args.spec)

    if not spec_path.exists():
        raise FileNotFoundError(f"Spec file does not exist: {spec_path}")

    spec = load_spec(spec_path)
    validate_spec(spec)
    plan = build_execution_plan(spec)

    print("Execution plan:")
    print(json.dumps(plan, indent=2))

    if not args.dry_run:
        print("\nNOTE: Real vSphere API execution is not implemented in this starter yet.")
        print("Hook build_execution_plan output into pyVmomi task functions.")


if __name__ == "__main__":
    main()
