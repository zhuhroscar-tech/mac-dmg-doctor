[![English](https://img.shields.io/badge/English-555555?style=flat)](README.md) [![简体中文](https://img.shields.io/badge/简体中文-555555?style=flat)](README.zh-CN.md)

# mac-dmg-doctor

`mac-dmg-doctor` has moved into [`mac-volume-doctor`](https://github.com/zhuhroscar-tech/mac-volume-doctor), the consolidated macOS volume-eject diagnostic suite.

The original DMG/resource-busy functionality is now available as:

```bash
mac-volume-doctor dmg scan
mac-volume-doctor dmg inspect "/Volumes/My Image"
mac-volume-doctor dmg --json scan
```

For compatibility, installing `mac-volume-doctor` also provides the legacy command name:

```bash
mac-dmg-doctor scan
```

This repository is archived as a migration pointer. Use `mac-volume-doctor` for new installs, fixes, and issues.

## Migration

```bash
git clone https://github.com/zhuhroscar-tech/mac-volume-doctor.git
cd mac-volume-doctor
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
```

The migrated check remains read-only: it inspects `mount`, `lsof`, and `hdiutil info`; it does not kill processes, force-unmount volumes, or detach disk images.

[mac-volume-doctor](https://github.com/zhuhroscar-tech/mac-volume-doctor) · [MIT license](LICENSE)
