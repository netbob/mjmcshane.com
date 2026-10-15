---
title: "The Twelve-Dollar Rehearsal"
description: "The 65C02 silicon arrives Friday and its breadboard next week, but the machine's future motherboard landed first, so the Pi 400 and a Raspberry Pi Pico are learning to talk before there is a CPU to talk about"
author: Michael McShane
date: 2026-10-14 17:35:00 -0700
categories: [Tech]
tags: [tech, '6502', raspberry-pi, pico]
pin: false
toc: true
---

The parts for the breadboard //e are arriving out of order, and it turns out the order is right.

The W65C02S and its supporting silicon land Friday, in a Mouser box. The breadboard they will live on lands next week. But the first arrival, due tomorrow, is a $12 Raspberry Pi Pico — a board that plays no part in Phase 1 of the build at all. Phase 1 is the processor free-running on a clock the Pi 400 generates, while the Pi watches the address bus and takes notes. No Pico required.

The Pico is for Phase 2, and Phase 2 is where the design gets honest about its two walls.

## Why the machine needs a second computer

The plan, from the first post in this series: in the early phases the Pi 400 is the 6502's memory, its clock, and its terminal. That works beautifully at a crawl, because the W65C02S is a fully static chip — stop the clock mid-instruction and it simply waits, indefinitely, while Linux takes its time.

It stops working at speed, for two reasons:

- **Pins.** Serving the bus takes 27 lines — 16 address, 8 data, clock, read/write, reset. The Pi 400's header offers 26 usable GPIO. One short, before a single spare.
- **Timing.** At an honest 1 MHz, each bus cycle is a microsecond, and the servant has to answer inside it, every time. Linux is a superb multitasker and a terrible metronome — scheduling jitter is measured in the same microseconds the bus allows. A servant who is *usually* fast enough is a machine that crashes *occasionally*, which is the worst kind.

The established cure — every serious build in this space, from the Neo6502 to the Sorbus Computer, converged on it — is a microcontroller in the middle. The RP2040 chip in the Pico has programmable I/O hardware that answers the bus deterministically, cycle by cycle, while the Pi supervises from a comfortable distance.

So the division of labor in the finished machine: **the Pico is the motherboard** — clock, memory service, I/O registers. **The Pi is the console** — keyboard, HDMI screen, the LOAD and SAVE files. And the two halves are joined by exactly one thing: a serial link. Two signal wires and a ground.

A motherboard that cannot talk to its console is a brick. So the first experiment with the Pico isn't a blink. It's the handshake.

## The rehearsal

Three jumpers, female ends slipped onto the labeled pins of the Pi's GPIO shield (the same shield running the ultrasonic sensor build — GPIO 14 and 15 were never part of that circuit), male ends into the breadboard strips beside the Pico's pins:

- Shield pin **15** (receive) to the Pico's **GP0** strip — the Pico talks, the Pi listens
- Shield pin **14** (transmit) to the Pico's **GP1** strip — the Pi talks back
- Shield **GND** to the Pico's ground strip — without a shared ground, a serial link is two machines shouting into separate voids

Serial crosses over, transmit to receive, like two people each holding a phone to the correct ear. Both sides are 3.3-volt logic, so the wires connect directly — a small mercy after the ultrasonic sensor's Echo line, which needed a three-resistor divider to step its 5 volts down to something the Pi could survive. The Pico gets its power from its own USB cable. No power wire ever crosses between the two boards; the link is signals and ground, nothing else.

On the Pico, eleven lines of MicroPython:

```python
from machine import UART, Pin
import time

uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
led = Pin(25, Pin.OUT)

while True:
    uart.write("hello from pico\n")
    led.toggle()
    if uart.any():
        data = uart.readline()
        print("Pi says:", data)
    time.sleep(1)
```

On the Pi, after a short detour through `raspi-config` to enable the serial hardware (and decline the login shell — the port has a job already), one command opens the window: `python3 -m serial.tools.miniterm /dev/serial0 115200`.

Proof is two lines. `hello from pico`, arriving once a second in the Pi's terminal. And a word typed there, surfacing in the Pico's console: `Pi says:`. Both directions seen, the link is real. Save the program on the Pico as `main.py` and it starts handshaking by itself at every power-up — no development tools attached, a small machine already doing its one job unprompted.

## What this buys the build

Not speed — nothing here touches the bus-timing problem yet; that is PIO work, later, and it is the Pico's real examination. What the rehearsal retires is everything around that problem: the console link Phase 2 will stand on, the firmware toolchain (the Pi as the Pico's development machine, via Thonny), and the wiring discipline of one more board on the bench. Phase 2's scariest sentence used to be "and then the two computers talk." After tomorrow it is a thing that already happened, on a Tuesday, for twelve dollars.

One honest caveat, because this site keeps its receipts in the open: the stock Pico exposes 26 GPIO, and the full bus job wants 27 — the same one-pin shortfall as the Pi, in miniature. The known closings are to offload the reset line (a pushbutton, or the Pi drives it down the console link it already owns) or to step up to Olimex's RP2040-PICO30, which breaks out all 30. That decision belongs to Phase 2. The handshake doesn't care which board it runs on.

When the breadboard lands next week, Phase 1 starts as planned — a processor, a clock made of software, `LDA DARK` walking the bus where the Pi can watch it. But at the other end of the sensor board there will be a second small computer, blinking once a second, already fluent in the only language the finished machine needs between its halves — waiting for its promotion.
