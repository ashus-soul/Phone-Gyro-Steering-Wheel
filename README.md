# 📱 Phone Air Steering Wheel

Turn your smartphone into an "air" steering wheel for PC driving games. Tilt your phone to steer, and the script converts the sensor data into a virtual Xbox 360 controller using UDP and [`vgamepad`](https://github.com/yannbouteiller/vgamepad).

No extra hardware needed, just your phone and your PC on the same Wi-Fi network.

---

## ✨ Features

- **Tilt to steer**: phone tilt is mapped to the left joystick (X axis)
- **Throttle / reverse**: controlled by phone pitch, mapped to the right and left triggers
- **Handbrake**: a dedicated tilt zone presses the `A` button
- **Smooth steering**: small dead zone removes jitter around the centre
- **Low latency**: sensor data is sent over UDP
- **Works as a real controller**: games see a standard Xbox 360 gamepad

---

## 🧰 Requirements

- Windows PC (ViGEmBus is Windows-only)
- Python 3.8+
- [ViGEmBus driver](https://github.com/nefarius/ViGEmBus/releases)
- Python package: `vgamepad`
- A phone app that streams sensor data over UDP as plain text `x,y,z` (see [Phone setup](#-phone-setup))
- Phone and PC connected to the **same network**

---

## 🚀 Installation

1. Install the **ViGEmBus** driver and restart your PC if asked.
2. Clone this repo and install the dependency:

```bash
git clone <your-repo-url>
cd <your-repo-folder>
pip install vgamepad
```

---

## 📲 Phone setup

Your phone must send UDP packets to your PC on port **9999**, where each packet is a comma-separated string of three numbers:

```
x,y,z
```

For example: `5.12,-3.40,1.85`

1. Find your PC's local IP address (run `ipconfig` in Command Prompt and look for the IPv4 address).
2. In your sensor-streaming app, set:
   - **Protocol:** UDP
   - **IP address:** your PC's local IP
   - **Port:** `9999`
   - **Data format:** `x,y,z` (accelerometer or the sensor you calibrated for)
3. Start streaming.

> If your app uses a different packet format, edit `parse_message()` in the script.

---

## ▶️ Usage

1. Run the script:

```bash
python main.py
```

2. Start streaming from your phone.
3. Open your game and set the controller as the input device (it shows up as an Xbox 360 controller).
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

- Tilt angle is divided by 6 to give a value between -1 and 1.
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
Phone sensors ──UDP──▶ Python server (port 9999) ──▶ vgamepad ──▶ Virtual Xbox 360 controller ──▶ Game
```

1. The script opens a UDP socket and listens for packets.
2. Each packet is parsed into `x, y, z` floats.
3. The values are converted into steering, throttle, reverse, and handbrake inputs.
4. `vgamepad` sends those inputs to the virtual controller via ViGEmBus.

---

## 🩹 Troubleshooting

| Problem | Fix |
|---------|-----|
| `NOT A NUMBER GNG` printed repeatedly | Your phone app is sending a different format. It must be `x,y,z` as plain numbers. |
| No input in the game | Check that ViGEmBus is installed, and that the game detects an Xbox 360 controller. |
| Nothing received from the phone | Make sure both devices are on the same Wi-Fi, check the IP/port, and allow Python through Windows Firewall (UDP 9999). |
| Steering feels reversed or axes are mixed up | Your phone's sensor axes differ. Swap the `x`, `y`, `z` assignments in the main loop or adjust the zones. |
| Steering feels twitchy | Increase the dead zone or add smoothing (e.g. `0.2 * new + 0.8 * old`). |
| `GP disconnected` error | The virtual gamepad failed. Reinstall ViGEmBus and restart the script. |

---

## 🗺️ Roadmap

- [ ] Apply the smoothing filter (`20% new + 80% old`) to steering
- [ ] Analog throttle/brake based on tilt depth
- [ ] Config file or CLI arguments instead of editing the script
- [ ] Calibration mode to set the neutral position
- [ ] Support for extra buttons (gear shift, horn, etc.)

---

## ⚠️ Notes

- UDP has no authentication. Only use this on a trusted network.
- Not tested with every game. Games that support Xbox controllers should work best.

---

## 📄 License

Add your license here (e.g. MIT).
