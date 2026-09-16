[![English](https://img.shields.io/badge/English-555555?style=flat)](README.md) [![简体中文](https://img.shields.io/badge/简体中文-555555?style=flat)](README.zh-CN.md)

# mac-dmg-doctor

A read-only macOS CLI for investigating “Resource busy” errors when ejecting DMGs or other mounted volumes. It lists processes with open references and prints next-step guidance so you can close applications normally before retrying an eject.

The tool does **not** kill processes, detach disk images, or force-unmount volumes. Any suggested `hdiutil detach` command is text for you to review, not an action it performs.

## Install

Requires macOS, Python 3.8+, and the system tools `mount`, `lsof`, and `hdiutil`. There are no third-party Python runtime dependencies.

```bash
git clone https://github.com/zhuhroscar-tech/mac-dmg-doctor.git
cd mac-dmg-doctor
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

## Quick start

```bash
mac-dmg-doctor scan
mac-dmg-doctor inspect "/Volumes/My Image"
mac-dmg-doctor --json scan
mac-dmg-doctor --json inspect "/Volumes/My Image"
```

`--json` is a global option: place it **before** `scan` or `inspect`. With no subcommand, the CLI defaults to scanning.

- `scan` reads mounts under `/Volumes/` and reports those with detected open processes.
- `inspect` checks one path and includes device information when it matches a known mount point, process names/PIDs, and recommendations.
- `hdiutil info` supplies image-path hints where the parser can correlate them.

After closing a listed application, rerun `inspect` and try a normal eject in Finder. Verify the device identifier before following any manual detach suggestion.

## Limitations and safety

Inspection uses recursive `lsof +D`, which can be slow on large directory trees. Its query times out after five seconds. Missing tools, permission restrictions, failed commands, and timeouts can result in empty process lists; **“no busy mount points detected” is not a guarantee that a volume is safe to detach**.

The displayed open-handle count is actually a count of deduplicated command/PID entries, not individual file descriptors. Image-path correlation is best-effort. Diagnostic commands normally return `0`, including when blockers are found, so inspect the report rather than using the exit code as a busy/idle signal.

The application only reads system state and does not write files or change mount state. Reports can contain local paths and process names; review them before sharing.

## Preview and development

[Example output](docs/images/example-output.png) · [Demo video](docs/demo.mp4)

```bash
python -m pip install pytest
python -m pytest -v
```

[Implementation](src/mac_dmg_doctor/cli.py) · [Tests](tests/test_cli.py) · [MIT license](LICENSE)
