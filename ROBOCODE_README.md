# ESP-Drone — Robocode frozen build

A fixed copy of [espressif/esp-drone](https://github.com/espressif/esp-drone) that builds with **ESP-IDF v5.0.7** for **ESP32-S2** and **ESP32-S3** drones, plus a pinned PC client (cfclient). Nothing is downloaded at build time, and nothing changes unless Robocode changes it.

The full step-by-step setup guide (with prerequisites) is **`ROBOCODE_SETUP_GUIDE.pdf`** in this folder.

## Quick reference

Build and flash — open **ESP-IDF 5.0 CMD** from the Start menu:

```
cd C:\esp\esp-drone
idf.py set-target esp32s2          (or esp32s3)
idf.py -p COM3 flash monitor       (use your COM port; Ctrl+] to exit)
```

cfclient — install **Python 3.11.9** and **Git for Windows**, then double-click `tools\cfclient\install_cfclient.bat`. Join the drone's Wi-Fi `ESP-DRONE_XXXXXXXXXXXX` (password `12345678`) and start **cfclient (ESP-Drone)** from the desktop.

## What is pinned

| Part | Source | Version |
|---|---|---|
| Firmware | upstream `espressif/esp-drone` | `db0f6562` (June 2026, last IDF 5.0 version) |
| esp-now / cmake_utilities | vendored in `components/` | 2.5.2 / 0.5.3 |
| cfclient | `RobocodeUK/crazyflie-clients-python` (fork of leeebo) | `76d5093` |
| cflib | `RobocodeUK/crazyflie-lib-python` (fork of leeebo) | `f2baeab` (adds UDP keep-alive) |
| Other Python libraries | PyPI | exact versions in `tools/cfclient/requirements-cfclient.txt` |

Don't update to newer upstream esp-drone: it needs ESP-IDF 5.5 or 6.1.

## Changes from upstream

- esp-now and cmake_utilities copied into `components/`, and `esp-now` added to the `crazyflie` and `wifi` `REQUIRES`.
- Upstream CI workflows removed.
- cflib UDP driver sends a keep-alive every 100 ms. Without it the drone stops sending data 1 s after the PC goes quiet (no gamepad), so cfclient froze after a few seconds.

## Known issues

- **`MPU6050 I2C connection [FAIL]`** on boot (no sensor data, cfclient frozen): the IMU has locked up, often after a crash or on a low battery. Unplug USB **and** battery for 10 s, then power on again. Charge the battery.
- **Windows drops the drone Wi-Fi** after ~40 s and rejoins the home network (the drone has no internet). Untick "Connect automatically" on other saved networks while flying.
- **cfclient "Socket is already connected"** after a disconnect: close and reopen cfclient.
- cfclient is tested on Python 3.11 only. Python 3.13 will not install it.
