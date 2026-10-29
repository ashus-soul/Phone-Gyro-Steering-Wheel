# 📱 Phone Air Steering Wheel

Turn your smartphone into an "air" steering wheel for PC driving games. Tilt your phone to steer, and the script converts the phone's gravity sensor data into a virtual Xbox 360 controller using UDP and [`vgamepad`](https://github.com/yannbouteiller/vgamepad).

No extra hardware needed, just your phone and your PC on the same Wi-Fi network.

> **Status:** works today with the [HyperIMU](https://play.google.com/store/apps/details?id=com.ianovir.hyperimu) app. A dedicated Android app is planned (see [Android app](#-android-app-planned)).

---

## ⭐ Features

- **Tilt to steer**: phone tilt is mapped to the left joystick (X axis)
- **Throttle / reverse**: controlled by phone pitch, mapped to the right and left triggers
- **Handbrake**: a dedicated tilt zone presses the `A` button
- **Dead zone**: a small dead zone around the centre removes jitter
- **Low latency**: sensor data is sent over UDP
- **Works as a real controller**: games see a standard Xbox 360 gamepad

---

## 🙏 Requirements

- Windows PC (ViGEmBus is Windows-only)
- Python 3.8+
- [ViGEmBus driver](https://github.com/nefarius/ViGEmBus/releases)
- Python package: `vgamepad`
- Android phone with [HyperIMU](https://play.google.com/store/apps/details?id=com.ianovir.hyperimu) (or any app that sends `x,y,z` over UDP)
- Phone and PC connected to the **same network**

---

## 🚀 Installation

1. Install the **ViGEmBus** driver and restart your PC if asked.
2. Clone this repo and install the dependency:

```bash
git clone https://github.com/ashus-soul/Phone-Gyro-Steering-Wheel
cd Phone-Gyro-Steering-Wheel
pip install vgamepad
```

---

## 📲 Phone setup (HyperIMU)

1. Find your PC's local IP address: run `ipconfig` in Command Prompt and look for the **IPv4 Address**.
2. Open **HyperIMU** on your phone and select **only the Gravity sensor**. Selecting only one sensor makes each packet exactly three numbers, which is what the script expects.
3. In the stream settings, set:
   - **Protocol:** UDP
   - **IP address:** your PC's local IP
   - **Port:** `9999`
4. If HyperIMU is adding extra values like a timestamp, turn them off so the packet stays `x,y,z`.
5. Start streaming.

Each packet should look like this:

```
x,y,z
```

For example: `5.12,-3.40,1.85`

> **Why gravity?** The gravity sensor gives values from about -9.8 to 9.8 (m/s²) depending on how your phone is tilted, which is why the default zones in the script use numbers like 6 and 8. The raw gyroscope sends rotation speed instead, so it won't work with these values.

> If your app uses a different packet format, edit `parse_message()` in the script.

**Tested on:** Redmi Note 8 Pro + HyperIMU. Other phones may report slightly different axes, so you might need to tune the zones (see [Configuration](#️-configuration)).

---

## ▶️ Usage

1. Run the script:

```bash
python server_gp.py
```

2. Start streaming from your phone.
3. Open your game and select the controller as the input device (it shows up as an Xbox 360 controller).
4. Hold your phone in landscape like a steering wheel and drive!

Press `Ctrl + C` to stop. The virtual gamepad is reset automatically on exit.

---

## 🎮 Controls mapping

| Phone axis | Range | Action | Gamepad output |
|-----------|-------|--------|----------------|
| `y` | -6 to 6 (clamped beyond) | Steering | Left joystick X (-1 to 1) |
| `x` | `< 6` | Accelerate | Right trigger |
| `x` | `> 8` | Reverse | Left trigger |
| `x` | 6 to 8 | Dead zone | Nothing |
| `z` | 0 to 4 | Handbrake | `A` button |

**Steering details**

- Tilt value is divided by 6 to give a value between -1 and 1.
- Values between -0.1 and 0.1 are treated as 0 (dead zone) to stop jitter.
- Tilting past ±6 gives full lock.

---

## ⚙️ Configuration

You can tune the zones at the top of the script to fit your phone and the way you hold it:

```python
ACC_MAX = 6   # x below this  -> accelerate
REV_MIN = 8   # x above this  -> reverse (between ACC_MAX and REV_MIN is a dead zone)
HB_MIN  = 0   # z from HB_MIN to HB_MAX -> handbrake
HB_MAX  = 4
```

Other settings:

- **Port:** change `server.bind(("0.0.0.0", 9999))` to use a different port.
- **Steering sensitivity:** change the `6` in `run_server_tilt()` (lower = more sensitive).
- **Steering dead zone:** change the `0.1` threshold in `run_server_tilt()`.

---

## 🛠️ How it works

```
Phone gravity sensor ──UDP──▶ Python server (port 9999) ──▶ vgamepad ──▶ Virtual Xbox 360 controller ──▶ Game
```

1. The script opens a UDP socket and listens for packets.
2. Each packet is parsed into `x, y, z` floats.
3. The values are converted into steering, throttle, reverse, and handbrake inputs.
4. `vgamepad` sends those inputs to the virtual controller via ViGEmBus.

---

## 📦 Android app (planned)

A dedicated Android app is planned to replace HyperIMU. It will send the sensor data to the PC over UDP in the same `x,y,z` format, so this script will keep working without changes. The app may be built with the Godot engine.

---

## 🩹 Troubleshooting

| Problem | Fix |
|---------|-----|
| `NOT A NUMBER GNG` printed repeatedly | The phone app is sending a different format. Select only the Gravity sensor in HyperIMU and turn off extras like timestamps. |
| No input in the game | Check that ViGEmBus is installed, and that the game detects an Xbox 360 controller. |
| Nothing received from the phone | Make sure both devices are on the same Wi-Fi, check the IP and port, and allow Python through Windows Firewall (UDP 9999). |
| Steering feels reversed or axes are mixed up | Your phone's sensor axes differ. Swap the `x`, `y`, `z` assignments in the main loop or adjust the zones. |
| Steering feels twitchy | Increase the dead zone. |
| `GP disconnected` error | The virtual gamepad failed. Reinstall ViGEmBus and restart the script. |

---

## ⚠️ Notes

- UDP has no authentication. Only use this on a trusted network.
- Not tested with every game. Games that support Xbox controllers should work best.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).