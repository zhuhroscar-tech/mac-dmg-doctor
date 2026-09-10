# mac-dmg-doctor

`mac-dmg-doctor` is a lightweight diagnostic helper for macOS users who see
"Resource busy" or similar errors when detaching/unmounting DMG or mounted
volumes.

It only *reads* system state and prints safe guidance; it does not forcefully
terminate processes or run destructive unmount operations.

## Usage

```bash
# Scan mounted volumes with open handles
mac-dmg-doctor scan

# Inspect a specific mount point
mac-dmg-doctor inspect /Volumes/MyImage

# JSON output for scripting
mac-dmg-doctor scan --json
mac-dmg-doctor inspect /Volumes/MyImage --json
```

## Checks performed

- Reads `mount` output and highlights mount points under `/Volumes`.
- Uses `lsof +D <path>` to detect open file handles.
- Uses `hdiutil info` (if available) to correlate mounts to image paths.

## Security

No filesystem writes are performed.
