# Pong LED Matrix
A DIY Pong game built with an HUB75 LED matrix, controlled by a Raspberry Pi running Python, with two homemade controllers based on the Seeed XIAO ESP32-S3.

This project began when I repurposed two 64x32 HUB75 LED panels that had been purchased as surplus for a pincab project (PIN2DMD).

---

## Overview
| Element              | Description                                                                                 |
|----------------------|---------------------------------------------------------------------------------------------|
| Display              | 2x HUB75 64x32 panels daisy-chained → 128x32 pixels                                         |
| Display controller   | Raspberry Pi3 + Adafruit RGB Matrix HAT                                                     |
| Controllers          | 2x DIY enclosures, rotary potentiometer + buttons, Seeed XIAO ESP32-S3 as a USB HID gamepad |
| Programming Language | Python (game + logic), C++/Arduino (controller firmware)                                    |

---

## Hardware
**Display**
- [2x HUB75 64x32 LED panels (P2.5, 160x80mm)](https://de.aliexpress.com/item/4000002686894.html?spm=a2g0o.order_list.order_list_main.25.349d5e5bjVvuIp&gatewayAdapt=glo2deu)
- Raspberry Pi 3
- [RGB Matrix HAT](https://de.aliexpress.com/item/1005012491710993.html?spm=a2g0o.order_list.order_list_main.19.349d5e5bjVvuIp&gatewayAdapt=glo2deu)
- Dedicated 5V power supply for the panels (allow plenty of headroom; ~4A per panel at full brightness)
- Enclosure (3D-printed or wood)

**Joysticks (x2)**
- [1x Seeed XIAO ESP32-S3](https://de.aliexpress.com/item/1005009532378267.html?spm=a2g0o.order_list.order_list_main.62.21ef5e5bRagfYp&gatewayAdapt=glo2deu)
- [1x 10kΩ linear rotary potentiometer (with a mechanical stop)](https://de.aliexpress.com/item/1005003161558340.html?spm=a2g0o.order_list.order_list_main.4.21ef5e5bRagfYp&gatewayAdapt=glo2deu)
- [2 pushbuttons (start/select, pause)](https://de.aliexpress.com/item/1005007846743211.html?spm=a2g0o.productlist.main.1.7929zRVPzRVPAJ&algo_pvid=d8ded36e-1367-44e6-b110-11ba5b95bca0&algo_exp_id=d8ded36e-1367-44e6-b110-11ba5b95bca0-0&pdp_ext_f=%7B%22order%22%3A%224065%22%2C%22eval%22%3A%221%22%2C%22fromPage%22%3A%22search%22%7D&pdp_npi=6%40dis%21CHF%210.66%210.66%21%21%210.80%210.80%21%400b88ad2b17871277200061079e0dc1%2112000042509083257%21sea%21CH%21173941914%21X%211%210%21n_tag%3A-29919%3Bbm%3A1%3Bd%3A93c017af%3Bm03_new_user%3A-29895&curPageLogUid=On7RRVf0PfBF&utparam-url=scene%3Asearch%7Cquery_from%3A%7Cx_object_id%3A1005007846743211%7C_p_origin_prod%3A)
- Enclosure (3D-printed or wood)

---

## Wiring
**Potentiometer → XIAO ESP32-S3**
| Potentiometer | XIAO pin   |
|---------------|------------|
| 1             | 3V3        |
| 2 (slider)    | A0 (GPIO1) |
| 3             | GND        |

**Buttons → XIAO ESP32-S3**
- Each button connects a digital pin (D1, D2...) to GND, with an internal pull-up (INPUT_PULLUP); no external resistor is required.

---

## Software
**Display (Raspberry Pi)**
- rpi-rgb-led-matrix library (hzeller) with Python bindings
- Chaining options: --led-cols=64 --led-rows=32 --led-chain=2

**Controllers (ESP32-S3)**
- Arduino IDE, ESP32 core, USBHIDGamepad library (TinyUSB)  
  ⚠️ Enable “USB CDC On Boot” in the board settings
- Reads the potentiometer axis and button states, sent as native USB HID Gamepad data

**Game (Python, on the Pi)**
- pygame.joystick to read the 2 USB controllers directly (no custom serial protocol required)
- Game loop: paddle positions, ball physics, collisions, score

---

## Repository Structure

```txt
pong-led-matrix/
├── README.md
├── firmware/
│   └── paddle_controller/
│       └── paddle_controller.ino
├── software/
│   ├── pong.py
│   ├── display.py
│   └── requirements.txt
├── hardware/
│   ├── wiring.md
│   └── enclosure/               ← STL files for controller cases
└── docs/
    └── photos/
```

---

## Roadmap
- [x] Choosing the hardware (boards, Pi, ESP32)
- [x] Choosing the gamepad solution (Seeed XIAO ESP32-S3, native HID Gamepad)
- [ ] Wiring and testing the two gamepads
- [ ] ESP32-S3 firmware (reading potentiometer and buttons → HID Gamepad)
- [ ] Configuring the Raspberry Pi + 128x32 display
- [ ] Pong script (display, physics, score)
- [ ] 3D-printed enclosures
- [ ] Final assembly

---

## License
**MIT** [LICENCE.md](https://github.com/toninodigiacomo/pong-led-matrix/blob/f3098bfc4be7f9d33e8b683e3e7f83d1b701de16/LICENSE.md)
