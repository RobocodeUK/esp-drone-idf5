# ESP-Drone — Robocode frozen build

A fixed copy of [espressif/esp-drone](https://github.com/espressif/esp-drone) that builds with **ESP-IDF v5.0.7** for **ESP32-S2** and **ESP32-S3** drones, plus a pinned PC client (cfclient). Nothing is downloaded at build time, and nothing changes unless Robocode changes it.

## Start here

Everything for setting up a PC is in the **`robocode-setup`** folder:

| File | What it is |
|---|---|
| **`SETUP.bat`** | Double-click this. Installs Git 2.47.1, ESP-IDF 5.0.7, Python 3.11.9 and cfclient, skipping anything already installed. |
| `ROBOCODE_SETUP_GUIDE.pdf` | Step-by-step guide from a fresh Windows PC to live drone data. |
| `install_cfclient.bat` | Installs or repairs just cfclient (SETUP.bat runs it). |
| `DOWNLOAD_LINKS.txt` | The pinned official installer links and their SHA-256 fingerprints. |
| `download_and_verify.ps1` | Helper: downloads a file and refuses it if the fingerprint doesn't match. |
| `requirements-cfclient.txt` | Exact versions of every cfclient library. |
| `guide/make_guide.py` | Regenerates the PDF (needs `reportlab`). |

Installers are downloaded from the official sites into `robocode-setup\downloads\` (not stored in the repo; the ESP-IDF installer alone is 916 MB) and checked against their fingerprints before running.

## Quick reference

Build and flash — open **ESP-IDF 5.0 CMD** from the Start menu:

```
cd C:\esp\esp-drone
idf.py set-target esp32s2          (or esp32s3)
idf.py -p COM3 flash monitor       (use your COM port; Ctrl+] to exit)
```

cfclient — installed by `SETUP.bat` (or repair it with `robocode-setup\install_cfclient.bat`). Join the drone's Wi-Fi `ESP-DRONE_XXXXXXXXXXXX` (password `12345678`) and start **cfclient (ESP-Drone)** from the desktop.

## What is pinned

| Part | Source | Version |
|---|---|---|
| Firmware | upstream `espressif/esp-drone` | `db0f6562` (June 2026, last IDF 5.0 version) |
| esp-now / cmake_utilities | vendored in `components/` | 2.5.2 / 0.5.3 |
| cfclient | `RobocodeUK/crazyflie-clients-python` (fork of leeebo) | `76d5093` |
| cflib | `RobocodeUK/crazyflie-lib-python` (fork of leeebo) | `f2baeab` (adds UDP keep-alive) |
| Other Python libraries | PyPI | exact versions in `robocode-setup/requirements-cfclient.txt` |
| Installers | official download links | Git 2.47.1, ESP-IDF 5.0.7 offline, Python 3.11.9 (SHA-256 in `robocode-setup/DOWNLOAD_LINKS.txt`) |

Don't update to newer upstream esp-drone: it needs ESP-IDF 5.5 or 6.1.

## Changes from upstream

- esp-now and cmake_utilities copied into `components/`, and `esp-now` added to the `crazyflie` and `wifi` `REQUIRES`.
- Upstream CI workflows removed.
- cflib UDP driver sends a keep-alive every 100 ms. Without it the drone stops sending data 1 s after the PC goes quiet (no gamepad), so cfclient froze after a few seconds.

## Known issues

- **`MPU6050 I2C connection [FAIL]`** on boot (no sensor data, cfclient frozen): the IMU has locked up, often after a crash or on a low battery. Unplug USB **and** battery for 10 s, then power on again. Charge the battery.
- **Windows drops the drone Wi-Fi** after ~40 s and rejoins the home network (the drone has no internet). Untick "Connect automatically" on other saved networks while flying.
- **cfclient "Socket is already connected"** after a disconnect: close and reopen cfclient.
- cfclient is tested on Python 3.11 only (the installer sets it up). Python 3.13 will not install it.
