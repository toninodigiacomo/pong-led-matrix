# Wiring - Pong Controllers (Seeed XIAO ESP32-S3)
Wiring for the 2 DIY controller cases. Each case is identical: 1 rotary potentiometer (joystick) + 2 buttons (Start/Select, Pause).

## Components per enclosure
| Component               | Details                                             |
|-------------------------|-----------------------------------------------------|
| Microcontroller         | Seeed XIAO ESP32-S3                                 |
| Potentiometer           | WH148, 10 kΩ, linear (“B” taper), single-turn, 300° |
| Button 1 - Start/Select | 8 mm metal pushbutton, momentary, 2-pind            |
| Button 2 - Pause        | P8 mm metal pushbutton, momentary, 2-pin            |

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
              │      ┌──────────┐ │     |        │                 │
              └──────┼─► 1      │ │     |        │                 │
                     │   2 ●────┼─┘     |        │                 │
                     │   3 ●────┼───────┴────────│────────┬────────│────────┐
                     └──────────┘                │        │        │        │
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

-----

# Wiring - Display (HUB75 panels + adapter board + power supplies)
## Components
| Component               | Details                                             |
|-------------------------|-----------------------------------------------------|
| Raspberry Pi            | Pi 3                                                |
| Adapter board           | [HAT/HUB75](https://de.aliexpress.com/item/1005012491710993.html?spm=a2g0o.order_list.order_list_main.36.2c095e5bPojAKY&gatewayAdapt=glo2deu) |
| LED displays            | 2× HUB75 64×32, daisy-chained → 128×32              |
| Display power supply    | [5V, dedicated, RS-100-5 (see calculation below)](https://de.aliexpress.com/item/1005010698463734.html?spm=a2g0o.productlist.main.5.34b5FoPOFoPOrf&algo_pvid=c8d60dc1-213e-45f0-b350-761fae3add45&algo_exp_id=c8d60dc1-213e-45f0-b350-761fae3add45-4&pdp_ext_f=%7B%22order%22%3A%22-1%22%2C%22eval%22%3A%221%22%2C%22fromPage%22%3A%22search%22%7D&pdp_npi=6%40dis%21CHF%2114.20%2114.20%21%21%21115.67%21115.67%21%400b88ab8a17871395621861763e0c43%2112000053229343332%21sea%21CH%21173941914%21X%211%210%21n_tag%3A-29919%3Bd%3A93c017af%3Bm03_new_user%3A-29895&curPageLogUid=O1O5RjEPbHj9&utparam-url=scene%3Asearch%7Cquery_from%3A%7Cx_object_id%3A1005010698463734%7C_p_origin_prod%3A) |

## Complete schema
```txt
 ┌──────────────────────┐
 │   Power supply  5V ●─┼────┬───┬─────────────────────────────────────────┐
 │                GND ●─┼────┼───|──────────────────────────────────────┐  |
 └──────────────────────┘    │   │                                      |  |
                             ▼   ▼                                      |  |
                           ┌─┼───┼─┐      ┌──────────────────────┐      |  |
                           |  USB  |      │  HAT - Bonnet HUB75  │      |  |
            Raspberry Pi 3 └─┼───┼─┘      |                      |      |  |
            ┌────────────────┴───┴─┐      |   GPIO     IDC 2x8 ●─┼──┐   |  |
            |               GPIO ●─┼──►───┼────●                 |  |   |  |
            │                      │      └──────────────────────┘  |   |  |
            └──────────────────────┘                                ▼   ▼  ▼
                                                                    |   |  |
                                      ┌────────────────────────┐    |   |  |
                                      │ Display #1 (64x32)     │    |   |  |
                                      │                  5V  ●─┼────|───┤  |
                                      │                  GND ●─┼────|──────┤
                                      │                        │    |   |  |
                                      │          IDC 2x8 IN  ●─┼────┘   |  |
                                      │          IDC 2x8 OUT ●─┼────┐   |  |
                                      └────────────────────────┘    │   |  |
                                                                    ▼   ▼  ▼
                                                                    |   |  |
                                      ┌────────────────────────┐    |   |  |
                                      │ Display #2 (64x32)     │    |   |  |
                                      │                  5V  ●─┼────|───┘  |
                                      │                  GND ●─┼────|──────┘
                                      │                        │    |
                                      │          IDC 2x8 IN  ●─┼────┘
                                      │          IDC 2x8 OUT   |
                                      └────────────────────────┘
```

## Connection Details
1. **HAT HUB75 Board → Raspberry Pi** Plugs directly into the 40-pin GPIO connector.
2. **HAT/Bonnet board → Display #1** 2×8 IDC ribbon cable (included with the displays or the board) between the board’s output and the IN connector on Display #1.
3. **Display #1 → Display #2 (daisy chaining)** 2×8 IDC ribbon cable between the OUT connector on Display #1 and the IN connector on Display #2.
⚠️ Make sure to follow the IN → OUT direction - Connecting them backwards is the most common mistake.
4. **5V Power Supply for the Displays** ⚠️ Never power the displays from the Pi or the HAT board - **The required current far exceeds what the Pi can supply**.
⚠️ Run a cable from the dedicated 5V power supply directly to the power terminal block of each display, in parallel (both displays on the same power supply).
ℹ️ **Power calculation** Total width in pixels × 0.12A.
- For a width of 128 pixels → 128 × 0.12 ≈ 15.4A.
- Plan for a 5V / 15–20A power supply to ensure sufficient power at full brightness (the brightness can be reduced via software to lower power consumption in daily use, but the power supply must be sized generously to allow for a margin).




