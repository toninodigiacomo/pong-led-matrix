# Wiring - Pong Controllers (Seeed XIAO ESP32-S3)
Wiring for the 2 DIY controller cases. Each case is identical: 1 rotary potentiometer (joystick) + 2 buttons (Start/Select, Pause).

## Components per enclosure
| Component               | Part Number                                         |
|-------------------------|-----------------------------------------------------|
| Microcontroller         | Seeed XIAO ESP32-S3                                 |
| Potentiometer           | WH148, 10 kΩ, linear (“B” taper), single-turn, 300° |
| Button 1 — Start/Select | 8 mm metal pushbutton, momentary, 2-pind            |
| Button 2 — Pause        | P8 mm metal pushbutton, momentary, 2-pin            |

## Pin Selection (XIAO ESP32-S3)
Pins D2, D6, and D7 play a role during boot on the ESP32-S3 - Avoid using them. Use only “safe” pins:

| Function               | XIAO Pin | Type         |
|------------------------|----------|--------------|
| Potentiometer (slider) | A0 (D0)  | Analog (ADC) |
| Start/Select button    | D1       | Digital      |
| Pause button           | D3       | Digital      |

## Wiring Diagram
#### Potentiometer (WH148, 3-pin)
```txt
        WH148
    ┌───────────┐
    │  1  2  3  │
    └──┬──┬──┬──┘
       │  │  └──── GND
       │  └─────── A0 (cursor / wiper)
       └────────── 3V3
```
| Potentiometer Pin | XIAO Pin | Function               |
|-------------------|----------|------------------------|
| 1                 | 3V3      | Power Supply           |
| 2 (slider)        | A0       | Analog Signal (0–3.3V) |
| 3                 | GND      | Ground                 |

> The 1/3 direction can be reversed depending on the desired rotation direction (racket moving up vs. down) - If the movement is reversed after testing, simply swap wires 1 and 3, or reverse the mapping in the code ```(map(potValue, 4095, 0, ...))```

#### Buttons (2-pin, momentary)
Each button is wired between its digital pin and GND, using the GPIO's internal pull-up resistor (```INPUT_PULLUP``` in the firmware) - No external resistor is required.
```txt
  Bouton Start/Select          Bouton Pause
   ┌───────────┐               ┌───────────┐
   │  o     o  │               │  o     o  │
   └──┬─────┬──┘               └──┬─────┬──┘
      │     │                     │     │
      D1   GND                    D3   GND
```
| Bouton       | XIAO Pin | GND |
|--------------|----------|-----|
| Start/Select | D1       | GND |
| Pause        | D3       | GND |

## Complete schema
```txt
                         ┌──────────────────────────┐
                         │   Seeed XIAO ESP32-S3    │
                         │                          │
                         │   ┌──────────────────┐   │
                         │   │      USB-C       │───┼────────► Raspberry Pi
                         │   └──────────────────┘   │        (Alim + HID Gamepad)
                         │                          │
                         │  3V3 ●                   │
                         │  GND ●●●                 │
                         │  A0  ●                   │
                         │  D1  ●                   │
                         │  D3  ●                   │
                         │                          │
                         └──┬─────┬─────┬────┬────┬─┘
                            │     │     │    │    │
              ┌─────────────┘     │     │    │    └────────────────┐
              │                   │     │    └───┐                 │
              │                   │     │        │                 │
              ▼                   ▲     ▲        ▲                 ▲
            (3V3)                (A0) (GND)     (D1)              (D3)
              │                   │     │        │                 │
              │                   │     |        │                 │
              │                   |     |        │                 │
              │       ┌─────────┐ │     |        │                 │
              └───────┼─►1      │ │     |        │                 │
                      │  2 ●────┼─┘     |        │                 │
                      │  3 ●────┼───────┴────────│────────┬────────│────────┐
                      └─────────┘                │        │        │        │
                         WH148                   │        │        │        │
                     Potentiometer            ┌──┼────────┼──┐  ┌──┼────────┼──┐
                                              │  ●        ●  │  │  ●        ●  │
                                              │ (D1)    (GND)│  │ (D3)    (GND)│
                                              └──────────────┘  └──────────────┘
                                               [Bouton Start]    [Bouton Pause]
```

## Assembly  Notes
- The WH148 potentiometer has a total rotation of 300° with true mechanical stops—there is no need to handle software-based stops, unlike with an incremental encoder.
- The 8mm knobs are panel-mount type - an 8mm hole in the enclosure wall is sufficient; they are secured using the supplied nut and ring.
- A single USB-C cable per enclosure is sufficient: power for the XIAO and HID Gamepad data transmission use the same connection, which plugs directly into a USB port on the Raspberry Pi.
