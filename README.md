# IllumiNation – Smart Lighting Prototype

**Smart lighting, brighter futures**

A multi-modal smart lighting system designed for medical environments, focused on accessibility, convenience, and energy efficiency. This project explores how intelligent lighting can reduce patient disruption, improve safety, and lower energy usage through sensor-driven automation and manual control.

⸻

## The Problem

Lighting in hospitals is way less accessible than it should be.

Patients often can't reach wall-mounted switches, especially at night, which forces them to call staff for basic lighting changes. Staff then end up disrupting patient rest during early morning rounds just to turn lights on. On top of that, traditional switches introduce hygiene concerns and increase fall risk in low-light conditions.

This project addresses those issues by creating a lighting system that is easy to access, adaptive to the environment, and usable without physical switches.

⸻

## The Solution

IllumiNation is a three-mode smart lighting system where multiple control methods can operate at the same time:

### 1. Manual Control

Lights can be turned on or off through a web-based interface on a phone or laptop.

### 2. Motion-Activated Lighting

Infrared sensors detect movement and automatically turn lights on when someone enters or moves within the room.

### 3. Ambient Light-Aware Lighting

A light sensor measures natural light levels and adjusts artificial lighting accordingly.

Any combination of these modes can be enabled simultaneously. For example, motion detection can remain active at night even if the lights are manually turned off, improving safety without disturbing sleep.

⸻

## Why This Matters

Existing hospital lighting solutions usually implement these features in isolation. This project combines them into a single system that:
- Improves accessibility for patients
- Reduces unnecessary staff intervention
- Minimizes nighttime disruption
- Has the potential to reduce hospital energy consumption

⸻

## System Overview

### Inputs
- Ambient light level
- Motion detection
- Room temperature

### Processing
- Control logic running on a Raspberry Pi Pico determines lighting behavior based on enabled modes and sensor readings

### Outputs
- LED lighting (used as a stand-in for room lighting)
- Live feedback through the web interface

⸻

## Hardware Used

| Component | Purpose |
|-----------|---------|
| Light Sensor (C2255-001) | Detects ambient light level |
| Thermistor (AL03006-165.9-55-G1) | Measures room temperature |
| IR Emitter (IR333-A) | Motion detection |
| IR Receiver (LTR-3208E) | Motion detection |
| LED (WP7113ID) | Represents room lighting |

### Software Stack
- Raspberry Pi Pico
- C / MicroPython (control logic)
- HTML (web-based UI)

The system connects sensor data and control logic directly to the UI, allowing real-time feedback and control.

⸻

## User Interface

The web interface allows:
- Manual light toggling
- Enabling or disabling motion detection
- Enabling or disabling ambient light automation
- Viewing live temperature data
- Viewing time and date information

The UI is designed to be simple, readable, and usable on both desktop and mobile devices.

⸻

## Current Status

This repository represents a working prototype.

**What's implemented:**
- Motion-based lighting control
- Ambient light-based automation
- Temperature sensing
- Web UI controls
- Hardware and software integration

**Planned improvements:**
- UI polish and responsiveness
- Better sensor calibration
- Expanded automation logic
- Multi-room scalability

⸻

## Disclaimer

This project is a functional prototype built for exploration and learning. It is not intended for direct clinical deployment.
