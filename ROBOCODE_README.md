# ESP-Drone — Robocode frozen build

This is a fixed copy of [espressif/esp-drone](https://github.com/espressif/esp-drone) that builds with **ESP-IDF v5.0.7** for **ESP32-S2** and **ESP32-S3** drones. Nothing is downloaded at build time.

## What was changed from upstream

- Based on upstream commit `db0f6562e4f67cccee3acac4dff39c9aaea4e5fa` (June 2026), the last version that supports IDF 5.0. Newer upstream versions need IDF 5.5 or 6.1, so don't update.
- `espressif/esp-now` **2.5.2** and its helper `cmake_utilities` **0.5.3** are copied into `components/` rather than downloaded from the component registry.
- `crazyflie` and `wifi` components now list `esp-now` in their `REQUIRES`.

## Build and flash

Open the **ESP-IDF 5.0 CMD** (or PowerShell) shortcut from the Start menu, then:

```
cd C:\esp\esp-drone
idf.py set-target esp32s2        (or esp32s3)
idf.py -p COM5 flash monitor     (change COM5 to your port)
```

Press `Ctrl+]` to leave the monitor. Run `set-target` again only when switching between S2 and S3 boards.

## cfclient (PC control/debug app) — optional

Pinned to Robocode forks of the ESP-Drone cfclient (`RobocodeUK/crazyflie-clients-python@76d5093`, from leeebo) and cflib (`RobocodeUK/crazyflie-lib-python@a430283`) (the Wi-Fi/UDP link). Exact library versions are in `tools/cfclient/requirements-cfclient.txt`.

1. Install **Python 3.11** from python.org (3.13 does **not** work: numpy 1.x, pyzmq 25 and vispy 0.14 have no 3.13 builds).
2. Double-click `tools\cfclient\install_cfclient.bat` (creates `C:\esp\cfclient-venv`).
3. Connect the PC to the drone's Wi-Fi (`ESP-DRONE_XXXX`, password `12345678`), then run `C:\esp\cfclient-venv\Scripts\cfclient.exe`.
