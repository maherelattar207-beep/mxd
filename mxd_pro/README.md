# MXD Pro - Ultimate AI Security & Game Optimizer

This is the official repository for the fully merged, restored, and upgraded MXD Pro application.

## Overview

MXD Pro is a professional-grade suite of tools for Windows, combining a military-grade AI-powered antivirus with an advanced game optimization engine. It is designed to be fully offline-capable, modular, and user-friendly.

## Features

- **AI-Powered Security Engine:** Multi-layered threat detection including signatures, heuristics, and behavioral analysis in a sandbox.
- **Offline System Booster:** Tools to clean temporary files and safely stop background processes to enhance system performance.
- **AI-Powered Dynamic Game Optimizer:** Per-game optimization profiles with real-time telemetry and safe rollback capabilities.
- **Universal Help System:** Every setting includes a `?` icon with a clear, concise explanation.
- **Professional UI:** A modern, professional user interface with a Red/Gold/Black theme.
- **Performance Modes:** Auto-detects system hardware to apply a Low-End, Normal, or High-End performance tier.

## How to Run

1.  **Dependencies:** Ensure you have Python 3 and PyQt5 installed. You will also need to install `psutil` and `wmi` (on Windows):
    ```bash
    pip install pyqt5 psutil wmi
    ```
2.  **Execution:** Run the application from the root of the repository using the main entry point:
    ```bash
    python mxd_pro/main.py
    ```

## How to Run Tests

The unit tests are located in the `mxd_pro/tests/` directory. You can run them using Python's built-in `unittest` module:

```bash
python -m unittest discover mxd_pro/tests
```

## Project Structure

- `mxd_pro/core/`: Contains all backend logic (optimizer, security, hardware detection).
- `mxd_pro/ui/`: Contains all PyQt5 UI panels and widgets.
- `mxd_pro/assets/`: For icons, themes, and images.
- `mxd_pro/language/`: For localization files.
- `mxd_pro/settings/`: For user configurations, logs, and quarantine.
- `mxd_pro/docs/`: Contains design documents and file maps.
- `mxd_pro/tests/`: Contains all unit tests.
- `mxd_pro/archive/`: Contains archived versions of old, replaced files.
- `mxd_pro/main.py`: The single entry point for the application.