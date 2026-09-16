[![English](https://img.shields.io/badge/English-555555?style=flat)](README.md) [![简体中文](https://img.shields.io/badge/简体中文-555555?style=flat)](README.zh-CN.md)

# mac-dmg-doctor

只读的 macOS CLI，用于排查弹出 DMG 或其他已挂载卷时出现的“Resource busy”错误。它列出仍持有打开引用的进程，并给出后续建议，方便你正常关闭应用后再尝试弹出。

工具**不会**终止进程、分离磁盘映像或强制卸载卷。报告中的 `hdiutil detach` 只是供你核对的命令建议，不会自动执行。

## 安装

需要 macOS、Python 3.8+ 和系统工具 `mount`、`lsof`、`hdiutil`。Python 运行时没有第三方依赖。

```bash
git clone https://github.com/zhuhroscar-tech/mac-dmg-doctor.git
cd mac-dmg-doctor
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

## 快速开始

```bash
mac-dmg-doctor scan
mac-dmg-doctor inspect "/Volumes/My Image"
mac-dmg-doctor --json scan
mac-dmg-doctor --json inspect "/Volumes/My Image"
```

`--json` 是全局选项，必须放在 `scan` 或 `inspect` **之前**。不带子命令时默认扫描。

- `scan` 读取 `/Volumes/` 下的挂载点，报告检测到打开进程的卷。
- `inspect` 检查指定路径；如果匹配已知挂载点，会显示设备信息，以及进程名、PID 和处理建议。
- 解析器能匹配时，`hdiutil info` 会补充映像文件路径。

关闭报告中的应用后，重新执行 `inspect`，再尝试通过 Finder 正常弹出。手动执行 detach 建议之前，务必核对设备标识。

## 限制与安全

检查使用递归的 `lsof +D`，目录树很大时可能较慢；该查询会在五秒后超时。工具缺失、权限不足、命令失败或超时，都可能导致进程列表为空。**“未检测到占用”不保证可以安全分离该卷。**

界面显示的 open-handle 数量实际是去重后的命令/PID 条目数，不是文件描述符数量。映像路径关联是尽力而为的结果。诊断命令通常返回 `0`，即使发现占用也是如此；请读取报告，不要用退出码区分 busy/idle。

应用只读取系统状态，不写文件，也不改变挂载状态。报告可能包含本地路径和进程名，分享前请检查。

## 预览与开发

[输出截图](docs/images/example-output.png) · [演示视频](docs/demo.mp4)

```bash
python -m pip install pytest
python -m pytest -v
```

[实现](src/mac_dmg_doctor/cli.py) · [测试](tests/test_cli.py) · [MIT 许可证](LICENSE)
