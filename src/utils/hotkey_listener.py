import ctypes
import ctypes.wintypes
from PySide6.QtCore import QThread, Signal

MOD_CONTROL = 0x0002
MOD_ALT = 0x0001
MOD_SHIFT = 0x0004
MOD_WIN = 0x0008
WM_HOTKEY = 0x0312

user32 = ctypes.windll.user32
RegisterHotKey = user32.RegisterHotKey
UnregisterHotKey = user32.UnregisterHotKey


class GlobalHotkeyListener(QThread):
    """全局热键监听线程"""
    hotkey_pressed = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.hotkey_id = 1 
        self.running = False
        
    def register_hotkey(self):
        """注册全局热键"""
        if not RegisterHotKey(None, self.hotkey_id, MOD_CONTROL, 0x20):  # 0x20是空格键的虚拟键码
            print("注册全局热键失败")
            return False
        return True
        
    def unregister_hotkey(self):
        """注销全局热键"""
        UnregisterHotKey(None, self.hotkey_id)
        
    def run(self):
        """运行热键监听"""
        if not self.register_hotkey():
            return
            
        self.running = True
        msg = ctypes.wintypes.MSG()
        
        while self.running:
            if user32.PeekMessageA(ctypes.byref(msg), None, 0, 0, 0x0001):
                if msg.message == WM_HOTKEY:
                    self.hotkey_pressed.emit()
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageA(ctypes.byref(msg))
            else:
                self.msleep(10)  
                
    def stop(self):
        """停止监听"""
        self.running = False
        self.unregister_hotkey()
        self.quit()
        self.wait()