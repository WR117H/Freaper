(https://github.com/user-attachments/assets/98c173ed-3681-46a3-82b4-6442a49e7662)

**Freaper** – SubGHz Toolkit for RP2040 + CC1101

> **SHcipher – Atmega based subghz tool** (Now ported and expanded for RP2040)

---

## 🧬 What is Freaper?

**Freaper** is a compact and powerful Sub-1GHz hacking toolkit built around the **RP2040 microcontroller** and **CC1101 RF transceiver**. It brings together a suite of essential features including:

- 🔊 **Jammer** – Saturate SubGHz frequencies to disrupt communication.
- 🧭 **Analyzer** – Scan and analyze SubGHz signals with precision.
- 📡 **Raw Recorder** – Capture raw packets for later study or replay.
- 🔁 **Replay** – Re-transmit captured signals for penetration testing and IoT fuzzing.

Whether you're a security researcher or an RF enthusiast, Freaper provides a flexible interface and robust capabilities in a minimalist package.

---

## 🚀 Features

- ✅ Compatible with RP2040-based boards
- ✅ Uses CC1101 (433/868/915 MHz supported)
- ✅ Interactive CLI interface via USB serial
- ✅ Plug-and-play: no external drivers required
- ✅ Open source and customizable

---

## 🖥️ CLI Preview

![CLI Screenshot](./path/to/command_preview.png)

The interface supports modular commands. Example:

```bash
freaper1 > scan
freaper1 > jam 433.92
freaper1 > record raw_433.sig
freaper1 > replay raw_433.sig
