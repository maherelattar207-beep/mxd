# MXD Pro

**MXD Pro** is a professional, ultra-stable multi-GPU, multi-game optimizer and config management tool built with Python and PyQt5.  
It provides advanced, per-game optimization and system profiling for power users and gamers, with robust failsafes, logging, and a modern UI.

---

## Features

- **Multi-GPU Support:** Full detection for NVIDIA, AMD, Intel GPUs, real VRAM/driver info, and monitor details.
- **Multi-Game Profiles:** Optimizer supports dozens (or hundreds) of games, with per-game config logic and schema.
- **Advanced Settings:** Up to 6K, FPS, DLSS/FSR/XeSS, Ray Tracing, VRS, frame cap, dynamic scaling, input lag minimizer, and more.
- **Failsafe & Backup:** Each config write is backed up; instant restore and profile history for every game.
- **Professional UI:** Multi-panel PyQt5 interface with tooltips, logs, and system summary.
- **Logging & Recovery:** Built-in log viewer, export/import of logs and settings, and recovery controls.
- **No 8K Option:** Always operates in a stable, safe range (up to 6K, never above).
- **Extensible:** Easily add more games, GPUs, or settings schemas. Plugin and localization stubs included.

---

## Getting Started

### 1. Clone or Download

Clone this repo or copy all contents into a directory.

### 2. Install Requirements

```bash
pip install PyQt5 psutil wmi screeninfo
```

### 3. Run MXD Pro

```bash
python main.py
```

### 4. Project Structure

```
mxd_pro/
├── main.py
├── core/
│   ├── hardware.py
│   ├── game_profiles.py
│   ├── settings_engine.py
│   ├── logger.py
│   ├── config_writer.py
│   ├── localization.py
│   ├── plugins.py
├── ui/
│   ├── main_window.py
│   ├── optimizer_panel.py
│   ├── sysinfo_panel.py
│   ├── logs_panel.py
├── plugins/
│   └── (your .py plugins here)
├── assets/
│   ├── icons/
│   │   └── app_icon.png
│   ├── themes/
├── mxdpro_backups/
├── mxd_pro.log
├── mxdpro_user_settings.json
└── README.md
```

---

## Extending

- **Add a Game:**  
  Edit `core/game_profiles.py`, add a new `GameProfile` entry.
- **Add More Settings:**  
  Expand the `settings_schema` and UI controls.
- **Custom Icons/Themes:**  
  Place files in `assets/icons` or `assets/themes`.
- **Localization:**  
  Extend `core/localization.py` with more languages.
- **Plugins:**  
  Drop `.py` files in the `plugins/` directory.

---

## License

MIT License

---