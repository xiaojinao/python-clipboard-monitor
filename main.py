#!/usr/bin/env python3
"""
剪贴板监听工具 - 主程序入口
"""

import sys
import os
from PySide6.QtWidgets import QApplication

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.ui.main_window import ClipboardApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    app.setApplicationName("剪贴板监听工具")
    app.setOrganizationName("ClipboardMonitor")
    
    window = ClipboardApp()
    window.show()
    sys.exit(app.exec())