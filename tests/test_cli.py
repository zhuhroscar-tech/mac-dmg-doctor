import unittest
from unittest.mock import patch

from mac_dmg_doctor import cli


class DmgDoctorTests(unittest.TestCase):
    def test_parse_mounts(self) -> None:
        text = """/dev/disk1s1 on / (apfs, local, read-only, noowners)
/dev/disk2s1 on /Volumes/ExampleVol (apfs, local, nodev, nosuid, read-write)
/dev/disk3s1 on /Volumes/Test Image (apfs, local, nodev, nosuid, read-write)
"""
        mounts = cli.parse_mounts(text)
        self.assertEqual(len(mounts), 2)
        self.assertEqual(mounts["/Volumes/ExampleVol"], "/dev/disk2s1")
        self.assertEqual(mounts["/Volumes/Test Image"], "/dev/disk3s1")

    def test_parse_lsof_processes(self) -> None:
        text = """COMMAND PID USER FD TYPE DEVICE SIZE/OFF NODE NAME
Finder 100 oscar cwd DIR 1,4 4096 1234 /Volumes/Example
chrome 101 oscar txt REG 1,4 1024 5678 /Applications/.."""
        rows = cli.parse_lsof_processes(text)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["command"], "Finder")

    def test_parse_hdiutil_info(self) -> None:
        text = """image-path: /Users/oscar/Documents/Test.dmg
   /dev/disk8
   mountpoint: /Volumes/TestImage
"""
        parsed = cli.parse_hdiutil_info(text)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]["image_path"], "/Users/oscar/Documents/Test.dmg")
        self.assertEqual(parsed[0]["mountpoint"], "/Volumes/TestImage")

    @patch("mac_dmg_doctor.cli.run_command")
    def test_scan_busy_mounts(self, run_command):
        def side_effect(cmd, timeout=3):
            if cmd == ["mount"]:
                return (
                    0,
                    (
                        "/dev/disk2s1 on /Volumes/BusyVol (apfs, local, nodev, nosuid, read-write)\n"
                        "/dev/disk3s1 on /Volumes/FreeVol (apfs, local, nodev, nosuid, read-write)"
                    ),
                    "",
                )
            if cmd[0:2] == ["lsof", "+D"]:
                if cmd[2] == "/Volumes/BusyVol":
                    return (
                        0,
                        "COMMAND PID USER FD TYPE DEVICE SIZE/OFF NODE NAME\nFinder 123 oscar cwd DIR 1,4 0 0 /Volumes/BusyVol",
                        "",
                    )
                return 1, "", ""
            if cmd == ["hdiutil", "info"]:
                return 0, "", ""
            return 1, "", "unexpected"

        run_command.side_effect = side_effect
        report = cli.scan_busy_mounts()
        self.assertEqual(report["mounted"], 2)
        self.assertEqual(len(report["busy"]), 1)
        self.assertEqual(report["busy"][0]["mountpoint"], "/Volumes/BusyVol")
        self.assertEqual(report["busy"][0]["open_processes"][0]["command"], "Finder")

    @patch("mac_dmg_doctor.cli.collect_hdi_images")
    @patch("mac_dmg_doctor.cli.collect_mounts")
    @patch("mac_dmg_doctor.cli.open_processes")
    def test_inspect_target_recommendation(self, open_processes, collect_mounts, collect_hdi_images):
        collect_mounts.return_value = {"/Volumes/Test": "/dev/disk9"}
        open_processes.return_value = [{"command": "python", "pid": "999"}]
        collect_hdi_images.return_value = {"/Volumes/Test": "/tmp/Test.dmg"}

        report = cli.inspect_target("/Volumes/Test")
        self.assertEqual(report["device"], "/dev/disk9")
        self.assertEqual(report["hdi_image_path"], "/tmp/Test.dmg")
        self.assertEqual(len(report["open_processes"]), 1)
        self.assertTrue(any("hdiutil detach" in line for line in report["recommendations"]))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
