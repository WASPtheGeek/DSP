# 🎧️ Digital Signal Processing (DSP) & Hearing Tech Marathon

This project documents my journey from fundamental audio analysis to real-time embedded DSP development.

> **📌 Note:** All hands-on tasks are designed, structured, and provided by an AI mentour to simulate a production-grade engineering internship. 🙂

## 🗂️ Project structure and roadmap

* **[Phase 1: Environment Setup & Audio Visualization](docs/phase1.md)**
DSP environment setup, extracting audio parameters ("SignalPassport"), creating utilities for spectogram and waveform

* **[Phase 2: Binaural Audiometer & Device Diagnostics](docs/phase2.md)**
Engineering an Audiometer that could be performed at home using the Houston-Westlake method.

* **[Phase 3: Digital Filtering & Phase-Perfect Filter Bank](docs/phase3.md)**
TBD
___

## 🛠️ Combined Tech Stack & Prerequisites

* **Runtime Ecosystem:** Python v3.14+
* **DSP & Math Core:** `numpy`, `scipy.signal`, `librosa`
* **Hardware IO / Drivers:** `sounddevice` (PortAudio C-wrapper)
* **Data Visualization:** `matplotlib`

### 🐧 Linux/PipeWire Configuration
To allow `sounddevice` to dynamically interface with Linux audio streams without triggering device busy blocks:
```bash
sudo apt update && sudo apt install libportaudio2 libasound2-plugins
systemctl --user restart pipewire wireplumber
```