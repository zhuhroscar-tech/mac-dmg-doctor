[![English](https://img.shields.io/badge/English-555555?style=flat)](README.md) [![简体中文](https://img.shields.io/badge/简体中文-555555?style=flat)](README.zh-CN.md)

# mac-dmg-doctor

`mac-dmg-doctor` 已迁移到 [`mac-volume-doctor`](https://github.com/zhuhroscar-tech/mac-volume-doctor)，作为统一的 macOS 卷弹出诊断套件的一部分。

原来的 DMG / resource-busy 功能现在可通过以下命令使用：

```bash
mac-volume-doctor dmg scan
mac-volume-doctor dmg inspect "/Volumes/My Image"
mac-volume-doctor dmg --json scan
```

为了兼容旧用法，安装 `mac-volume-doctor` 后仍会提供原命令名：

```bash
mac-dmg-doctor scan
```

此仓库已作为迁移指引归档。新安装、修复和 issue 请使用 `mac-volume-doctor`。

## 迁移

```bash
git clone https://github.com/zhuhroscar-tech/mac-volume-doctor.git
cd mac-volume-doctor
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[test]"
```

迁移后的检查仍然是只读的：它读取 `mount`、`lsof` 和 `hdiutil info`，不会终止进程、强制卸载卷或分离磁盘映像。

[mac-volume-doctor](https://github.com/zhuhroscar-tech/mac-volume-doctor) · [MIT 许可证](LICENSE)
