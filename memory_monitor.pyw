#This code is open source. If you want to improve it and share it, please share it as open source and give me credit.
#It's 3:10 a.m. in my country right now, and I'm dealing with this, bruhhh
#I don't know if this will be useful o_O
#However, since the “matcha” issue hasn't been resolved for me, this works. The backend doesn't consume too much memory, or so it seems.
#https://discord.gg/BJwSQzGRwH
#I'm sharing this on the script channel because there's nowhere else to share it. If you agree that it's not a virus, you can use it. OPEN SOURCE!
#This code is open source. If you want to improve it and share it, please share it as open source and give me credit.
#It's 3:10 a.m. in my country right now, and I'm dealing with this, bruhhh
#I don't know if this will be useful o_O
#However, since the “matcha” issue hasn't been resolved for me, this works. The backend doesn't consume too much memory, or so it seems.
#https://discord.gg/BJwSQzGRwH
#I'm sharing this on the script channel because there's nowhere else to share it. If you agree that it's not a virus, you can use it. OPEN SOURCE!
import psutil
import time
import os
import sys
import ctypes
import json
from threading import Thread
import customtkinter as ctk
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import winreg
import atexit
import requests

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

import gc
gc.enable()
gc.set_threshold(700, 10, 10)

CONFIG_FILE = os.path.join(os.path.expanduser("~"), "app_memory_monitor_config.json")
LANGUAGES_DIR = os.path.join(os.path.expanduser("~"), ".app_memory_monitor", "languages")
MUTEX_NAME = "Global\\AppMemoryMonitorMutex_UNIQUE_12345"
GITHUB_LANGUAGES_URL = "https://raw.githubusercontent.com/orbiacc/Mathca-Memory-Monitor/main/languages/"  #If you wish, you can use the same repository on your own GitHub.

mutex_handle = None
CURRENT_LANG = {}

def release_mutex():
    global mutex_handle
    if mutex_handle:
        try:
            ctypes.windll.kernel32.ReleaseMutex(mutex_handle)
            ctypes.windll.kernel32.CloseHandle(mutex_handle)
            mutex_handle = None
        except:
            pass

def check_single_instance():
    global mutex_handle
    
    pid_file = os.path.join(os.environ['TEMP'], 'memory_monitor_old_pid.txt')
    if os.path.exists(pid_file):
        try:
            with open(pid_file, 'r') as f:
                old_pid = int(f.read().strip())
            
            try:
                old_process = psutil.Process(old_pid)
                for i in range(10):
                    if not old_process.is_running():
                        break
                    time.sleep(0.5)
            except:
                pass
            
            os.remove(pid_file)
        except:
            pass
        
        try:
            mutex_handle = ctypes.windll.kernel32.CreateMutexW(None, True, MUTEX_NAME)
            atexit.register(release_mutex)
            return True
        except:
            return False
    
    try:
        mutex_handle = ctypes.windll.kernel32.CreateMutexW(None, True, MUTEX_NAME)
        last_error = ctypes.windll.kernel32.GetLastError()
        
        if last_error == 183:
            ctypes.windll.user32.MessageBoxW(
                0,
                "app.exe Memory Monitor is already running!\n\nCheck system tray.",  #No matter what language you use, this will not change.
                "Already Running",
                0x30 | 0x40000
            )
            release_mutex()
            os._exit(1)
        
        atexit.register(release_mutex)
        return True
    except:
        return False

def download_language_file(lang_code):
    try:
        os.makedirs(LANGUAGES_DIR, exist_ok=True)
        url = f"https://raw.githubusercontent.com/orbiacc/Mathca-Memory-Monitor/main/languages/{lang_code}.json"   #If you are using a different repository, change this link!
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            lang_file = os.path.join(LANGUAGES_DIR, f"{lang_code}.json")
            with open(lang_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            return True
        return False
    except Exception as e:
        return False

def load_language(lang_code):
    global CURRENT_LANG
    
    lang_file = os.path.join(LANGUAGES_DIR, f"{lang_code}.json")
    
    if os.path.exists(lang_file):
        try:
            with open(lang_file, 'r', encoding='utf-8') as f:
                CURRENT_LANG = json.load(f)
            return True
        except:
            pass
    
    if download_language_file(lang_code):
        try:
            with open(lang_file, 'r', encoding='utf-8') as f:
                CURRENT_LANG = json.load(f)
            return True
        except:
            pass
    
    if lang_code != "en":
        lang_code = "en"
        lang_file = os.path.join(LANGUAGES_DIR, f"{lang_code}.json")
        
        if os.path.exists(lang_file):
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    CURRENT_LANG = json.load(f)
                return True
            except:
                pass
        
        download_language_file("en")
        if os.path.exists(lang_file):
            try:
                with open(lang_file, 'r', encoding='utf-8') as f:
                    CURRENT_LANG = json.load(f)
                return True
            except:
                pass
    
    CURRENT_LANG = {
        "app_title": "Memory Monitor",
        "running": "Running",
        "not_running": "Not Running",
        "restart_blocked": "Restart Blocked",
        "close": "Close",
        "memory_usage": "Memory Usage",
        "limit": "Limit",
        "configuration": "Configuration",
        "settings": "Settings",
        "hide": "Hide"
    }
    return False

def t(key):
    return CURRENT_LANG.get(key, key)

def get_available_languages(): #DO NOT TOUCH THIS PART No support for Israel!
    try:
        url = "https://api.github.com/repos/orbiacc/Mathca-Memory-Monitor/contents/languages" #If you are using a different repository, change this link!
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            files = response.json()
            langs = []
            blocked_langs = ["he", "iw"]
            
            for file in files:
                if file['name'].endswith('.json'):
                    code = file['name'].replace('.json', '')
                    if code not in blocked_langs:
                        langs.append(code)
            return langs if langs else ["en", "tr"]
        return ["en", "tr"]
    except Exception as e:
        return ["en", "tr"]

def add_to_startup():
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        
        script_path = os.path.abspath(sys.argv[0])
        
        if script_path.endswith('.pyw'):
            python_dir = os.path.dirname(sys.executable)
            pythonw_exe = os.path.join(python_dir, 'pythonw.exe')
            
            if not os.path.exists(pythonw_exe):
                pythonw_exe = sys.executable
            
            command = f'"{pythonw_exe}" "{script_path}"'
        else:
            command = f'"{script_path}"'
        
        winreg.SetValueEx(key, "AppMemoryMonitor", 0, winreg.REG_SZ, command)
        winreg.CloseKey(key)
        return True
    except:
        return False

def remove_from_startup():
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, "AppMemoryMonitor")
        winreg.CloseKey(key)
        return True
    except:
        return False

def is_in_startup():
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
        winreg.QueryValueEx(key, "AppMemoryMonitor")
        winreg.CloseKey(key)
        return True
    except:
        return False

class MemoryMonitor:
    def __init__(self):
        self.monitoring = True
        self.process_name = "app.exe"  #If you want to use another program, type it in, for example, example.exe
        
        self.default_config = {        #If you wish, you can change the default values.
            "max_memory_mb": 4096,
            "update_interval": 1,
            "auto_restart": True,
            "language": "en"
        }
        
        self.load_config()
        load_language(self.language)
        
        self.current_memory = 0
        self.process_running = False
        self.window = None
        self.tray_icon = None
        self.window_open = False
        self.tracked_pid = None
        self.settings_window = None
        self.config_window = None
        self.user_closed = False
        self.app_path = None
        
        self.restart_history = []
        self.restart_cooldown = 60
        self.max_restarts_in_cooldown = 3
        self.auto_restart_blocked = False
        
        self.show_window_on_start = self.check_if_restart()
    
    def check_if_restart(self):
        pid_file = os.path.join(os.environ['TEMP'], 'memory_monitor_old_pid.txt')
        return os.path.exists(pid_file)
    
    def restart_program(self):
        try:
            import subprocess
            script_path = os.path.abspath(sys.argv[0])
            current_pid = os.getpid()
            
            pid_file = os.path.join(os.environ['TEMP'], 'memory_monitor_old_pid.txt')
            with open(pid_file, 'w') as f:
                f.write(str(current_pid))
            
            if script_path.endswith('.py') or script_path.endswith('.pyw'):
                python_exe = sys.executable
                if script_path.endswith('.pyw'):
                    python_exe = python_exe.replace('python.exe', 'pythonw.exe')
                
                subprocess.Popen(
                    [python_exe, script_path, '--show-window'],
                    creationflags=subprocess.CREATE_NEW_CONSOLE,
                    close_fds=True
                )
            else:
                subprocess.Popen(
                    [script_path, '--show-window'],
                    creationflags=subprocess.CREATE_NEW_CONSOLE,
                    close_fds=True
                )
            
            time.sleep(1)
            
            self.monitoring = False
            
            if self.tray_icon:
                try:
                    self.tray_icon.visible = False
                    self.tray_icon.stop()
                except:
                    pass
            
            if self.settings_window:
                try:
                    self.settings_window.destroy()
                except:
                    pass
            
            if self.config_window:
                try:
                    self.config_window.destroy()
                except:
                    pass
            
            if self.window:
                try:
                    self.window.destroy()
                except:
                    pass
            
            release_mutex()
            os._exit(0)
            
        except Exception as e:
            release_mutex()
            os._exit(0)
        
    def load_config(self):
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.max_memory_mb = config.get('max_memory_mb', self.default_config['max_memory_mb'])
                    self.update_interval = config.get('update_interval', self.default_config['update_interval'])
                    self.auto_restart = config.get('auto_restart', self.default_config['auto_restart'])
                    self.language = config.get('language', self.default_config['language'])
            else:
                self.max_memory_mb = self.default_config['max_memory_mb']
                self.update_interval = self.default_config['update_interval']
                self.auto_restart = self.default_config['auto_restart']
                self.language = self.default_config['language']
                self.save_config()
        except:
            self.max_memory_mb = self.default_config['max_memory_mb']
            self.update_interval = self.default_config['update_interval']
            self.auto_restart = self.default_config['auto_restart']
            self.language = self.default_config['language']
    
    def save_config(self):
        try:
            config = {
                'max_memory_mb': self.max_memory_mb,
                'update_interval': self.update_interval,
                'auto_restart': self.auto_restart,
                'language': self.language
            }
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
            return True
        except:
            return False
    
    def mb_to_bytes(self, mb):
        return mb * 1024 * 1024
    
    def create_tray_icon(self, color="green"):
        width, height = 64, 64
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        dc = ImageDraw.Draw(image)
        
        colors = {
            "green": "#10b981",
            "yellow": "#f59e0b",
            "red": "#ef4444",
            "gray": "#6b7280"
        }
        
        color_hex = colors.get(color, colors["gray"])
        
        dc.ellipse([4, 4, 60, 60], fill="#1f2937")
        
        chip_left = 18
        chip_right = 46
        chip_top = 20
        chip_bottom = 44
        
        dc.rounded_rectangle(
            [chip_left, chip_top, chip_right, chip_bottom],
            radius=3,
            fill=color_hex
        )
        
        pin_width = 3
        pin_height = 4
        pin_spacing = 5
        
        for i in range(4):
            pin_x = chip_left + 2 + i * pin_spacing
            dc.rectangle(
                [pin_x, chip_top - pin_height, pin_x + pin_width, chip_top],
                fill=color_hex
            )
            dc.rectangle(
                [pin_x, chip_bottom, pin_x + pin_width, chip_bottom + pin_height],
                fill=color_hex
            )
        
        line_start = chip_left + 6
        line_end = chip_right - 6
        line_y1 = 28
        line_y2 = 32
        line_y3 = 36
        
        dc.line([line_start, line_y1, line_end, line_y1], fill="#1f2937", width=2)
        dc.line([line_start, line_y2, line_end, line_y2], fill="#1f2937", width=2)
        dc.line([line_start, line_y3, line_end, line_y3], fill="#1f2937", width=2)
        
        dc.ellipse([2, 2, 62, 62], outline=color_hex, width=2)
        
        return image
    
    def get_status_color(self):
        if not self.process_running:
            return "gray"
        
        usage_percent = (self.current_memory / self.max_memory_mb) * 100
        if usage_percent < 75:
            return "green"
        elif usage_percent < 90:
            return "yellow"
        else:
            return "red"
    
    def monitor_process(self):
        while self.monitoring:
            try:
                max_memory_bytes = self.mb_to_bytes(self.max_memory_mb)
                
                if self.tracked_pid:
                    try:
                        proc = psutil.Process(self.tracked_pid)
                        if proc.name().lower() == self.process_name.lower():
                            try:
                                full_mem = proc.memory_full_info()
                                memory_usage = full_mem.uss
                            except (AttributeError, psutil.AccessDenied):
                                memory_usage = proc.memory_info().rss
                            
                            memory_mb = memory_usage / (1024 * 1024)
                            self.current_memory = memory_mb
                            self.process_running = True
                            self.user_closed = False
                            
                            if memory_usage > max_memory_bytes:
                                if not self.app_path:
                                    try:
                                        self.app_path = proc.exe()
                                    except:
                                        pass
                                
                                proc.terminate()
                                time.sleep(2)
                                if proc.is_running():
                                    proc.kill()
                                
                                self.tracked_pid = None
                                self.process_running = False
                                self.current_memory = 0
                                
                                if self.auto_restart and self.app_path:
                                    time.sleep(3)
                                    self.restart_app()
                        else:
                            self.tracked_pid = None
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        self.tracked_pid = None
                        self.process_running = False
                        self.current_memory = 0
                
                if not self.tracked_pid:
                    for proc in psutil.process_iter(['pid', 'name']):
                        try:
                            if proc.info['name'].lower() == self.process_name.lower():
                                self.tracked_pid = proc.info['pid']
                                
                                if not self.app_path:
                                    try:
                                        p = psutil.Process(self.tracked_pid)
                                        self.app_path = p.exe()
                                    except:
                                        pass
                                break
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            pass
                    
                    if not self.tracked_pid:
                        self.process_running = False
                        self.current_memory = 0
                
            except Exception as e:
                pass
            
            if self.window_open and self.window:
                try:
                    self.window.after(0, self.update_gui)
                except:
                    pass
            
            time.sleep(self.update_interval)
            
            if not hasattr(self, '_gc_counter'):
                self._gc_counter = 0
            self._gc_counter += 1
            if self._gc_counter >= 10:
                gc.collect()
                self._gc_counter = 0
    
    def restart_app(self):
        if not self.app_path or not os.path.exists(self.app_path):
            return
        
        if self.auto_restart_blocked:
            return
        
        current_time = time.time()
        self.restart_history = [t for t in self.restart_history if current_time - t < self.restart_cooldown]
        
        if len(self.restart_history) >= self.max_restarts_in_cooldown:
            self.auto_restart_blocked = True
            
            ctypes.windll.user32.MessageBoxW(
                0,
                t("restart_loop_blocked_msg").format(
                    cooldown=self.restart_cooldown,
                    count=len(self.restart_history),
                    limit=self.max_memory_mb
                ),
                t("restart_loop_blocked_title"),
                0x30 | 0x40000
            )
            return
        
        self.restart_history.append(current_time)
        
        try:
            import subprocess
            subprocess.Popen([self.app_path], shell=True)
        except:
            pass
    
    def update_gui(self):
        if not self.window_open:
            return
            
        try:
            if self.process_running:
                usage_percent = (self.current_memory / self.max_memory_mb) * 100
                
                if self.auto_restart_blocked:
                    self.status_label.configure(text=f"🚫 {t('restart_blocked')}", text_color="#ef4444")
                else:
                    self.status_label.configure(text=f"🟢 {t('running')}", text_color="#10b981")
                
                self.memory_label.configure(text=f"{self.current_memory:.1f} MB")
                self.progress_bar.set(usage_percent / 100)
                self.percent_label.configure(text=f"{usage_percent:.1f}%")
                
                if usage_percent >= 90:
                    self.progress_bar.configure(progress_color="#ef4444")
                    self.percent_label.configure(text_color="#ef4444")
                elif usage_percent >= 75:
                    self.progress_bar.configure(progress_color="#f59e0b")
                    self.percent_label.configure(text_color="#f59e0b")
                else:
                    self.progress_bar.configure(progress_color="#10b981")
                    self.percent_label.configure(text_color="#10b981")
            else:
                if self.auto_restart_blocked:
                    self.status_label.configure(text=f"🚫 {t('restart_blocked')}", text_color="#ef4444")
                else:
                    self.status_label.configure(text=f"⚪ {t('not_running')}", text_color="#6b7280")
                self.memory_label.configure(text="0 MB")
                self.progress_bar.set(0)
                self.percent_label.configure(text="0%", text_color="#6b7280")
            
            if hasattr(self, 'limit_info_label'):
                self.limit_info_label.configure(text=f"{t('limit')}: {self.max_memory_mb} MB ({self.max_memory_mb/1024:.1f} GB)")
            
            if hasattr(self, 'interval_info_label'):
                self.interval_info_label.configure(text=f"{t('update_interval')}: {self.update_interval}s • {self.process_name}")
        except:
            pass
    
    def show_window(self):
        try:
            if self.window_open and self.window and self.window.winfo_exists():
                self.window.deiconify()
                self.window.lift()
                self.window.focus_force()
                return
        except:
            pass
        
        if not self.window_open:
            self.window = None
            Thread(target=self.create_window, daemon=True).start()
    
    def hide_window(self):
        if self.window and self.window_open:
            self.window.withdraw()
    
    def show_config(self):
        try:
            if self.config_window and self.config_window.winfo_exists():
                self.config_window.lift()
                self.config_window.focus_force()
                self.config_window.attributes('-topmost', True)
                self.config_window.after(100, lambda: self.config_window.attributes('-topmost', False))
                return
        except:
            self.config_window = None
        
        self.config_window = ctk.CTkToplevel(self.window if self.window else None)
        self.config_window.title(f"⚙️ {t('configuration')}")
        self.config_window.geometry("520x750")
        self.config_window.resizable(False, False)
        self.config_window.attributes('-topmost', True)
        self.config_window.after(200, lambda: self.config_window.attributes('-topmost', False))
        
        main = ctk.CTkScrollableFrame(self.config_window, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        header = ctk.CTkFrame(main, fg_color="#1f2937", corner_radius=15)
        header.pack(fill="x", pady=(5, 15))
        
        ctk.CTkLabel(header, text="⚙️", font=ctk.CTkFont(size=40)).pack(pady=(20, 5))
        ctk.CTkLabel(header, text=t('configuration'), font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(0, 20))
        
        limit_card = ctk.CTkFrame(main, fg_color="#1f2937", corner_radius=12)
        limit_card.pack(fill="x", pady=10)
        
        limit_inner = ctk.CTkFrame(limit_card, fg_color="transparent")
        limit_inner.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(limit_inner, text=f"💾 {t('memory_limit')}", font=ctk.CTkFont(size=14, weight="bold"), anchor="w").pack(fill="x", pady=(0, 5))
        ctk.CTkLabel(limit_inner, text=t('memory_limit_desc'), font=ctk.CTkFont(size=11), text_color="#9ca3af", anchor="w").pack(fill="x", pady=(0, 12))
        
        limit_frame = ctk.CTkFrame(limit_inner, fg_color="transparent")
        limit_frame.pack(fill="x", pady=(0, 5))
        
        limit_entry = ctk.CTkEntry(limit_frame, width=300, height=40, font=ctk.CTkFont(size=14))
        limit_entry.pack(side="left", padx=(0, 10))
        limit_entry.insert(0, str(self.max_memory_mb))
        
        ctk.CTkLabel(limit_frame, text="MB", font=ctk.CTkFont(size=14, weight="bold"), text_color="#9ca3af").pack(side="left")
        
        limit_gb_label = ctk.CTkLabel(limit_inner, text=f"≈ {self.max_memory_mb/1024:.2f} GB", font=ctk.CTkFont(size=12), text_color="#10b981", anchor="w")
        limit_gb_label.pack(fill="x", pady=(5, 0))
        
        def update_gb(*args):
            try:
                mb = int(limit_entry.get())
                limit_gb_label.configure(text=f"≈ {mb/1024:.2f} GB")
            except:
                limit_gb_label.configure(text="≈ 0.00 GB")
        
        limit_entry.bind("<KeyRelease>", update_gb)
        
        interval_card = ctk.CTkFrame(main, fg_color="#1f2937", corner_radius=12)
        interval_card.pack(fill="x", pady=10)
        
        interval_inner = ctk.CTkFrame(interval_card, fg_color="transparent")
        interval_inner.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(interval_inner, text=f"⚡ {t('update_interval_label')}", font=ctk.CTkFont(size=14, weight="bold"), anchor="w").pack(fill="x", pady=(0, 5))
        ctk.CTkLabel(interval_inner, text=t('update_interval_desc'), font=ctk.CTkFont(size=11), text_color="#9ca3af", anchor="w").pack(fill="x", pady=(0, 12))
        
        interval_frame = ctk.CTkFrame(interval_inner, fg_color="transparent")
        interval_frame.pack(fill="x", pady=(0, 5))
        
        interval_entry = ctk.CTkEntry(interval_frame, width=300, height=40, font=ctk.CTkFont(size=14))
        interval_entry.pack(side="left", padx=(0, 10))
        interval_entry.insert(0, str(self.update_interval))
        
        ctk.CTkLabel(interval_frame, text=t('seconds'), font=ctk.CTkFont(size=14, weight="bold"), text_color="#9ca3af").pack(side="left")
        
        separator = ctk.CTkFrame(main, height=2, fg_color="#374151")
        separator.pack(fill="x", pady=15)
        
        button_frame = ctk.CTkFrame(main, fg_color="transparent")
        button_frame.pack(fill="x", pady=10, padx=5)
        
        def save_and_apply():
            try:
                new_limit = int(limit_entry.get())
                if new_limit < 100 or new_limit > 32768:
                    ctypes.windll.user32.MessageBoxW(0, t('limit_range_error'), t('error'), 0x10)
                    return
                
                new_interval = float(interval_entry.get())
                if new_interval < 0.5 or new_interval > 60:
                    ctypes.windll.user32.MessageBoxW(0, t('interval_range_error'), t('error'), 0x10)
                    return
                
                self.max_memory_mb = new_limit
                self.update_interval = new_interval
                self.save_config()
                
                if self.auto_restart_blocked:
                    self.auto_restart_blocked = False
                    self.restart_history = []
                
                ctypes.windll.user32.MessageBoxW(
                    0,
                    t('settings_saved').format(limit=new_limit, gb=new_limit/1024, interval=new_interval),
                    t('success'),
                    0x40
                )
                
                self.config_window.destroy()
                self.config_window = None
                
                if self.window_open and self.window:
                    self.update_gui()
                    
            except ValueError:
                ctypes.windll.user32.MessageBoxW(0, t('invalid_number'), t('error'), 0x10)
        
        ctk.CTkButton(
            button_frame,
            text=f"💾 {t('save_apply')}",
            command=save_and_apply,
            width=460,
            height=55,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#10b981",
            hover_color="#059669",
            corner_radius=10
        ).pack(pady=8)
        
        def reset_defaults():
            limit_entry.delete(0, 'end')
            limit_entry.insert(0, str(self.default_config['max_memory_mb']))
            interval_entry.delete(0, 'end')
            interval_entry.insert(0, str(self.default_config['update_interval']))
            limit_gb_label.configure(text=f"≈ {self.default_config['max_memory_mb']/1024:.2f} GB")
        
        ctk.CTkButton(
            button_frame,
            text=f"🔄 {t('reset_defaults')}",
            command=reset_defaults,
            width=460,
            height=48,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#f59e0b",
            hover_color="#d97706",
            corner_radius=10
        ).pack(pady=8)
        
        def close_config():
            self.config_window.destroy()
            self.config_window = None
        
        ctk.CTkButton(
            button_frame,
            text=t('close'),
            command=close_config,
            width=460,
            height=48,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#4b5563",
            hover_color="#374151",
            corner_radius=10
        ).pack(pady=8)
    
    def show_settings(self):
        try:
            if self.settings_window and self.settings_window.winfo_exists():
                self.settings_window.attributes('-topmost', True)
                self.settings_window.lift()
                self.settings_window.focus_force()
                self.settings_window.after(100, lambda: self.settings_window.attributes('-topmost', False))
                return
        except:
            self.settings_window = None
        
        self.settings_window = ctk.CTkToplevel(self.window if self.window else None)
        self.settings_window.title(f"🚀 {t('settings')}")
        self.settings_window.geometry("450x700")
        self.settings_window.resizable(False, False)
        
        self.settings_window.attributes('-topmost', True)
        self.settings_window.lift()
        self.settings_window.focus_force()
        self.settings_window.grab_set()
        self.settings_window.after(300, lambda: self.settings_window.attributes('-topmost', False))
        
        container = ctk.CTkFrame(self.settings_window, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=25, pady=25)
        
        header = ctk.CTkFrame(container, fg_color="#1f2937", corner_radius=15)
        header.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(header, text="🚀", font=ctk.CTkFont(size=40)).pack(pady=(20, 5))
        ctk.CTkLabel(header, text=t('program_settings'), font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(0, 20))
        
        main = ctk.CTkScrollableFrame(container, fg_color="transparent")
        main.pack(fill="both", expand=True, pady=(0, 10))
        
        lang_card = ctk.CTkFrame(main, fg_color="#1f2937", corner_radius=12)
        lang_card.pack(fill="x", pady=10)
        
        lang_inner = ctk.CTkFrame(lang_card, fg_color="transparent")
        lang_inner.pack(fill="x", padx=20, pady=20)
        
        lang_info = ctk.CTkFrame(lang_inner, fg_color="transparent")
        lang_info.pack(fill="x", pady=(0, 12))
        
        ctk.CTkLabel(lang_info, text=f"🌍 {t('language_setting')}", font=ctk.CTkFont(size=14, weight="bold"), anchor="w").pack(side="left")
        
        ctk.CTkLabel(lang_inner, text=t('language_desc'), font=ctk.CTkFont(size=11), text_color="#6b7280", wraplength=350, justify="left").pack(pady=(0, 12), anchor="w")
        
        available_langs = get_available_languages() #All of these languages aren't listed here https://github.com/orbiacc/Mathca-Memory-Monitor/tree/main/languages, but if you add them, why not? :D
        lang_names = {
            "en": "🇬🇧 English", "tr": "🇹🇷 Türkçe", "de": "🇩🇪 Deutsch", "fr": "🇫🇷 Français", "es": "🇪🇸 Español",
            "it": "🇮🇹 Italiano", "pt": "🇵🇹 Português", "ru": "🇷🇺 Русский", "nl": "🇳🇱 Nederlands", "pl": "🇵🇱 Polski",
            "uk": "🇺🇦 Українська", "cs": "🇨🇿 Čeština", "sk": "🇸🇰 Slovenčina", "ro": "🇷🇴 Română", "hu": "🇭🇺 Magyar",
            "bg": "🇧🇬 Български", "hr": "🇭🇷 Hrvatski", "sr": "🇷🇸 Српски", "el": "🇬🇷 Ελληνικά", "sv": "🇸🇪 Svenska",
            "no": "🇳🇴 Norsk", "da": "🇩🇰 Dansk", "fi": "🇫🇮 Suomi", "is": "🇮🇸 Íslenska", "et": "🇪🇪 Eesti",
            "lv": "🇱🇻 Latviešu", "lt": "🇱🇹 Lietuvių", "sl": "🇸🇮 Slovenščina", "mk": "🇲🇰 Македонски", "sq": "🇦🇱 Shqip",
            "bs": "🇧🇦 Bosanski", "mt": "🇲🇹 Malti", "ga": "🇮🇪 Gaeilge", "cy": "🏴󠁧󠁢󠁷󠁬󠁳󠁿 Cymraeg", "eu": "🏴 Euskara",
            "ca": "🏴 Català", "gl": "🏴 Galego", "zh": "🇨🇳 中文", "ja": "🇯🇵 日本語", "ko": "🇰🇷 한국어",
            "vi": "🇻🇳 Tiếng Việt", "th": "🇹🇭 ไทย", "id": "🇮🇩 Bahasa Indonesia", "ms": "🇲🇾 Bahasa Melayu",
            "tl": "🇵🇭 Filipino", "my": "🇲🇲 မြန်မာ", "km": "🇰🇭 ខ្មែរ", "lo": "🇱🇦 ລາວ", "si": "🇱🇰 සිංහල",
            "bn": "🇧🇩 বাংলা", "hi": "🇮🇳 हिन्दी", "ta": "🇮🇳 தமிழ்", "te": "🇮🇳 తెలుగు", "ml": "🇮🇳 മലയാളം",
            "kn": "🇮🇳 ಕನ್ನಡ", "mr": "🇮🇳 मराठी", "gu": "🇮🇳 ગુજરાતી", "pa": "🇮🇳 ਪੰਜਾਬੀ", "ur": "🇵🇰 اردو",
            "fa": "🇮🇷 فارسی", "ps": "🇦🇫 پښتو", "ne": "🇳🇵 नेपाली", "mn": "🇲🇳 Монгол", "ka": "🇬🇪 ქართული",
            "hy": "🇦🇲 Հայերեն", "az": "🇦🇿 Azərbaycan", "kk": "🇰🇿 Қазақ", "uz": "🇺🇿 Oʻzbek", "ky": "🇰🇬 Кыргызча",
            "tg": "🇹🇯 Тоҷикӣ", "tk": "🇹🇲 Türkmen", "ar": "🇸🇦 العربية", "ku": "🏴 کوردی", "sw": "🇰🇪 Kiswahili",
            "am": "🇪🇹 አማርኛ", "ha": "🇳🇬 Hausa", "yo": "🇳🇬 Yorùbá", "ig": "🇳🇬 Igbo", "zu": "🇿🇦 isiZulu",
            "xh": "🇿🇦 isiXhosa", "af": "🇿🇦 Afrikaans", "so": "🇸🇴 Soomaali", "mg": "🇲🇬 Malagasy",
            "pt-br": "🇧🇷 Português (Brasil)", "es-mx": "🇲🇽 Español (México)", "es-ar": "🇦🇷 Español (Argentina)",
            "fr-ca": "🇨🇦 Français (Canada)", "en-us": "🇺🇸 English (US)", "en-gb": "🇬🇧 English (UK)",
            "en-au": "🇦🇺 English (Australia)", "eo": "🌍 Esperanto", "la": "🏛️ Latina"
        }
        
        lang_dropdown = ctk.CTkOptionMenu(
            lang_inner,
            values=[lang_names.get(l, l) for l in available_langs],
            width=380,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#10b981",
            button_color="#059669",
            button_hover_color="#047857"
        )
        
        current_lang_name = lang_names.get(self.language, self.language)
        lang_dropdown.set(current_lang_name)
        lang_dropdown.pack()
        
        def change_language(choice):
            for code, name in lang_names.items():
                if name == choice:
                    if code == self.language:
                        return
                    
                    self.language = code
                    self.save_config()
                    
                    ctypes.windll.user32.MessageBoxW(
                        0,
                        f"Language changed to {name}\n\nProgram will restart completely.",
                        "Language Changed - Restarting",
                        0x40
                    )
                    
                    self.restart_program()
                    break
        
        lang_dropdown.configure(command=change_language)
        
        restart_card = ctk.CTkFrame(main, fg_color="#1f2937", corner_radius=12)
        restart_card.pack(fill="x", pady=10)
        
        restart_inner = ctk.CTkFrame(restart_card, fg_color="transparent")
        restart_inner.pack(fill="x", padx=20, pady=20)
        
        restart_info = ctk.CTkFrame(restart_inner, fg_color="transparent")
        restart_info.pack(fill="x", pady=(0, 12))
        
        ctk.CTkLabel(restart_info, text=f"🔄 {t('auto_restart')}", font=ctk.CTkFont(size=14, weight="bold"), anchor="w").pack(side="left")
        
        restart_status = t('on') if self.auto_restart else t('off')
        restart_color = "#10b981" if self.auto_restart else "#6b7280"
        
        restart_status_label = ctk.CTkLabel(restart_info, text=restart_status, font=ctk.CTkFont(size=13), text_color=restart_color, anchor="e")
        restart_status_label.pack(side="right")
        
        ctk.CTkLabel(restart_inner, text=t('auto_restart_desc'), font=ctk.CTkFont(size=11), text_color="#6b7280", wraplength=350, justify="left").pack(pady=(0, 12), anchor="w")
        
        restart_btn = ctk.CTkButton(
            restart_inner,
            text=f"✓ {t('on')}" if self.auto_restart else f"✗ {t('off')}",
            command=lambda: self.toggle_auto_restart(restart_btn, restart_status_label),
            width=380,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#10b981" if self.auto_restart else "#4b5563",
            hover_color="#059669" if self.auto_restart else "#374151"
        )
        restart_btn.pack()
        
        startup_card = ctk.CTkFrame(main, fg_color="#1f2937", corner_radius=12)
        startup_card.pack(fill="x", pady=10)
        
        startup_inner = ctk.CTkFrame(startup_card, fg_color="transparent")
        startup_inner.pack(fill="x", padx=20, pady=20)
        
        startup_info = ctk.CTkFrame(startup_inner, fg_color="transparent")
        startup_info.pack(fill="x", pady=(0, 12))
        
        ctk.CTkLabel(startup_info, text=f"🚀 {t('windows_startup')}", font=ctk.CTkFont(size=14, weight="bold"), anchor="w").pack(side="left")
        
        status_text = t('active') if is_in_startup() else t('passive')
        status_color = "#10b981" if is_in_startup() else "#6b7280"
        
        startup_status_label = ctk.CTkLabel(startup_info, text=status_text, font=ctk.CTkFont(size=13), text_color=status_color, anchor="e")
        startup_status_label.pack(side="right")
        
        ctk.CTkLabel(startup_inner, text=t('windows_startup_desc'), font=ctk.CTkFont(size=11), text_color="#6b7280", wraplength=350, justify="left").pack(pady=(0, 12), anchor="w")
        
        startup_btn = ctk.CTkButton(
            startup_inner,
            text=f"✓ {t('enabled')}" if is_in_startup() else f"✗ {t('disabled')}",
            command=lambda: self.toggle_startup(startup_btn, startup_status_label),
            width=380,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#10b981" if is_in_startup() else "#4b5563",
            hover_color="#059669" if is_in_startup() else "#374151"
        )
        startup_btn.pack()
        
        separator = ctk.CTkFrame(main, height=2, fg_color="#374151")
        separator.pack(fill="x", pady=20)
        
        def close_settings():
            self.settings_window.destroy()
            self.settings_window = None
        
        ctk.CTkButton(
            container,
            text=t('close'),
            command=close_settings,
            width=400,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#4b5563",
            hover_color="#374151",
            corner_radius=10
        ).pack(pady=(0, 0))
    
    def toggle_auto_restart(self, button, status_label):
        self.auto_restart = not self.auto_restart
        self.save_config()
        
        if self.auto_restart:
            button.configure(text=f"✓ {t('on')}", fg_color="#10b981", hover_color="#059669")
            status_label.configure(text=t('on'), text_color="#10b981")
        else:
            button.configure(text=f"✗ {t('off')}", fg_color="#4b5563", hover_color="#374151")
            status_label.configure(text=t('off'), text_color="#6b7280")
    
    def toggle_startup(self, button, status_label):
        if is_in_startup():
            if remove_from_startup():
                button.configure(text=f"✗ {t('disabled')}", fg_color="#4b5563", hover_color="#374151")
                status_label.configure(text=t('passive'), text_color="#6b7280")
        else:
            if add_to_startup():
                button.configure(text=f"✓ {t('enabled')}", fg_color="#10b981", hover_color="#059669")
                status_label.configure(text=t('active'), text_color="#10b981")
    
    def create_window(self):
        if self.window_open:
            return
            
        self.window_open = True
        self.window = ctk.CTk()
        self.window.title(t('app_title'))
        self.window.geometry("450x680")
        self.window.resizable(False, False)
        
        def on_closing():
            self.hide_window()
        
        self.window.protocol("WM_DELETE_WINDOW", on_closing)
        
        main_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        header = ctk.CTkFrame(main_frame, fg_color="#1f2937", corner_radius=15)
        header.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(header, text=t('memory_monitor'), font=ctk.CTkFont(size=28, weight="bold")).pack(pady=25)
        
        status_frame = ctk.CTkFrame(main_frame, fg_color="#1f2937", corner_radius=12)
        status_frame.pack(fill="x", pady=10)
        
        status_inner = ctk.CTkFrame(status_frame, fg_color="transparent")
        status_inner.pack(fill="x", padx=20, pady=15)
        
        ctk.CTkLabel(status_inner, text=t('status'), font=ctk.CTkFont(size=13), text_color="#9ca3af", anchor="w").pack(side="left")
        
        self.status_label = ctk.CTkLabel(status_inner, text=f"⚪ {t('not_running')}", font=ctk.CTkFont(size=15, weight="bold"), text_color="#6b7280", anchor="e")
        self.status_label.pack(side="right")
        
        memory_frame = ctk.CTkFrame(main_frame, fg_color="#1f2937", corner_radius=12)
        memory_frame.pack(fill="x", pady=10)
        
        memory_inner = ctk.CTkFrame(memory_frame, fg_color="transparent")
        memory_inner.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(memory_inner, text=t('memory_usage'), font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(0, 10))
        
        self.memory_label = ctk.CTkLabel(memory_inner, text="0 MB", font=ctk.CTkFont(size=40, weight="bold"))
        self.memory_label.pack(pady=10)
        
        self.limit_info_label = ctk.CTkLabel(memory_inner, text=f"{t('limit')}: {self.max_memory_mb} MB ({self.max_memory_mb/1024:.1f} GB)", font=ctk.CTkFont(size=12), text_color="#9ca3af")
        self.limit_info_label.pack(pady=(0, 5))
        
        progress_container = ctk.CTkFrame(memory_inner, fg_color="transparent")
        progress_container.pack(fill="x", pady=15)
        
        self.progress_bar = ctk.CTkProgressBar(progress_container, width=370, height=12, corner_radius=6, progress_color="#10b981")
        self.progress_bar.pack(pady=(0, 8))
        self.progress_bar.set(0)
        
        self.percent_label = ctk.CTkLabel(progress_container, text="0%", font=ctk.CTkFont(size=16, weight="bold"), text_color="#10b981")
        self.percent_label.pack()
        
        separator = ctk.CTkFrame(main_frame, height=2, fg_color="#374151")
        separator.pack(fill="x", pady=20)
        
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=5)
        
        top_buttons = ctk.CTkFrame(button_frame, fg_color="transparent")
        top_buttons.pack(fill="x", pady=5)
        
        ctk.CTkButton(
            top_buttons,
            text=f"⚙️ {t('configuration')}",
            command=self.show_config,
            width=400,
            height=50,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#8b5cf6",
            hover_color="#7c3aed",
            corner_radius=10
        ).pack(pady=5)
        
        ctk.CTkButton(
            top_buttons,
            text=f"🚀 {t('settings')}",
            command=self.show_settings,
            width=400,
            height=50,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#3b82f6",
            hover_color="#2563eb",
            corner_radius=10
        ).pack(pady=5)
        
        ctk.CTkButton(
            button_frame,
            text=t('hide'),
            command=on_closing,
            width=400,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#6b7280",
            hover_color="#4b5563",
            corner_radius=10
        ).pack(pady=5)
        
        info_frame = ctk.CTkFrame(main_frame, fg_color="#1f2937", corner_radius=8)
        info_frame.pack(fill="x", pady=(10, 0))
        
        self.interval_info_label = ctk.CTkLabel(info_frame, text=f"{t('update_interval')}: {self.update_interval}s • {self.process_name}", font=ctk.CTkFont(size=11), text_color="#9ca3af")
        self.interval_info_label.pack(pady=10)
        
        self.update_gui()
        
        def on_destroy(event):
            if event.widget == self.window:
                self.window_open = False
        
        self.window.bind("<Destroy>", on_destroy)
        self.window.mainloop()
    
    def setup_tray(self):
        def on_show(icon, item):
            self.show_window()
        
        def on_quit(icon, item):
            try:
                self.monitoring = False
                
                try:
                    icon.visible = False
                    icon.stop()
                except:
                    pass
                
                if self.settings_window:
                    try:
                        self.settings_window.quit()
                        self.settings_window.destroy()
                    except:
                        pass
                
                if self.config_window:
                    try:
                        self.config_window.quit()
                        self.config_window.destroy()
                    except:
                        pass
                
                if self.window and self.window_open:
                    try:
                        self.window.quit()
                        self.window.destroy()
                    except:
                        pass
                
                release_mutex()
                
            finally:
                import sys
                try:
                    sys.exit(0)
                except:
                    pass
                os._exit(0)
        
        def safe_show_settings(icon, item):
            try:
                self.show_window()
                time.sleep(0.5)
                if self.window_open and self.window:
                    self.show_settings()
            except Exception as e:
                pass
        
        menu = Menu(
            MenuItem(t('open'), on_show, default=True),
            MenuItem(t('settings'), safe_show_settings),
            Menu.SEPARATOR,
            MenuItem(t('exit'), on_quit)
        )
        
        self.tray_icon = Icon(
            "memory_monitor",
            self.create_tray_icon("gray"),
            t('app_title'),
            menu
        )
        
        def update_tray():
            last_color = None
            update_counter = 0
            
            while self.monitoring:
                color = self.get_status_color()
                
                if color != last_color:
                    self.tray_icon.icon = self.create_tray_icon(color)
                    last_color = color
                
                if update_counter % 2 == 0:
                    try:
                        if self.process_running:
                            usage = (self.current_memory / self.max_memory_mb) * 100
                            self.tray_icon.title = f"{t('app_title')}\n{self.current_memory:.1f} MB ({usage:.1f}%)"
                        else:
                            self.tray_icon.title = f"{t('app_title')}\n{t('not_running')}"
                    except:
                        pass
                
                update_counter += 1
                time.sleep(1)
                
                if update_counter >= 30:
                    gc.collect()
                    update_counter = 0
        
        Thread(target=update_tray, daemon=True).start()
        self.tray_icon.run()
    
    def start(self):
        Thread(target=self.monitor_process, daemon=True).start()
        
        if '--show-window' in sys.argv:
            time.sleep(0.5)
            self.show_window()
        
        self.setup_tray()

if __name__ == "__main__":
    check_single_instance()
    
    try:
        if not is_in_startup():
            add_to_startup()
        else:
            add_to_startup()
    except:
        pass
    
    app = MemoryMonitor()
    app.start()
