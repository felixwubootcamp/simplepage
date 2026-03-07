# vSphere VM Automation Starter

This repository scaffold helps automate VM provisioning in VMware vSphere using a YAML machine definition.

## What it automates

- CPU and RAM sizing
- Storage (single or multiple disks)
- Network/VLAN selection via portgroup mapping
- Guest OS profile metadata
- VM naming and template selection

## Structure

- `vm-spec.example.yaml` – Example VM request file
- `provision_vm.py` – CLI that loads and validates VM specs, then builds an execution plan
- `requirements.txt` – Python dependencies

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp vm-spec.example.yaml vm-spec.yaml
python provision_vm.py --spec vm-spec.yaml --dry-run
```

## Next steps for real provisioning

1. Create a vSphere service account with least privilege.
2. Add environment variables for credentials:
   - `VSPHERE_SERVER`
   - `VSPHERE_USERNAME`
   - `VSPHERE_PASSWORD`
3. Replace the `build_execution_plan()` calls with real pyVmomi tasks:
   - clone from template
   - reconfigure CPU/RAM
   - attach disks
   - connect NIC(s) to target portgroup(s)
   - set guest customization spec

## Notes

- `--dry-run` is enabled by default when you're experimenting.
- The starter intentionally separates parsing/validation from execution, so you can plug in Terraform, Ansible, or pyVmomi later.
