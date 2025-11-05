from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import QObject, Signal, QCoreApplication


class TrayIconManager(QObject):
    """系统托盘管理器"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tray_icon = None
        self.parent_window = None
        
    def setup_tray(self, parent_window, app_name="剪贴板监听工具"):
        """设置系统托盘"""
        self.parent_window = parent_window
        
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return False
            
        self.tray_icon = QSystemTrayIcon(parent_window)
        
        tray_menu = QMenu(parent_window)
        
        show_action = QAction("显示主窗口", parent_window)
        show_action.triggered.connect(self.show_normal)
        tray_menu.addAction(show_action)
        
        tray_menu.addSeparator()
        
        quit_action = QAction("退出", parent_window)
        quit_action.triggered.connect(parent_window.quit_app)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.setToolTip(app_name)
        
        app_icon = parent_window.style().standardIcon(parent_window.style().StandardPixmap.SP_ComputerIcon)
        self.tray_icon.setIcon(app_icon)
        
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        
        self.tray_icon.show()
        return True
        
    def on_tray_icon_activated(self, reason):
        """托盘图标激活事件"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_normal()
            
    def show_normal(self):
        """显示主窗口"""
        if self.parent_window:
            self.parent_window.showNormal()
            self.parent_window.raise_()
            self.parent_window.activateWindow()
        
    def show_notification(self, title, message, icon=QSystemTrayIcon.Information, duration=2000):
        """显示通知"""
        if self.tray_icon and self.tray_icon.isVisible():
            self.tray_icon.showMessage(title, message, icon, duration)
        
    def hide_tray(self):
        """隐藏托盘图标"""
        if self.tray_icon:
            self.tray_icon.hide()
            self.tray_icon = None
            
    def is_system_tray_available(self):
        """检查系统是否支持托盘"""
        return QSystemTrayIcon.isSystemTrayAvailable()
        
    def is_visible(self):
        """检查托盘图标是否可见"""
        return self.tray_icon and self.tray_icon.isVisible()