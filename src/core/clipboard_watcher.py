from PySide6.QtCore import QThread, QTimer, Signal
from PySide6.QtWidgets import QApplication


class ClipboardMonitor(QThread):
    """剪贴板监听线程"""
    clipboard_changed = Signal(str) 
    
    def __init__(self):
        super().__init__()
        self.last_clipboard_content = ""
        self.ignore_next_change = False  
        
    def run(self):
        """运行剪贴板监听"""
        clipboard = QApplication.clipboard()
        self.last_clipboard_content = clipboard.text()
        
        timer = QTimer()
        timer.timeout.connect(self.check_clipboard)
        timer.start(500)  
        
        self.exec()  
        
    def check_clipboard(self):
        """检查剪贴板是否变化"""
        clipboard = QApplication.clipboard()
        current_content = clipboard.text()
        
        if current_content and current_content != self.last_clipboard_content:
            if self.ignore_next_change:
                self.ignore_next_change = False
                self.last_clipboard_content = current_content
                return
                
            self.last_clipboard_content = current_content
            self.clipboard_changed.emit(current_content)
            
    def ignore_next_change(self):
        """设置忽略下一次剪贴板变化"""
        self.ignore_next_change = True