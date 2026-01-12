# 🖥️ Memory Monitor - Advanced Process Memory Manager

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

Advanced memory monitoring and automatic management tool for Windows applications. Monitors `app.exe` process memory usage and automatically restarts it when limits are exceeded.

---

## 📑 Table of Contents
- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Configuration](#️-configuration)
- [Settings](#-settings)
- [Language Support](#-language-support)
- [Usage Guide](#-usage-guide)
- [Technical Details](#-technical-details)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

---

## ✨ Features

### 🎯 Core Features
- **Real-time Memory Monitoring** - Track `app.exe` memory usage with customizable intervals
- **Automatic Process Restart** - Smart restart when memory limits are exceeded
- **System Tray Integration** - Minimalist background operation with status indicators
- **Multi-language Support** - 100+ languages with automatic downloading
- **Windows Startup Integration** - Auto-start with Windows
- **Loop Protection** - Prevents infinite restart cycles
- **Single Instance** - Ensures only one monitor runs at a time

### 🎨 User Interface
- Modern dark theme with CustomTkinter
- Real-time memory usage visualization
- Color-coded status indicators (Green/Yellow/Red)
- Progress bars and percentage displays
- Floating configuration windows

### 🔒 Safety Features
- Restart cooldown system (max 3 restarts per 60 seconds)
- Automatic restart blocking on loop detection
- Process validation and tracking
- Graceful shutdown handling

---

## 📥 Installation

### System Requirements
- **OS**: Windows 10/11 (64-bit recommended)
- **Python**: 3.7 or higher
- **RAM**: Minimum 100MB free
- **Disk**: 50MB for program + language files

### Required Python Packages

```bash
pip install psutil customtkinter pillow pystray requests
```

**Package Details:**
- `psutil` - Process and system monitoring (memory, CPU, etc.)
- `customtkinter` - Modern GUI framework with dark theme
- `pillow` - Image processing for tray icons
- `pystray` - System tray integration
- `requests` - HTTP requests for downloading language files

### Installation Steps

1. **Download the program:**
   ```bash
   git clone https://github.com/orbiacc/Mathca-Memory-Monitor.git
   cd Mathca-Memory-Monitor
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the program:**
   ```bash
   pythonw memory_monitor.pyw
   ```
   > **Note:** Use `pythonw` instead of `python` to run without console window

4. **First launch:**
   - Program automatically adds itself to Windows startup
   - Downloads default English language file
   - Creates config file in `%USERPROFILE%\app_memory_monitor_config.json`

---

## 🚀 Quick Start

### Basic Usage

1. **Launch the program** - Double-click `memory_monitor.pyw` or run from command line
2. **Check system tray** - Look for the green chip icon 🟢
3. **Right-click tray icon** - Access main menu
4. **Open main window** - Double-click tray icon or select "Open"

### Default Settings

When first launched, the program uses these defaults:

| Setting | Default Value | Description |
|---------|--------------|-------------|
| Memory Limit | 4096 MB (4 GB) | Maximum allowed memory before restart |
| Update Interval | 1 second | How often to check memory usage |
| Auto Restart | Enabled | Automatically restart when limit exceeded |
| Language | English | UI language |
| Windows Startup | Enabled | Auto-start with Windows |

---

## ⚙️ Configuration

### Memory Limit Settings

**Access:** Main Window → Configuration Button

#### Setting Memory Limit
- **Range:** 100 MB - 32,768 MB (32 GB)
- **Recommended Values:**
  - Light apps: 1024-2048 MB (1-2 GB)
  - Medium apps: 2048-4096 MB (2-4 GB)
  - Heavy apps: 4096-8192 MB (4-8 GB)
  - Very heavy apps: 8192+ MB (8+ GB)

```
Example: If you set 2048 MB limit
→ When app.exe reaches 2048 MB
→ Program terminates app.exe
→ Waits 3 seconds
→ Automatically restarts app.exe (if enabled)
```

#### Update Interval
- **Range:** 0.5 - 60 seconds
- **Impact on Performance:**
  - 0.5s = Very responsive, higher CPU usage
  - 1.0s = Balanced (recommended)
  - 2.0s+ = Lower CPU usage, slower detection

**Best Practices:**
```
Fast-growing memory issues → Use 0.5-1s
Stable applications → Use 2-5s
Low-power systems → Use 5-10s
```

### Configuration Window Features

1. **Memory Limit Input**
   - Enter value in MB
   - Auto-converts to GB for easier reading
   - Real-time validation

2. **Update Interval Input**
   - Enter value in seconds
   - Accepts decimal values (e.g., 0.5, 1.5)

3. **Action Buttons**
   - **Save & Apply** - Saves settings and applies immediately
   - **Reset to Defaults** - Restores factory settings
   - **Close** - Exit without saving

4. **Reset Restart Block**
   - Automatically clears restart loop protection
   - Useful after fixing the underlying issue

---

## 🔧 Settings

**Access:** Main Window → Settings Button

### 1. Language Selection 🌐

**100+ languages supported!** 

#### How It Works:
1. Click language dropdown
2. Select your preferred language
3. Program automatically:
   - Downloads language file from GitHub
   - Saves your choice
   - Completely restarts to apply new language

#### Language File Location:
```
%USERPROFILE%\.app_memory_monitor\languages\
├── en.json
├── tr.json
├── de.json
└── ...
```

#### Offline Language Files:
- Files are cached locally after first download
- No internet needed for previously used languages
- Fallback to English if download fails

### 2. Auto Restart 🔄

**Controls automatic process restart behavior**

#### When Enabled (✅):
```
Memory exceeds limit
→ Terminate app.exe
→ Wait 3 seconds
→ Restart app.exe automatically
→ Resume monitoring
```

#### When Disabled (❌):
```
Memory exceeds limit
→ Terminate app.exe
→ Stop (manual restart required)
→ Continue monitoring
```

#### Loop Protection:
- Maximum 3 restarts per 60 seconds
- If exceeded → Auto-restart disabled automatically
- Prevents system instability
- Manual reset available in Configuration

**Use Cases:**
- **Enable:** Production environments, unattended systems
- **Disable:** Testing, debugging, manual control needed

### 3. Windows Startup 🚀

**Automatically launch Memory Monitor with Windows**

#### When Enabled (✅):
- Program starts when Windows boots
- Runs in system tray (minimized)
- No visible window unless you open it

#### When Disabled (❌):
- Manual launch required each time
- Shortcut remains in startup folder but inactive

#### Registry Location:
```
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
Key: AppMemoryMonitor
Value: "C:\path\to\memory_monitor.pyw"
```

#### Manual Control:
```
Enable Startup:
1. Open Settings
2. Click "Windows Startup" button
3. Status changes to "Active" ✅

Disable Startup:
1. Open Settings
2. Click "Windows Startup" button again
3. Status changes to "Passive" ❌
```

---

## 🌐 Language Support

### Supported Language Families

#### 🇪🇺 European Languages (30+)
English, Turkish, German, French, Spanish, Italian, Portuguese, Russian, Dutch, Polish, Ukrainian, Czech, Slovak, Romanian, Hungarian, Bulgarian, Croatian, Serbian, Greek, Swedish, Norwegian, Danish, Finnish, Icelandic, Estonian, Latvian, Lithuanian, Slovenian, Macedonian, Albanian, Bosnian, Maltese, Irish, Welsh, Basque, Catalan, Galician

#### 🌏 Asian Languages (30+)
Chinese, Japanese, Korean, Vietnamese, Thai, Indonesian, Malay, Filipino, Burmese, Khmer, Lao, Sinhala, Bengali, Hindi, Tamil, Telugu, Malayalam, Kannada, Marathi, Gujarati, Punjabi, Urdu, Persian, Pashto, Nepali, Mongolian, Georgian, Armenian, Azerbaijani, Kazakh, Uzbek, Kyrgyz, Tajik, Turkmen

#### 🏜️ Middle Eastern Languages (2)
Arabic, Kurdish

#### 🌍 African Languages (10)
Swahili, Amharic, Hausa, Yoruba, Igbo, Zulu, Xhosa, Afrikaans, Somali, Malagasy

#### 🌎 Regional Variants (7)
Portuguese (Brazil), Spanish (Mexico), Spanish (Argentina), French (Canada), English (US), English (UK), English (Australia)

#### 🗿 Constructed/Historical Languages (2)
Esperanto, Latin

### ⚠️ Blocked Languages
**Hebrew (he/iw)** - Israeli languages are not supported and blocked at code level

---

## 📖 Usage Guide

### Daily Operation

#### 1. System Tray Icons
The tray icon color indicates current status:

| Color | Status | Memory Usage |
|-------|--------|--------------|
| 🟢 Green | Normal | < 75% of limit |
| 🟡 Yellow | Warning | 75-90% of limit |
| 🔴 Red | Critical | 90-100% of limit |
| ⚪ Gray | Not Running | app.exe is not active |

#### 2. Tray Menu Options
- **Open** - Show main window (default double-click action)
- **Settings** - Quick access to settings window
- **Exit** - Completely close Memory Monitor

#### 3. Main Window Information

**Status Section:**
```
🟢 Running - app.exe is active and monitored
⚪ Not Running - app.exe is not found
🚫 Restart Blocked - Loop protection activated
```

**Memory Display:**
- Current usage in MB
- Percentage of limit
- Visual progress bar with color coding
- Limit information (MB and GB)

**Bottom Info Bar:**
- Update interval
- Monitored process name (app.exe)

### Advanced Usage

#### Changing Target Process
Currently hardcoded to `app.exe`. To monitor different process:

1. Open `memory_monitor.pyw` in text editor
2. Find line: `self.process_name = "app.exe"`
3. Change to your target: `self.process_name = "your_app.exe"`
4. Save and restart

#### Custom Memory Limits by Time
Create a scheduled task to modify config:

```python
import json

config_file = r"C:\Users\YourName\app_memory_monitor_config.json"
with open(config_file, 'r') as f:
    config = json.load(f)

# Day shift: 4GB limit
config['max_memory_mb'] = 4096

with open(config_file, 'w') as f:
    json.dump(config, f, indent=4)
```

#### Monitoring Multiple Processes
Run multiple instances with different configs:

```bash
# Copy program
copy memory_monitor.pyw memory_monitor_app2.pyw

# Edit MUTEX_NAME and CONFIG_FILE in new copy
# Change process_name to target different app
```

---

## 🔬 Technical Details

### Architecture

```
Memory Monitor
├── Main Thread (GUI)
├── Monitor Thread (Process checking)
└── Tray Thread (Icon updates)
```

### Memory Measurement
Uses `psutil.Process.memory_full_info().uss`:
- **USS (Unique Set Size)** - Memory unique to this process
- Most accurate for per-process measurement
- Excludes shared libraries

### Files Created

```
%USERPROFILE%\
├── app_memory_monitor_config.json (Settings)
└── .app_memory_monitor\
    └── languages\
        ├── en.json
        ├── tr.json
        └── ...

%TEMP%\
└── memory_monitor_old_pid.txt (Temporary, for restarts)
```

### Registry Entries

```
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
└── AppMemoryMonitor = "C:\...\memory_monitor.pyw"
```

### Network Usage
- **Language downloads only** (first use per language)
- GitHub API for language list (once per launch)
- No telemetry, analytics, or tracking
- All monitoring is 100% local

---

## 🐛 Troubleshooting

### Common Issues

#### ❌ "Already Running" Message
**Cause:** Another instance is active

**Solutions:**
1. Check system tray for existing icon
2. End task in Task Manager (pythonw.exe)
3. Restart computer if persistent

#### ❌ Program Won't Start
**Cause:** Missing dependencies

**Solutions:**
```bash
# Reinstall all packages
pip uninstall psutil customtkinter pillow pystray requests
pip install psutil customtkinter pillow pystray requests

# Use specific versions if issues persist
pip install psutil==5.9.5 customtkinter==5.2.0
```

#### ❌ Language Won't Change
**Cause:** Download failed or network issue

**Solutions:**
1. Check internet connection
2. Manually download from GitHub
3. Place in `%USERPROFILE%\.app_memory_monitor\languages\`
4. Restart program

#### ❌ Auto Restart Not Working
**Possible Causes:**
1. Loop protection activated → Reset in Configuration
2. app.exe path changed → Restart Monitor once
3. Auto-restart disabled → Check Settings

#### ❌ High CPU Usage
**Cause:** Update interval too short

**Solution:**
- Increase update interval to 2-5 seconds
- Close other monitoring tools
- Check for process conflicts

#### ⚠️ "Restart Blocked" Message
**Cause:** Too many restarts in short time (loop protection)

**Solution:**
1. Fix the underlying memory issue in app.exe
2. Increase memory limit
3. Open Configuration → Save & Apply (resets block)
4. Or disable auto-restart temporarily

---

## 🤝 Contributing

### Creating Language Files

1. **Fork the repository**
2. **Create new language file:** `languages/xx.json` (xx = language code)
3. **Use this template:**

```json
{
  "app_title": "Memory Monitor",
  "memory_monitor": "Memory Monitor",
  "running": "Running",
  "not_running": "Not Running",
  "restart_blocked": "Restart Blocked",
  "status": "Status",
  "memory_usage": "Memory Usage",
  "limit": "Limit",
  "configuration": "Configuration",
  "settings": "Settings",
  "program_settings": "Program Settings",
  "close": "Close",
  "hide": "Hide",
  "open": "Open",
  "exit": "Exit",
  "save_apply": "Save & Apply",
  "reset_defaults": "Reset to Defaults",
  "language_setting": "Language",
  "language_desc": "Select your preferred language. Program will restart to apply changes.",
  "auto_restart": "Automatic Restart",
  "auto_restart_desc": "Automatically restart app.exe when memory limit is exceeded.",
  "on": "ON",
  "off": "OFF",
  "enabled": "Enabled",
  "disabled": "Disabled",
  "active": "Active",
  "passive": "Passive",
  "windows_startup": "Windows Startup",
  "windows_startup_desc": "Launch Memory Monitor automatically when Windows starts.",
  "memory_limit": "Memory Limit",
  "memory_limit_desc": "Maximum memory allowed for app.exe before automatic restart.",
  "update_interval_label": "Update Interval",
  "update_interval": "Update Interval",
  "update_interval_desc": "How often to check memory usage (in seconds).",
  "seconds": "seconds",
  "settings_saved": "Settings saved!\n\nMemory Limit: {limit} MB ({gb:.2f} GB)\nUpdate Interval: {interval} seconds",
  "success": "Success",
  "error": "Error",
  "limit_range_error": "Memory limit must be between 100-32768 MB!",
  "interval_range_error": "Update interval must be between 0.5-60 seconds!",
  "invalid_number": "Please enter a valid number!",
  "restart_loop_blocked_title": "Auto-Restart Blocked!",
  "restart_loop_blocked_msg": "app.exe has been restarted {count} times in {cooldown} seconds!\n\nThis may indicate a memory leak or insufficient limit.\n\nCurrent limit: {limit} MB\n\nAuto-restart is now DISABLED.\nTo re-enable, fix the issue and click 'Save & Apply' in Configuration."
}
```

4. **Test thoroughly:** Ensure all UI elements display correctly
5. **Submit pull request:** With screenshots showing the translated UI

### Language Code Reference
Use standard ISO 639-1 codes:
- `en` = English
- `tr` = Turkish
- `de` = German
- `fr` = French
- `es` = Spanish
- etc.

Regional variants use hyphen:
- `pt-br` = Portuguese (Brazil)
- `en-us` = English (US)
- `zh-cn` = Chinese (Simplified)

---

## 📄 License

MIT License - Feel free to modify and distribute

---

## 🔗 Links

- **GitHub Repository:** https://github.com/orbiacc/Mathca-Memory-Monitor
- **Issue Tracker:** https://github.com/orbiacc/Mathca-Memory-Monitor/issues
- **Language Files:** https://github.com/orbiacc/Mathca-Memory-Monitor/tree/main/languages

---

## 📊 Statistics

- **Total Lines of Code:** ~1000+
- **Supported Languages:** 100+
- **File Size:** ~50KB (.pyw) + language files
- **Memory Footprint:** ~30-50MB RAM
- **CPU Usage:** <1% (at 1s interval)

---

**Made with ❤️ for efficient memory management**

*Last Updated: January 2025*
